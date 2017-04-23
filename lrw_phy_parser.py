#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

MIC_LEN = 4
MSGDIR_DOWN = "down"
MSGDIR_UP = "up"

'''
MAC Command Parsers
'''
def print_detail(text):
    indent = "     ** Detail :"
    print(indent, text.strip())

def parse_maccmd_LinkCheckReq(hex_data):
    pass

def parse_maccmd_LinkCheckAns(hex_data):
    offset = 0
    #
    Margin = int(hex_data[offset], 16)
    print("    Margin: %d (%s)" % (Margin, hex_data[offset]))
    print_detail("""
The link margin in dB of the last successfully received
LinkCheckReq command.
A value of 0 means that the frame was received at the
demodulation floor (0 dB or no 28 margin) while a value of 20,
for example, means that the frame reached the gateway 20 dB
above the demodulation floor. Value 255 is reserved.
""")
    offset += 1
    #
    GwCnt = int(hex_data[offset], 16)
    print("    GwCnt: %d (%s)" % (GwCnt, hex_data[offset]))
    print_detail("""
the number of gateways that successfully received the
last 31 LinkCheckReq command."
""")

def parse_maccmd_LinkADRReq(hex_data):
    offset = 0
    #
    txp = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    DataRate_TXPower:", hex_data[offset])
    print("      DataRate: ", txp[0:3])
    print("      TXPower: ", txp[4:])
    print_detail("""
(region specific)
""")
    offset += 1
    #
    ChMask1 = bin(int(hex_data[offset], 16))[2:].zfill(8)
    ChMask2 = bin(int(hex_data[offset+1], 16))[2:].zfill(8)
    print("    ChMask:", ChMask1, ChMask2)
    print("      0...7 :", ChMask1)
    print("      8...15:", ChMask2)
    print_detail("""
set to 1 means that the corresponding channel can be used for
uplink transmissions if this channel allows the data
rate currently used by the end-device. A
bit set to 0 means the corresponding channels should be
avoided.
""")
    offset += 2
    #
    print("    Redundancy:", hex_data[offset])
    Redundancy = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("      RFU:", Redundancy[0])
    print("      ChMaskCntl:", Redundancy[1:4])
    print_detail("""
(region specific)
""")
    print("      NbTrans:", Redundancy[4:])
    print_detail("""
the number of transmissions for each uplink message.
This applies only to unconfirmed uplink frames.
The default value is 1 corresponding to a single transmission
of each frame.  The valid range is [1:15].
If NbTrans==0 is received the end-device should use the
default value. This field can be used
by the network manager to control the redundancy of the
node uplinks to obtain a given Quality of Service.
""")

def parse_maccmd_LinkADRAns(hex_data):
    offset = 0
    #
    Status = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    Status:", hex_data[offset], Status)
    print("      RFU:", Status[0:5])
    print("      Power ACK:", Status[5])
    if Status[5] == "0":
        print_detail("""
The channel mask sent enables a yet undefined
channel or the channel mask required all channels to be
disabled. The command was discarded and the end- device
state was not changed.
""")
    else:
        print_detail("""
The channel mask sent was successfully interpreted.
All currently defined channel states were set according
to the mask.
""")
    print("      Data rate ACK:", Status[6])
    if Status[6] == "0":
        print_detail("""
The data rate requested is unknown to the end-device
or is not possible given the channel mask provided
(not supported by any of the enabled channels). The
command was discarded and the end-device state was not
changed.
""")
    else:
        print_detail("""
The data rate was successfully set.
""")
    print("      Channel mask ACK:", Status[7])
    if Status[7] == "0":
        print_detail("""
The requested power level is not implemented in the device.
The command was discarded and the end- device state was not
changed.
""")
    else:
        print_detail("""
The power level was successfully set.
""")

def parse_maccmd_DutyCycleReq(hex_data):
    offset = 0
    #
    cycle = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    DutyCyclePL:", hex_data[offset])
    print("      RFU:", status[0:4])
    print("      MaxDCycle:", status[4])
    print_detail("""
A value of 0 corresponds to no duty cycle
limitation except the one set by the regional regulation.
""")

def parse_maccmd_DutyCycleAns(hex_data):
    pass

def parse_maccmd_RXParamSetupReq(hex_data):
    offset = 0
    #
    DLsettings = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    DLsettings:", hex_data[offset])
    print("      RFU:", DLsettings[0])
    print("      RX1DRoffset:", DLsettings[1:4])
    print_detail("""
The RX1DRoffset field sets the offset between the
uplink data rate and the downlink data
rate used to communicate with the end-device on
the first reception slot (RX1). As a default
this offset is 0. The offset is used to take
into account maximum power density constraints
for base stations in some regions and to balance
the uplink and downlink radio link margins.
""")
    print("      RX2DataRate:", DLsettings[4:])
    print_detail("""
The data rate (RX2DataRate) field defines
the data rate of a downlink using the second
receive window following the same convention as
the LinkADRReq command (0 means
DR0/125kHz for example). 
""")
    offset += 1
    #
    print("    Frequency:", ''.join(hex_data[offset:offset+3]))
    print_detail("""
The frequency (Frequency) field corresponds to the frequency of
the channel used for the second receive window,
whereby the frequency is coded following
the convention defined in the NewChannelReq
command.
""")

def parse_maccmd_RXParamSetupAns(hex_data):
    offset = 0
    #
    Status = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    RFU:", Status[0:5])
    print("    RX1DRoffset ACK:", Status[5])
    if Status[5] == "0":
        print_detail("""
The frequency requested is not usable by the end-device.
""")
    else:
        print_detail("""
RX2 slot channel was successfully set.
""")
    print("    RX2 Data rate ACK:", Status[6])
    if Status[6] == "0":
        print_detail("""
The data rate requested is unknown to the end-device.
""")
    else:
        print_detail("""
RX2 slot data rate was successfully set.
""")
    print("    Channel ACK:", Status[7])
    if Status[7] == "0":
        print_detail("""
the uplink/downlink data rate offset for RX1 slot is not in the allowed range.
""")
    else:
        print_detail("""
RX1DRoffset was successfully set.
""")

def parse_maccmd_DevStatusReq(hex_data):
    pass

def parse_maccmd_DevStatusAns(hex_data):
    offset = 0
    #
    Battery = int(hex_data[offset], 16)
    print("    Battery: %d (%s)" % (Battery, hex_data[offset]))
    if Battery == 255:
        print_detail("""
The end-device was not able to measure the battery level.
""")
    elif Battery == 0:
        print_detail("""
The end-device is connected to an external power source.
""")
    offset += 1
    Margin = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    Bargin: (%s)" % (hex_data[offset]))
    print("      RFU:", Margin[0:2])
    print("      Margin:", Margin[2:])
    print_detail("""
The margin (Margin) is the demodulation signal-to-noise ratio in dB rounded to
the nearest integer value for the last successfully received
DevStatusReq command. It is a signed
integer of 6 bits with a minimum value of -32
and a maximum value of 31.
""")

def parse_maccmd_NewChannelReq(hex_data):
    offset = 0
    #
    ChIndex = int(hex_data[offset], 16)
    print_detail("""
The channel index (ChIndex) is the index of the channel being
created or modified.
Depending on the region and frequency band used, the LoRaWAN specification imposes
default channels which must be common to all
devices and cannot be modified by the NewChannelReq command (cf. Chapter 6).
If the number of default channels is N, the default channels go from 0 to N-1,
and the acceptable range for ChIndex is N to 15.
A device must be able to handle at least 16
different channel definitions. In certain region
the device may have to store more than 16 channel definitions.
""")
    offset += 1
    #
    Freq = int(hex_data[offset], 16)
    print_detail("""
The frequency (Freq) field is a 24 bits unsigned integer. The actual channel
frequency in Hz
is 100 x Freq whereby values representing
frequencies below 100 MHz are reserved for
future use. This allows setting the frequency of
a channel anywhere between 100 MHz to
1.67 GHz in 100 Hz steps. A Freq value of 0
disables the channel. The end-device has to
check that the frequency is actually allowed by
its radio hardware and return an error
otherwise.
""")
    offset += 3
    #
    DrRange = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    DrRange: %s" % (hex_data[offset]))
    print("      MaxDR: ", DrRange[0:4])
    print("      MinDR: ", DrRange[4:])
    print_detail("""
the minimum data rate (MinDR) subfield
designate the lowest uplink data rate allowed on
this channel. For example 0 designates
DR0 / 125 kHz. Similarly, the maximum data rate
(MaxDR) designates the highest uplink
data rate. For example, DrRange = 0x77 means
that only 50 kbps GFSK is allowed on a
channel and DrRange = 0x50 means that DR0 / 125
kHz to DR5 / 125 kHz are supported.
""")

def parse_maccmd_NewChannelAns(hex_data):
    offset = 0
    #
    Status = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    RFU:", Status[0:6])
    print("    Data rate range ok:", Status[6])
    if Status[6] == "0":
        print_detail("""
The designated data rate range exceeds the ones currently defined for this end-
device.
""")
    else:
        print_detail("""
The data rate range is compatible with the possibilities of the end-device.
""")
    print("    Channel frequency ok:", Status[7])
    if Status[7] == "0":
        print_detail("""
The device cannot use this frequency.
""")
    else:
        print_detail("""
The device is able to use this frequency.
""")

def parse_maccmd_RXTimingSetupReq(hex_data):
    offset = 0
    #
    Settings = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    RFU:", Status[0:4])
    print("    Delay:", Status[4:])
    print_detail("""
The delay (Delay) field specifies the delay in second.
the value of 0 and 1 indicates 1 (s).
the value of 15 indicates 15 (s).
""")

def parse_maccmd_RXTimingSetupAns(hex_data):
    pass

def parse_maccmd_TxParamSetupReq(hex_data):
    offset = 0
    #
    DwellTime = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    RFU:", DwellTime[0:2])
    print("    DownlinkDwellTime:", DwellTime[2])
    print("    UplinkDwellTime:", DwellTime[3])
    print("    MaxEIRP:", DwellTime[4:])

def parse_maccmd_TxParamSetupAns(hex_data):
    pass

def parse_maccmd_DlChannelReq(hex_data):
    offset = 0
    #
    ChIndex = int(hex_data[offset], 16)
    print_detail("""
The channel index (ChIndex) is the index of the
channel whose downlink frequency is
modified.
""")
    offset += 1
    #
    Freq = int(hex_data[offset], 16)
    print_detail("""
The frequency (Freq) field is a 24 bits unsigned integer. The actual downlink
frequency in Hz
is 100 x Freq whereby values representing
frequencies below 100 MHz are reserved for
future use. The end-device has to check that the
frequency is actually allowed by its radio
hardware and return an error otherwise.
""")

def parse_maccmd_DlChannelAns(hex_data):
    offset = 0
    #
    Status = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    RFU:", Status[0:6])
    print("    Uplink frequency exists:", Status[6])
    if Status[6] == "0":
        print_detail("""
The uplink frequency is not defined for this channel, the downlink frequency
can only be set for a channel that already has
a valid uplink frequency
""")
    else:
        print_detail("""
The uplink frequency of the channel is valid.
""")
    print("    Channel frequency ok:", Status[7])
    if Status[7] == "0":
        print_detail("""
The device cannot use this frequency.
""")
    else:
        print_detail("""
The device is able to use this frequency.
""")

'''
Table for MAC Command Parser
    name: MAC command name
    octet: content size in octet.
    parser: function name.
'''
mac_cmd_tab = {
    "02": {
        MSGDIR_UP: {
            "name": "LinkCheckReq",
            "octet": 0,
            "parser": parse_maccmd_LinkCheckReq
        },
        MSGDIR_DOWN: {
            "name": "LinkCheckAns",
            "octet": 2,
            "parser": parse_maccmd_LinkCheckAns
        }
    },
    "03": {
        MSGDIR_UP: {
            "name": "LinkADRAns",
            "octet": 1,
            "parser": parse_maccmd_LinkADRAns
        },
        MSGDIR_DOWN: {
            "name": "LinkADRReq",
            "octet": 4,
            "parser": parse_maccmd_LinkADRReq
        }
    },
    "04": {
        MSGDIR_UP: {
            "name": "DutyCycleAns",
            "octet": 0,
            "parser": parse_maccmd_DutyCycleAns
        },
        MSGDIR_DOWN: {
            "name": "DutyCycleReq",
            "octet": 1,
            "parser": parse_maccmd_DutyCycleReq
        }
    },
    "05": {
        MSGDIR_UP: {
            "name": "RXParamSetupAns",
            "octet": 1,
            "parser": parse_maccmd_RXParamSetupAns
        },
        MSGDIR_DOWN: {
            "name": "RXParamSetupReq",
            "octet": 4,
            "parser": parse_maccmd_RXParamSetupReq
        }
    },
    "06": {
        MSGDIR_UP: {
            "name": "DevStatusAns",
            "octet": 2,
            "parser": parse_maccmd_DevStatusAns
        },
        MSGDIR_DOWN: {
            "name": "DevStatusReq",
            "octet": 0,
            "parser": parse_maccmd_DevStatusReq
        }
    },
    "07": {
        MSGDIR_UP: {
            "name": "NewChannelAns",
            "octet": 1,
            "parser": parse_maccmd_NewChannelAns
        },
        MSGDIR_DOWN: {
            "name": "NewChannelReq",
            "octet": 5,
            "parser": parse_maccmd_NewChannelReq
        }
    },
    "08": {
        MSGDIR_UP: {
            "name": "RXTimingSetupAns",
            "octet": 0,
            "parser": parse_maccmd_RXTimingSetupAns
        },
        MSGDIR_DOWN: {
            "name": "RXTimingSetupReq",
            "octet": 1,
            "parser": parse_maccmd_RXTimingSetupReq
        }
    },
    "09": {
        MSGDIR_UP: {
            "name": "TxParamSetupAns",
            "octet": 0,
            "parser": parse_maccmd_TxParamSetupAns
        },
        MSGDIR_DOWN: {
            "name": "TxParamSetupReq",
            "octet": 1,
            "parser": parse_maccmd_TxParamSetupReq
        }
    },
    "0a": {
        MSGDIR_UP: {
            "name": "DlChannelAns",
            "octet": 1,
            "parser": parse_maccmd_DlChannelAns
        },
        MSGDIR_DOWN: {
            "name": "DlChannelReq",
            "octet": 4,
            "parser": parse_maccmd_DlChannelReq
        }
    }
    }

def parse_mac_cmd(msg_dir, hex_data):
    offset = 0
    while offset < len(hex_data):
        cid = hex_data[offset]
        a = mac_cmd_tab.has_key(cid)
        if a:
            t = mac_cmd_tab[cid][msg_dir]
            offset += 1
            if t["octet"] == 0:
                print("  %s (%slink) [%s]" % (t["name"], msg_dir, cid))
            else:
                print("  %s (%slink) [%s] [%s]" % (t["name"], msg_dir, cid,
                    ''.join(hex_data[offset:offset+t["octet"]])))
            t["parser"](hex_data[offset:])
            offset += t["octet"]
        else:
            print("ERROR: Proprietary command [%s] has been found." %
                  hex_data[offset])
            raise("")

'''
MHDR parser
    7 6 5 | 4 3 2 |  1 0
    MType |  RFU  | Major
'''
def get_mtype_cmd(mtype):
    return {
        "000": "Join Request",
        "001": "Join Accept",
        "010": "Unconfirmed Data Up",
        "011": "Unconfirmed Data Down",
        "100": "Confirmed Data Up",
        "101": "Confirmed Data Down",
        "110": "RFU",
        "111": "Proprietary"
        }[mtype]

def get_major(major):
    return {
        "00": "LoRaWAN R1",
        "01": "RFU",
        "10": "RFU",
        "11": "RFU"
        }[major]

def parse_mhdr(hex_data):
    mhdr = hex_data[0]
    mhdr_bin = bin(int(mhdr, 16))[2:].zfill(8)
    mtype = mhdr_bin[0:3]
    mtype_cmd = get_mtype_cmd(mtype)
    mhdr_rfu = mhdr_bin[3:6]
    major = mhdr_bin[6:]
    print("## MHDR        (x%s): b%s" % (mhdr, mhdr_bin))
    print("  MType     (b%s): %s" % (mtype, get_mtype_cmd(mtype)))
    print("  RFU       (b%s):" % mhdr_rfu)
    print("  Major     (b%s): %s" % (major, get_major(major)))
    #
    return mtype

'''
MACPayload parser

- MACPayload
    FHDR | FPort | FRMPayload

- FHDR
       4    |   1   |   2  | 0...15
    DevAddr | FCtrl | FCnt | FOpts

- FCtrl for downlink
     7  |  6  |  5  |    4     |   3...0
    ADR | RFU | ACK | FPending | FOptsLen

- FCtrl for uplink
     7  |     6     |  5  |  4  |   3...0
    ADR | ADRACKReq | ACK | RFU | FOptsLen
'''
def parse_mac_payload(msg_dir, hex_data):
    devaddr = ''.join(hex_data[0:4][::-1])
    fctrl = hex_data[4]
    fctrl_bin = bin(int(fctrl, 16))[2:].zfill(8)
    adr = fctrl_bin[0:1]
    if msg_dir == MSGDIR_DOWN:
        fctrl_rfu = fctrl_bin[1:2]
        ack = fctrl_bin[2:3]
        fpending = fctrl_bin[3:4]
    else:
        adrackreq = fctrl_bin[1:2]
        ack = fctrl_bin[2:3]
        fctrl_rfu = fctrl_bin[3:4]
    foptslen = int(fctrl_bin[4:], 2)
    fcnt = int(''.join(hex_data[5:7][::-1]), 16)
    #
    print("  FHDR          (x%s)" % (''.join(hex_data)))
    print("    DevAddr     (x%s): %s" % (''.join(hex_data[:4]), devaddr))
    print("    FCtrl       (b%s): %s" % (fctrl_bin, fctrl))
    print("      ADR       :", adr)
    if msg_dir == MSGDIR_DOWN:
        print("      RFU       :", fctrl_rfu)
        print("      ACK       :", ack)
        print("      FPending  :", fpending)
    else:
        print("      ADRACKReq :", ack)
        print("      ACK       :", ack)
        print("      RFU       :", fctrl_rfu)
    print("      FOptsLen  :", foptslen)
    print("    FCnt        (x%s): %d" % (''.join(hex_data[5:7]), fcnt))

    '''
## FOptsLen, FOpts, FPort, FRMPayload

4.3.1.6 Frame options (FOptsLen in FCtrl, FOpts)
If FOptsLen is 0, the FOpts field is absent.
If FOptsLen is different from 0,
i.e. if MAC commands are present in the FOpts field, the port 0 cannot be used
(FPort must be either not present or different from 0).

MAC commands cannot be simultaneously present in the payload field and the frame
options field. Should this occur, the device shall ignore the frame.

4.3.2 Port field (FPort)
If the frame payload field is not empty, the port field must be present
If present, an FPort value of 0 indicates that the FRMPayload contains MAC commands

5 MAC Commands
A single data frame can contain any sequence of MAC commands, either piggybacked
in the FOpts field or, when sent as a separate data frame, in the FRMPayload field
with the FPort field being set to 0.
Piggybacked MAC commands are always sent without encryption and
must not exceed 15 octets. MAC commands sent as FRMPayload are always
encrypted and must not exceed the maximum FRMPayload length.

## Pseudo code

    #
    if foptslen is 0:
        fopts is None
    else:
        fopts is not None
    #
    if rest_len is 0:
        fport is None
    else:
        if fport == 0:
            if foptslen is not 0:
                ERROR
            else:
                FRMPayload is MACCommand.
        else:
            FRMPayload is a message.
    '''
    #
    fopts_offset = 7  # the index of the FOpts start.
    offset = fopts_offset
    fopts = None
    fport = None
    if foptslen:
        offset += foptslen
        fopts = hex_data[fopts_offset:offset]
        print("    FOpts       (x%s)" % (''.join(fopts)))
        print("## MAC Command (FOpts)")
        parse_mac_cmd(msg_dir, fopts)
    rest_len = len(hex_data[offset:])
    if rest_len:
        fport = hex_data[offset]
        print("## FPort       (x%s): %d" % (fport, int(fport, 16)))
        offset += 1
        rest_len -= 1
        if int(fport) == 0:
            if foptslen:
                print("ERROR: MAC Command is in both FOpts and FRMPayload.")
                raise("")
            # XXX
            # Here the spec in the section 5 said the FRMPayload must be MAC Commands.
            # But, there seems some devices use an app message with port 0.
            # So, currently, we don't parse it as MAC Commands.
            #
            #print("=== MAC Command (FRMPayload) ===")
            #parse_mac_cmd(msg_dir, hex_data[offset:])
            #
            print("WARNING: might be violate to the spec.")
            return rest_len
        elif int(fport) == "224":
            print("=== MAC Command test ===")
            return 0
        else:
            return rest_len
    #
    return 0

'''
JoinReq parser

      8    |   8    |    2
    AppEUI | DevEUI | DevNonce

'''
def parse_joinreq(hex_data):
    appeui = hex_data[0:8][::-1]
    deveui = hex_data[8:16][::-1]
    devnonce = hex_data[16:18]  # XXX little endian ?
    print("  AppEUI        (x%s): %s" % (''.join(appeui[::-1]), ''.join(appeui)))
    print("  DevEUI        (x%s): %s" % (''.join(deveui[::-1]), ''.join(deveui)))
    print("  DevNonce      (x%s): %s" % (''.join(devnonce),
                                         ''.join(devnonce[::-1])))

'''
JoinRes parser

        3    |   3   |    4    |     1      |    1    |  (16)
    AppNonce | NetID | DevAddr | DLSettings | RxDelay | (CFList)

'''
def parse_joinres(hex_data):
    # XXX endian check is not yet ?
    appnonce = hex_data[0:3]
    netid = hex_data[3:6]
    devaddr = hex_data[6:10]
    DLSettings = hex_data[10]
    RxDelay = hex_data[11]
    print("  AppNonce      : x%s" % (''.join(appnonce)))
    print("  NetID         : x%s" % (''.join(netid)))
    print("  DevAddr       : x%s" % (''.join(devaddr)))
    print("  DLSettings    : x%s" % (DLSettings))
    print("  RxDelay       : x%s" % (RxDelay))
    print("WARNING: not all implemented yet.")

'''
PHYPayload parser

      1  |    1...M   |  4
    MHDR | MACPayload | MIC
    MHDR |   JoinReq  | MIC
    MHDR |   JoinRes  | MIC
'''
def parse_phy_payload(hex_data):
    # payload: i.e. MACPayload, Join Req, JoinRes
    payload_len = len(hex_data) - MIC_LEN
    payload = hex_data[1:payload_len]
    mic = hex_data[-MIC_LEN:]
    #
    mtype = parse_mhdr(hex_data)
    #
    msg_dir = MSGDIR_UP
    if mtype in [ "000", "011", "101" ]:
        msg_dir = MSGDIR_DOWN
    #
    if mtype == "000":
        print("## JoinReq")
        parse_joinreq(payload)
    elif mtype == "001":
        print("## JoinRes")
        parse_joinres(payload)
    else:
        print("## MACPayload")
        rest_len = parse_mac_payload(msg_dir, payload)
        if rest_len:
            print("## FRMPayload:", ''.join(payload[-rest_len:]))
    #
    print("## MIC          : x%s" % (''.join(mic))) # XXX endian ?


def hexstr2array(hexstr):
    return [ hexstr[i:i+2] for i in range(0,len(hexstr),2) ]

'''
test code
'''
if __name__ == '__main__' :
    if len(sys.argv) == 1:
        hex_data = sys.stdin.readline().strip()
    elif sys.argv[1] in ["-h", "--help"] or len(sys.argv) != 2:
        print("Usage: %s (hex)" % (sys.argv[0]))
        print("    You can use stdin to pass the hex string as well.")
        exit(1)
    elif sys.argv[1] == "test":
        hex_data = "402105810080160102a6bf4432169ea0784416868d9420dd244619443e"
    else:
        hex_data = sys.argv[1]
    print("=== PHYPayload ===")
    parse_phy_payload(hexstr2array(hex_data))

