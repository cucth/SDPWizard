import _io
import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QWidget, QFileDialog, QMessageBox
# from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5 import QtCore
import SDPW_MainWindow
import IP4Edit

DEFINE_NBSP = " "
DEFINE_MY_NAME = "SDP Wizard (for Spectrum)"
DEFINE_MY_VERSION = "0.1-alpha"
DEFINE_MY_AUTHOR = "Charles Sun @Harmonic Inc. (2022)"

DEFINE_SDPTYPE_PROTO_VER: str = "v="
DEFINE_SDPTYPE_ORIGIN: str = "o="
DEFINE_SDPTYPE_SESS_NAME: str = "s="
DEFINE_SDPTYPE_SESS_INFO: str = "i="
DEFINE_SDPTYPE_TIME_SESS_ACT: str = "t="
DEFINE_SDPTYPE_SESS_ATTR: str = "a="
DEFINE_SDPTYPE_MEDIA: str = "m="
DEFINE_SDPTYPE_MEDIA_TITLE: str = "i="
DEFINE_SDPTYPE_MEDIA_CONN_INFO: str = "c="
DEFINE_SDPTYPE_MEDIA_ATTR: str = "a="

DEFINE_SDPATTR_GROUP: str = "group:"
DEFINE_SDPATTR_TOOL: str = "tool:"
DEFINE_SDPATTR_TIMESTAMP_REFCLK: str = "ts-refclk:"
DEFINE_SDPATTR_MEDIA_CLOCK: str = "mediaclk:"
DEFINE_SDPATTR_MEDIA_RTPMAP: str = "rtpmap:"
DEFINE_SDPATTR_MEDIA_FMTP: str = "fmtp:"
DEFINE_SDPATTR_MEDIA_ID: str = "mid:"
DEFINE_SDPATTR_MEDIA_PTIME: str = "ptime:"

DEFINE_SDPPARAM_VIDEO_FMTP_SAMPLING: str = "sampling="
DEFINE_SDPPARAM_VIDEO_FMTP_WIDTH: str = "width="
DEFINE_SDPPARAM_VIDEO_FMTP_HEIGHT: str = "height="
DEFINE_SDPPARAM_VIDEO_FMTP_EXACTFR: str = "exactframerate="
DEFINE_SDPPARAM_VIDEO_FMTP_INTERLACE: str = "interlace;"
DEFINE_SDPPARAM_VIDEO_FMTP_DEPTH: str = "depth="
DEFINE_SDPPARAM_VIDEO_FMTP_TCS: str = "TCS="
DEFINE_SDPPARAM_VIDEO_FMTP_COLORIMETRY: str = "colorimetry="
DEFINE_SDPPARAM_VIDEO_FMTP_PM: str = "PM="
DEFINE_SDPPARAM_VIDEO_FMTP_TP: str = "TP="
DEFINE_SDPPARAM_VIDEO_FMTP_TROFF: str = "TROFF="
DEFINE_SDPPARAM_VIDEO_FMTP_SSN: str = "SSN="
DEFINE_SDPPARAM_AUDIO_CHANNELORDER: str = "channel-order="

DEFINE_SDPVALUE_PROTO_VER: str = "0"
DEFINE_SDPVALUE_SESS_USERNAME: str = "-"
DEFINE_SDPVALUE_NETTYPE: str = "IN"
DEFINE_SDPVALUE_ADDRTYPE: str = "IP4"
DEFINE_SDPVALUE_SESS_START_TIME: str = "0"
DEFINE_SDPVALUE_SESS_STOP_TIME: str = "0"
DEFINE_SDPVALUE_TSREFCLK_CLKSRC: str = "ptp="
DEFINE_SDPVALUE_PTP_VER: str = "IEEE1588-2008:"
DEFINE_SDPVALUE_MEDIACLK_DIRECT_REF: str = "direct="  # as per RFC 7273 section 5.2 & ST 2110-10
DEFINE_SDPVALUE_MEDIACLK_OFFSET: str = "0"
DEFINE_SDPVALUE_FMTP_PARAM_TROFF: str = "0;"
DEFINE_SDPVALUE_FMTP_PARAM_SSN: str = "ST2110-20:2017;"
DEFINE_SDPVALUE_GROUP_TYPE: str = "DUP"  # as per RFC 7104
DEFINE_SDPVALUE_GROUP_FIRST: str = "first"
DEFINE_SDPVALUE_GROUP_SECOND: str = "second"
DEFINE_SDPVALUE_MEDIA_TYPE_VIDEO: str = "video"
DEFINE_SDPVALUE_MEDIA_TYPE_AUDIO: str = "audio"
DEFINE_SDPVALUE_MEDIA_TYPE_ANC: str = "video"
DEFINE_SDPVALUE_MEDIA_PROTOCOL_VIDEO: str = "RTP/AVP"
DEFINE_SDPVALUE_MEDIA_PROTOCOL_AUDIO: str = "RTP/AVP"
DEFINE_SDPVALUE_MEDIA_PROTOCOL_ANC: str = "RTP/AVP"
DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_VIDEO: str = "96"
DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_AUDIO: list[str] = ["97", "98", "99", "100"]
DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_ANC: str = "101"
DEFINE_SDPVALUE_MEDIA_SUBTYPE_VIDEO: str = "raw/"
DEFINE_SDPVALUE_MEDIA_SUBTYPE_ANC: str = "smpte291/"
DEFINE_SDPVALUE_MEDIA_CLOCKRATE_VIDEO: str = "90000"
DEFINE_SDPVALUE_MEDIA_CLOCKRATE_ANC: str = "90000"
DEFEIN_SDPVALUE_MEDIA_PTIME_1MS: str = "1"
DEFEIN_SDPVALUE_MEDIA_PTIME_125US: str = "0.125"
DEFEIN_SDPVALUE_MEDIA_SUBTYPE_AUDIO_L16: str = "L16/"
DEFEIN_SDPVALUE_MEDIA_SUBTYPE_AUDIO_L24: str = "L24/"
DEFEIN_SDPVALUE_MEDIA_SUBTYPE_AUDIO_L32: str = "L32/"
DEFEIN_SDPVALUE_MEDIA_SUBTYPE_AUDIO_AES3: str = "AM824/"
DEFEIN_SDPVALUE_MEDIA_AUDIO_SAMPLING_RATE: str = "48000/"
DEFINE_SDPVALUE_AUDIO_CHANNELORDER_ST: str = "SMPTE2110.(ST)"
DEFINE_SDPVALUE_AUDIO_CHANNELORDER_51: str = "SMPTE2110.(51)"
DEFINE_SDPVALUE_AUDIO_CHANNELORDER_AES3: str = "SMPTE2110.(AES3)"
DEFINE_SDPVALUE_AUDIO_CHANNELORDER_SGRP: str = "SMPTE2110.(SGRP)"

str_proto_ver: str = ""
str_sess_id: str = ""
str_sess_ver: str = ""
str_sess_origin: str = ""
str_sess_name_video: str = ""
str_sess_name_audio: str = ""
str_sess_name_anc: str = ""
str_sess_info_video: str = ""
str_sess_info_audio: str = ""
str_sess_info_anc: str = ""
str_sess_time: str = ""
str_sess_group: str = ""
str_sess_tool: str = ""
str_ptp_grandmaster_id: str = ""
str_ptp_domain: str = ""
str_media_refclk: str = ""
str_media_clock_isdirect: str = ""
str_origin_unicast_ipaddr: str = ""
str_media_video_fmtp_value_sampling: str = ""
str_media_video_fmtp_value_width: str = ""
str_media_video_fmtp_value_height: str = ""
str_media_video_fmtp_value_exactframerate: str = ""
str_media_video_fmtp_value_interlace: str = ""
str_media_video_fmtp_value_depth: str = ""
str_media_video_fmtp_value_tcs: str = ""
str_media_video_fmtp_value_colorimetry: str = ""
str_media_video_fmtp_value_pm: str = ""
str_media_video_fmtp_value_tp: str = ""
str_media_video_dest_mcaddr_first: str = ""
str_media_video_dest_mcaddr_second: str = ""
str_media_video_dest_mcport_first: str = ""
str_media_video_dest_mcport_second: str = ""
str_media_audio_dest_mcaddr_first: str = ""
str_media_audio_dest_mcaddr_second: str = ""
str_media_audio_dest_mcport_first: str = ""
str_media_audio_dest_mcport_second: str = ""
str_media_anc_dest_mcaddr_first: str = ""
str_media_anc_dest_mcaddr_second: str = ""
str_media_anc_dest_mcport_first: str = ""
str_media_anc_dest_mcport_second: str = ""
str_media_desc_video_first: str = ""
str_media_desc_video_second: str = ""
str_media_desc_audio_first: str = ""
str_media_desc_audio_second: str = ""
str_media_desc_anc_first: str = ""
str_media_desc_anc_second: str = ""
str_media_info_video_first: str = ""
str_media_info_video_second: str = ""
str_media_info_audio_first: str = ""
str_media_info_audio_second: str = ""
str_media_info_anc_first: str = ""
str_media_info_anc_second: str = ""
str_media_conn_video_first: str = ""
str_media_conn_video_second: str = ""
str_media_conn_audio_first: str = ""
str_media_conn_audio_second: str = ""
str_media_conn_anc_first: str = ""
str_media_conn_anc_second: str = ""
str_media_ttl_video: str = ""
str_media_ttl_audio: str = ""
str_media_ttl_anc: str = ""
str_media_rtpmap_video: str = ""
str_media_rtpmap_audio: list[str] = []
str_media_rtpmap_anc: str = ""
str_media_fmtp_video: str = ""
str_media_fmtp_audio: list[str] = []
str_media_fmtp_anc: str = ""
str_media_id_video_first: str = ""
str_media_id_video_second: str = ""
str_media_id_audio_first: str = ""
str_media_id_audio_second: str = ""
str_media_id_anc_first: str = ""
str_media_id_anc_second: str = ""
str_channel_name: str = ""
str_channel_role: str = ""
str_channel_role_short: str = ""
str_tap_id: str = ""
str_tap_channel: str = ""
str_ptime: str = ""
str_filename_sdp_video: str = ""
str_filename_sdp_audio: str = ""
str_filename_sdp_anc: str = ""
str_filename_sdps: str = ""
str_output_path: str = ""
str_sub_path: str = ""
str_ntp_timestamp: str = ""
flag_is_slot_calling: bool = False
comboboxes_audio_format: list[QWidget] = []
comboboxes_audio_trackqty: list[QWidget] = []
comboboxes_audio_sample_size: list[QWidget] = []
file: _io.TextIOWrapper


def configSDP() -> bool:
    global str_proto_ver
    global str_sess_id
    global str_sess_ver
    global str_sess_origin
    global str_origin_unicast_ipaddr
    global str_sess_name_video
    global str_sess_name_audio
    global str_sess_name_anc
    global str_sess_info_video
    global str_sess_info_audio
    global str_sess_info_anc
    global str_sess_time
    global str_sess_group
    global str_sess_tool
    global str_ptp_grandmaster_id
    global str_ptp_domain
    global str_media_refclk
    global str_media_clock_isdirect
    global str_media_video_fmtp_value_sampling
    global str_media_video_fmtp_value_width
    global str_media_video_fmtp_value_height
    global str_media_video_fmtp_value_exactframerate
    global str_media_video_fmtp_value_interlace
    global str_media_video_fmtp_value_depth
    global str_media_video_fmtp_value_tcs
    global str_media_video_fmtp_value_colorimetry
    global str_media_video_fmtp_value_pm
    global str_media_video_fmtp_value_tp
    global str_media_video_dest_mcaddr_first
    global str_media_video_dest_mcaddr_second
    global str_media_video_dest_mcport_first
    global str_media_video_dest_mcport_second
    global str_media_audio_dest_mcaddr_first
    global str_media_audio_dest_mcaddr_second
    global str_media_audio_dest_mcport_first
    global str_media_audio_dest_mcport_second
    global str_media_anc_dest_mcaddr_first
    global str_media_anc_dest_mcaddr_second
    global str_media_anc_dest_mcport_first
    global str_media_anc_dest_mcport_second
    global str_media_desc_video_first
    global str_media_desc_video_second
    global str_media_desc_audio_first
    global str_media_desc_audio_second
    global str_media_desc_anc_first
    global str_media_desc_anc_second
    global str_media_info_video_first
    global str_media_info_video_second
    global str_media_info_audio_first
    global str_media_info_audio_second
    global str_media_info_anc_first
    global str_media_info_anc_second
    global str_media_conn_video_first
    global str_media_conn_video_second
    global str_media_conn_audio_first
    global str_media_conn_audio_second
    global str_media_conn_anc_first
    global str_media_conn_anc_second
    global str_media_ttl_video
    global str_media_ttl_audio
    global str_media_ttl_anc
    global str_media_rtpmap_video
    global str_media_rtpmap_audio
    global str_media_rtpmap_anc
    global str_media_fmtp_video
    global str_media_fmtp_audio
    global str_media_fmtp_anc
    global str_media_id_video_first
    global str_media_id_video_second
    global str_media_id_audio_first
    global str_media_id_audio_second
    global str_media_id_anc_first
    global str_media_id_anc_second
    global str_channel_name
    global str_channel_role
    global str_channel_role_short
    global str_tap_id
    global str_tap_channel
    global str_ptime
    global comboboxes_audio_format
    global comboboxes_audio_trackqty
    global comboboxes_audio_sample_size
    global str_filename_sdp_video
    global str_filename_sdp_audio
    global str_filename_sdp_anc
    global str_filename_sdps
    global str_sub_path
    global str_ntp_timestamp

    str_proto_ver = DEFINE_SDPTYPE_PROTO_VER + DEFINE_SDPVALUE_PROTO_VER
    str_sess_id = MainWindow.ui.lineEdit_Sess_ID.text()
    str_sess_ver = MainWindow.ui.lineEdit_Sess_Ver.text()
    str_origin_unicast_ipaddr = MainWindow.ui.ip4Edit_origin_IpAddr.text()
    str_channel_name = MainWindow.ui.lineEdit_Channel_ID.text()
    str_tap_id = MainWindow.ui.lineEdit_Tap_ID.text()
    comboboxes_audio_format = [
        MainWindow.ui.comboBox_Audio_Format_Ch1and2,
        MainWindow.ui.comboBox_Audio_Format_Ch3and4,
        MainWindow.ui.comboBox_Audio_Format_Ch5and6,
        MainWindow.ui.comboBox_Audio_Format_Ch7and8
    ]
    comboboxes_audio_trackqty = [
        MainWindow.ui.comboBox_Audio_Track_Qty_Ch1and2,
        MainWindow.ui.comboBox_Audio_Track_Qty_Ch3and4,
        MainWindow.ui.comboBox_Audio_Track_Qty_Ch5and6,
        MainWindow.ui.comboBox_Audio_Track_Qty_Ch7and8
    ]
    comboboxes_audio_sample_size = [
        MainWindow.ui.comboBox_Audio_Sample_Size_Ch1and2,
        MainWindow.ui.comboBox_Audio_Sample_Size_Ch3and4,
        MainWindow.ui.comboBox_Audio_Sample_Size_Ch5and6,
        MainWindow.ui.comboBox_Audio_Sample_Size_Ch7and8
    ]
    str_media_rtpmap_audio = ["", "", "", ""]
    str_media_fmtp_audio = ["", "", "", ""]

    # verify session ID:

    # verify session verison:

    # verify unicast IP address:

    # Origin (o=<username> <sess-id> <sess-version> <nettype> <addrtype> <unicast-address>)
    str_sess_origin = \
        DEFINE_SDPTYPE_ORIGIN + \
        DEFINE_SDPVALUE_SESS_USERNAME + DEFINE_NBSP + \
        str_sess_id + DEFINE_NBSP + \
        str_sess_ver + DEFINE_NBSP + \
        DEFINE_SDPVALUE_NETTYPE + DEFINE_NBSP + \
        DEFINE_SDPVALUE_ADDRTYPE + DEFINE_NBSP + \
        str_origin_unicast_ipaddr
    # Session Name - Video, Audio, ANC
    str_sess_name_video = \
        DEFINE_SDPTYPE_SESS_NAME + "Video SDP file for Channel-" + \
        str_channel_name + "-" + str_channel_role + \
        ", output on Tap#" + str_tap_id + "-" + str_tap_channel
    str_sess_name_audio = \
        DEFINE_SDPTYPE_SESS_NAME + "Audio SDP file for Channel-" + \
        str_channel_name + "-" + str_channel_role + \
        ", output on Tap#" + str_tap_id + "-" + str_tap_channel
    str_sess_name_anc = \
        DEFINE_SDPTYPE_SESS_NAME + "Ancillary Data SDP file for Channel-" + \
        str_channel_name + "-" + str_channel_role + \
        ", output on Tap#" + str_tap_id + "-" + str_tap_channel
    # SDP file Name - Video, Audio, ANC
    str_filename_sdp_video = \
        "OUT_Tap" + str_tap_id + str_tap_channel + \
        "_CH-" + str_channel_name.upper() + \
        "-" + str_channel_role_short + \
        "_Video.sdp"
    str_filename_sdp_audio = \
        "OUT_Tap" + str_tap_id + str_tap_channel + \
        "_CH-" + str_channel_name.upper() + \
        "-" + str_channel_role_short + \
        "_Audio.sdp"
    str_filename_sdp_anc = \
        "OUT_Tap" + str_tap_id + str_tap_channel + \
        "_CH-" + str_channel_name.upper() + \
        "-" + str_channel_role_short + \
        "_ANC_Data.sdp"
    str_filename_sdps = \
        "OUT_Tap" + str_tap_id + str_tap_channel + \
        "_CH-" + str_channel_name.upper() + \
        "-" + str_channel_role_short + \
        ".sdps"
    str_sub_path = "OUT_Tap" + str_tap_id + str_tap_channel

    # Session Information - Video, Audio, ANC
    str_sess_info_video = \
        DEFINE_SDPTYPE_SESS_INFO + str_media_video_fmtp_value_height[0:-1]
    if str_media_video_fmtp_value_interlace == "interlace; ":
        str_sess_info_video += "i"
    else:
        str_sess_info_video += "p"

    if str_media_video_fmtp_value_exactframerate == "25;":
        str_sess_info_video += "25"
    elif str_media_video_fmtp_value_exactframerate == "50;":
        str_sess_info_video += "50"
    elif str_media_video_fmtp_value_exactframerate == "30000/1001;":
        str_sess_info_video += "29.97"
    elif str_media_video_fmtp_value_exactframerate == "60000/1001;":
        str_sess_info_video += "59.94"

    str_sess_info_video += " Video Stream, ST 2110-20"
    str_sess_info_audio = DEFINE_SDPTYPE_SESS_INFO + "Audio Stream Pair, ST 2110-30/31"
    str_sess_info_anc = DEFINE_SDPTYPE_SESS_INFO + "Ancillary Data Stream, ST 2110-40"
    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        str_sess_info_video += " with ST 2022-7"
        str_sess_info_audio += " with ST 2022-7"
        str_sess_info_anc += " with ST 2022-7"

    # Session Active Time
    str_sess_time = \
        DEFINE_SDPTYPE_TIME_SESS_ACT + DEFINE_SDPVALUE_SESS_START_TIME + \
        DEFINE_NBSP + DEFINE_SDPVALUE_SESS_STOP_TIME
    # Group Description for Media Streams
    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        str_sess_group = \
            DEFINE_SDPTYPE_SESS_ATTR + DEFINE_SDPATTR_GROUP + \
            DEFINE_SDPVALUE_GROUP_TYPE + DEFINE_NBSP + \
            DEFINE_SDPVALUE_GROUP_FIRST + DEFINE_NBSP + \
            DEFINE_SDPVALUE_GROUP_SECOND
    else:
        str_sess_group = ""
    # Session Authoring Tool
    str_sess_tool = \
        DEFINE_SDPTYPE_SESS_ATTR + DEFINE_SDPATTR_TOOL + \
        DEFINE_MY_NAME + \
        " ver" + DEFINE_MY_VERSION + \
        " by " + DEFINE_MY_AUTHOR

    # Video (Sole, or first+second; incl. media desc, info, conn, rtpmap, fmtp)
    str_media_video_dest_mcport_first = MainWindow.ui.lineEdit_Media_Video_First_Dest_Mcast_Port.text()
    str_media_desc_video_first = \
        DEFINE_SDPTYPE_MEDIA + DEFINE_SDPVALUE_MEDIA_TYPE_VIDEO + DEFINE_NBSP + \
        str_media_video_dest_mcport_first + DEFINE_NBSP + \
        DEFINE_SDPVALUE_MEDIA_PROTOCOL_VIDEO + DEFINE_NBSP + \
        DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_VIDEO
    str_media_video_dest_mcaddr_first = MainWindow.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.text()
    str_media_video_dest_mcport_first = MainWindow.ui.lineEdit_Media_Video_First_Dest_Mcast_Port.text()
    str_media_ttl_video = MainWindow.ui.lineEdit_Media_Conn_TTL.text()

    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        str_media_video_dest_mcport_second = MainWindow.ui.lineEdit_Media_Video_Second_Dest_Mcast_Port.text()
        str_media_desc_video_second = \
            DEFINE_SDPTYPE_MEDIA + DEFINE_SDPVALUE_MEDIA_TYPE_VIDEO + DEFINE_NBSP + \
            str_media_video_dest_mcport_second + DEFINE_NBSP + \
            DEFINE_SDPVALUE_MEDIA_PROTOCOL_VIDEO + DEFINE_NBSP + \
            DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_VIDEO
        str_media_info_video_first = \
            DEFINE_SDPTYPE_MEDIA_TITLE + "First Video Stream in 2022-7 Group"
        str_media_info_video_second = \
            DEFINE_SDPTYPE_MEDIA_TITLE + "Second Video Stream in 2022-7 Group"
        str_media_video_dest_mcaddr_second = MainWindow.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.text()
        str_media_video_dest_mcport_second = MainWindow.ui.lineEdit_Media_Video_Second_Dest_Mcast_Port.text()
        str_media_conn_video_second = \
            DEFINE_SDPTYPE_MEDIA_CONN_INFO + \
            DEFINE_SDPVALUE_NETTYPE + DEFINE_NBSP + \
            DEFINE_SDPVALUE_ADDRTYPE + DEFINE_NBSP + \
            str_media_video_dest_mcaddr_second + "/" + str_media_ttl_video
        str_media_id_video_first = \
            DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_ID + \
            DEFINE_SDPVALUE_GROUP_FIRST
        str_media_id_video_second = \
            DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_ID + \
            DEFINE_SDPVALUE_GROUP_SECOND
    else:
        str_media_info_video_first = \
            DEFINE_SDPTYPE_MEDIA_TITLE + "Video Stream"

    str_media_conn_video_first = \
        DEFINE_SDPTYPE_MEDIA_CONN_INFO + \
        DEFINE_SDPVALUE_NETTYPE + DEFINE_NBSP + \
        DEFINE_SDPVALUE_ADDRTYPE + DEFINE_NBSP + \
        str_media_video_dest_mcaddr_first + "/" + str_media_ttl_video
    str_media_rtpmap_video = \
        DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_RTPMAP + \
        DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_VIDEO + DEFINE_NBSP + \
        DEFINE_SDPVALUE_MEDIA_SUBTYPE_VIDEO + DEFINE_SDPVALUE_MEDIA_CLOCKRATE_VIDEO
    str_media_fmtp_video = \
        DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_FMTP + \
        DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_VIDEO + DEFINE_NBSP + \
        DEFINE_SDPPARAM_VIDEO_FMTP_SAMPLING + \
        str_media_video_fmtp_value_sampling + DEFINE_NBSP + \
        DEFINE_SDPPARAM_VIDEO_FMTP_WIDTH + \
        str_media_video_fmtp_value_width + DEFINE_NBSP + \
        DEFINE_SDPPARAM_VIDEO_FMTP_HEIGHT + \
        str_media_video_fmtp_value_height + DEFINE_NBSP + \
        DEFINE_SDPPARAM_VIDEO_FMTP_EXACTFR + \
        str_media_video_fmtp_value_exactframerate + DEFINE_NBSP + \
        str_media_video_fmtp_value_interlace + \
        DEFINE_SDPPARAM_VIDEO_FMTP_DEPTH + \
        str_media_video_fmtp_value_depth + DEFINE_NBSP + \
        DEFINE_SDPPARAM_VIDEO_FMTP_TCS + \
        str_media_video_fmtp_value_tcs + DEFINE_NBSP + \
        DEFINE_SDPPARAM_VIDEO_FMTP_COLORIMETRY + \
        str_media_video_fmtp_value_colorimetry + DEFINE_NBSP + \
        DEFINE_SDPPARAM_VIDEO_FMTP_PM + \
        str_media_video_fmtp_value_pm + DEFINE_NBSP + \
        DEFINE_SDPPARAM_VIDEO_FMTP_TP + \
        str_media_video_fmtp_value_tp + DEFINE_NBSP + \
        DEFINE_SDPPARAM_VIDEO_FMTP_TROFF + \
        DEFINE_SDPVALUE_FMTP_PARAM_TROFF + DEFINE_NBSP + \
        DEFINE_SDPPARAM_VIDEO_FMTP_SSN + DEFINE_SDPVALUE_FMTP_PARAM_SSN

    # Audio (Sole, or first+second; incl. media desc, info, conn, rtpmap, fmtp)
    str_media_audio_dest_mcport_first = MainWindow.ui.lineEdit_Media_Audio_First_Dest_Mcast_Port.text()
    str_media_desc_audio_first = \
        DEFINE_SDPTYPE_MEDIA + DEFINE_SDPVALUE_MEDIA_TYPE_AUDIO + DEFINE_NBSP + \
        str_media_audio_dest_mcport_first + DEFINE_NBSP + \
        DEFINE_SDPVALUE_MEDIA_PROTOCOL_AUDIO + DEFINE_NBSP
    for i in range(4):
        if comboboxes_audio_format[i].currentIndex() != 0 \
                and comboboxes_audio_trackqty[i].currentText() != "":
            str_media_desc_audio_first += DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_AUDIO[i]
            str_media_desc_audio_first += " "
    str_media_audio_dest_mcaddr_first = MainWindow.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.text()
    str_media_audio_dest_mcport_first = MainWindow.ui.lineEdit_Media_Audio_First_Dest_Mcast_Port.text()
    str_media_ttl_audio = MainWindow.ui.lineEdit_Media_Conn_TTL.text()

    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        str_media_audio_dest_mcport_second = MainWindow.ui.lineEdit_Media_Audio_Second_Dest_Mcast_Port.text()
        str_media_desc_audio_second = \
            DEFINE_SDPTYPE_MEDIA + DEFINE_SDPVALUE_MEDIA_TYPE_AUDIO + DEFINE_NBSP + \
            str_media_audio_dest_mcport_second + DEFINE_NBSP + \
            DEFINE_SDPVALUE_MEDIA_PROTOCOL_AUDIO + DEFINE_NBSP
        for i in range(4):
            if comboboxes_audio_format[i].currentIndex() != 0 \
                    and comboboxes_audio_trackqty[i].currentText() != "":
                str_media_desc_audio_second += DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_AUDIO[i]
                str_media_desc_audio_second += " "
        str_media_info_audio_first = \
            DEFINE_SDPTYPE_MEDIA_TITLE + "First Audio Stream in 2022-7 Group. "
        str_media_info_audio_second = \
            DEFINE_SDPTYPE_MEDIA_TITLE + "Second Audio Stream in 2022-7 Group. "
        for i in range(4):
            if comboboxes_audio_format[i].currentIndex() != 0 \
                    and comboboxes_audio_trackqty[i].isEnabled() \
                    and comboboxes_audio_trackqty[i].currentText() != "":
                if i > 0:
                    str_media_info_audio_first += ", and "
                    str_media_info_audio_second += ", and "
                str_media_info_audio_first += comboboxes_audio_trackqty[i].currentText()
                str_media_info_audio_second += comboboxes_audio_trackqty[i].currentText()
                str_media_info_audio_first += " channels"
                str_media_info_audio_second += " channels"
                if comboboxes_audio_format[i].currentIndex() == 1:
                    str_media_info_audio_first += " PCM Standard Stereo (L,R) "
                    str_media_info_audio_second += " PCM Standard Stereo (L,R) "
                elif comboboxes_audio_format[i].currentIndex() == 2:
                    str_media_info_audio_first += " PCM 5.1 Surround (L,R,C,LFE,Ls,Rs) "
                    str_media_info_audio_second += " PCM 5.1 Surround (L,R,C,LFE,Ls,Rs) "
                elif comboboxes_audio_format[i].currentIndex() == 3:
                    str_media_info_audio_first += " DolbyE Compressed in AES3 frame "
                    str_media_info_audio_second += " DolbyE Compressed in AES3 frame "
                str_media_info_audio_first += comboboxes_audio_sample_size[i].currentText()
                str_media_info_audio_second += comboboxes_audio_sample_size[i].currentText()
                str_media_info_audio_first += " samples"
                str_media_info_audio_second += " samples"
        str_media_audio_dest_mcaddr_second = MainWindow.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.text()
        str_media_audio_dest_mcport_second = MainWindow.ui.lineEdit_Media_Audio_Second_Dest_Mcast_Port.text()
        str_media_conn_audio_second = \
            DEFINE_SDPTYPE_MEDIA_CONN_INFO + \
            DEFINE_SDPVALUE_NETTYPE + DEFINE_NBSP + \
            DEFINE_SDPVALUE_ADDRTYPE + DEFINE_NBSP + \
            str_media_audio_dest_mcaddr_second + "/" + str_media_ttl_audio
        str_media_id_audio_first = \
            DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_ID + \
            DEFINE_SDPVALUE_GROUP_FIRST
        str_media_id_audio_second = \
            DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_ID + \
            DEFINE_SDPVALUE_GROUP_SECOND
    else:
        str_media_info_audio_first = \
            DEFINE_SDPTYPE_MEDIA_TITLE + "Audio Stream: "
        for i in range(4):
            if comboboxes_audio_format[i].currentIndex() != 0 \
                    and comboboxes_audio_trackqty[i].isEnabled() \
                    and comboboxes_audio_trackqty[i].currentText() != "":
                if i > 0:
                    str_media_info_audio_first += ", and "
                str_media_info_audio_first += comboboxes_audio_trackqty[i].currentText()
                str_media_info_audio_first += " channels"
                if comboboxes_audio_format[i].currentIndex() == 1:
                    str_media_info_audio_first += " PCM Standard Stereo (L,R) "
                elif comboboxes_audio_format[i].currentIndex() == 2:
                    str_media_info_audio_first += " PCM 5.1 Surround (L,R,C,LFE,Ls,Rs) "
                elif comboboxes_audio_format[i].currentIndex() == 3:
                    str_media_info_audio_first += " DolbyE Compressed in AES3 frame "
                str_media_info_audio_first += comboboxes_audio_sample_size[i].currentText()
                str_media_info_audio_first += " samples"
    str_media_conn_audio_first = \
        DEFINE_SDPTYPE_MEDIA_CONN_INFO + \
        DEFINE_SDPVALUE_NETTYPE + DEFINE_NBSP + \
        DEFINE_SDPVALUE_ADDRTYPE + DEFINE_NBSP + \
        str_media_audio_dest_mcaddr_first + "/" + str_media_ttl_audio

    for i in range(4):
        if comboboxes_audio_format[i].currentIndex() != 0 \
                and comboboxes_audio_trackqty[i].isEnabled() \
                and comboboxes_audio_trackqty[i].currentText() != "":
            str_media_rtpmap_audio[i] = \
                DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_RTPMAP + \
                DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_AUDIO[i] + DEFINE_NBSP
            if comboboxes_audio_sample_size[i].currentText() == "24bit":
                if comboboxes_audio_format[i].currentIndex() == 3:
                    str_media_rtpmap_audio[i] += DEFEIN_SDPVALUE_MEDIA_SUBTYPE_AUDIO_AES3
                else:
                    str_media_rtpmap_audio[i] += DEFEIN_SDPVALUE_MEDIA_SUBTYPE_AUDIO_L24
            elif comboboxes_audio_sample_size[i].currentText() == "16bit":
                str_media_rtpmap_audio[i] += DEFEIN_SDPVALUE_MEDIA_SUBTYPE_AUDIO_L16
            elif comboboxes_audio_sample_size[i].currentText() == "32bit":
                str_media_rtpmap_audio[i] += DEFEIN_SDPVALUE_MEDIA_SUBTYPE_AUDIO_L32
            str_media_rtpmap_audio[i] += DEFEIN_SDPVALUE_MEDIA_AUDIO_SAMPLING_RATE
            str_media_rtpmap_audio[i] += comboboxes_audio_trackqty[i].currentText()

            str_media_fmtp_audio[i] = \
                DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_FMTP + \
                DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_AUDIO[i] + DEFINE_NBSP + \
                DEFINE_SDPPARAM_AUDIO_CHANNELORDER
            if comboboxes_audio_format[i].currentIndex() == 1:
                str_media_fmtp_audio[i] += DEFINE_SDPVALUE_AUDIO_CHANNELORDER_ST
            elif comboboxes_audio_format[i].currentIndex() == 2:
                str_media_fmtp_audio[i] += DEFINE_SDPVALUE_AUDIO_CHANNELORDER_51
            elif comboboxes_audio_format[i].currentIndex() == 3:
                str_media_fmtp_audio[i] += DEFINE_SDPVALUE_AUDIO_CHANNELORDER_AES3

    # ANC (Sole, or first+second; incl. media desc, info, conn, rtpmap)
    str_media_anc_dest_mcport_first = MainWindow.ui.lineEdit_Media_ANC_First_Dest_Mcast_Port.text()
    str_media_desc_anc_first = \
        DEFINE_SDPTYPE_MEDIA + DEFINE_SDPVALUE_MEDIA_TYPE_ANC + DEFINE_NBSP + \
        str_media_anc_dest_mcport_first + DEFINE_NBSP + \
        DEFINE_SDPVALUE_MEDIA_PROTOCOL_ANC + DEFINE_NBSP +\
        DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_ANC

    str_media_anc_dest_mcaddr_first = MainWindow.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.text()
    str_media_anc_dest_mcport_first = MainWindow.ui.lineEdit_Media_ANC_First_Dest_Mcast_Port.text()
    str_media_ttl_anc = MainWindow.ui.lineEdit_Media_Conn_TTL.text()

    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        str_media_anc_dest_mcport_second = MainWindow.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port.text()
        str_media_desc_anc_second = \
            DEFINE_SDPTYPE_MEDIA + DEFINE_SDPVALUE_MEDIA_TYPE_ANC + DEFINE_NBSP + \
            str_media_anc_dest_mcport_second + DEFINE_NBSP + \
            DEFINE_SDPVALUE_MEDIA_PROTOCOL_ANC + DEFINE_NBSP
        str_media_info_anc_first = \
            DEFINE_SDPTYPE_MEDIA_TITLE + "First ST 291 ANC Data Stream in 2022-7 Group. "
        str_media_info_anc_second = \
            DEFINE_SDPTYPE_MEDIA_TITLE + "Second ST 291 ANC Data Stream in 2022-7 Group. "

        str_media_anc_dest_mcaddr_second = MainWindow.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.text()
        str_media_anc_dest_mcport_second = MainWindow.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port.text()
        str_media_conn_anc_second = \
            DEFINE_SDPTYPE_MEDIA_CONN_INFO + \
            DEFINE_SDPVALUE_NETTYPE + DEFINE_NBSP + \
            DEFINE_SDPVALUE_ADDRTYPE + DEFINE_NBSP + \
            str_media_anc_dest_mcaddr_second + "/" + str_media_ttl_anc
        str_media_id_anc_first = \
            DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_ID + \
            DEFINE_SDPVALUE_GROUP_FIRST
        str_media_id_anc_second = \
            DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_ID + \
            DEFINE_SDPVALUE_GROUP_SECOND
    else:
        str_media_info_anc_first = \
            DEFINE_SDPTYPE_MEDIA_TITLE + "ST 291 ANC Data Stream"

    str_media_conn_anc_first = \
        DEFINE_SDPTYPE_MEDIA_CONN_INFO + \
        DEFINE_SDPVALUE_NETTYPE + DEFINE_NBSP + \
        DEFINE_SDPVALUE_ADDRTYPE + DEFINE_NBSP + \
        str_media_anc_dest_mcaddr_first + "/" + str_media_ttl_anc
    str_media_rtpmap_anc = \
        DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_RTPMAP + \
        DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_ANC + DEFINE_NBSP + \
        DEFINE_SDPVALUE_MEDIA_SUBTYPE_ANC + DEFINE_SDPVALUE_MEDIA_CLOCKRATE_ANC

    # reference clock
    str_ptp_grandmaster_id = MainWindow.ui.lineEdit_Sess_PTP_GMID.text()
    str_ptp_domain = MainWindow.ui.lineEdit_Sess_PTP_Domain.text()
    str_media_refclk = \
        DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_TIMESTAMP_REFCLK + \
        DEFINE_SDPVALUE_TSREFCLK_CLKSRC + DEFINE_SDPVALUE_PTP_VER + \
        str_ptp_grandmaster_id + ":" + str_ptp_domain
    # media clock
    str_media_clock_isdirect = \
        DEFINE_SDPTYPE_MEDIA_ATTR + DEFINE_SDPATTR_MEDIA_CLOCK + \
        DEFINE_SDPVALUE_MEDIACLK_DIRECT_REF + DEFINE_SDPVALUE_MEDIACLK_OFFSET

    # F-validate input values
    def display_alarm(set_focus_QWidget, str_alarm):
        MainWindow.ui.tabWidget_SDPPreview.setCurrentIndex(0)
        MainWindow.ui.listWidget_SDPPreview_Video.clear()
        MainWindow.ui.listWidget_SDPPreview_Video.setStyleSheet(
            "color: red; font-style: bold; font-size: 20px")
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_alarm)
        set_focus_QWidget.setFocus()

    # F-1 validate origin unicast IP
    ipaddrlist = str_origin_unicast_ipaddr.split(".")
    for i in ipaddrlist:
        if i == "":
            display_alarm(MainWindow.ui.ip4Edit_origin_IpAddr.ip_part1, "Please complete input")
            return False
    if int(ipaddrlist[0]) >= 224:
        display_alarm(MainWindow.ui.ip4Edit_origin_IpAddr.ip_part1,
                      "IP should be unicast address. Multicast or reserved address cannot be used!")
        return False
    if int(ipaddrlist[0]) == 127:
        display_alarm(MainWindow.ui.ip4Edit_origin_IpAddr.ip_part1,
                      "127.x.x.x is local loopback address. Please use valid unicast address!")
        return False
    if int(ipaddrlist[0]) == 169 and int(ipaddrlist[1]) == 254:
        display_alarm(MainWindow.ui.ip4Edit_origin_IpAddr.ip_part1,
                      "169.254.x.x is automatic private address. Please use valid unicast address!")
        return False

    # F-2 validate TTL

    # F-3 validate video first dest mcast address

    # F-4 validate video first dest mcast port

    # F-5 validate video second dest mcast address

    # F-6 validate video second dest mcast port

    # F-7 validate audio first dest mcast address

    # F-8 validate audio first dest mcast port

    # F-9 validate audio second dest mcast address

    # F-10 validate audio second dest mcast port

    # F-11 validate ANC first dest mcast address

    # F-12 validate ANC first dest mcast port

    # F-13 validate ANC second dest mcast address

    # F-14 validate ANC second dest mcast port

    # Audio Packet Time
    str_ptime = \
        DEFINE_SDPTYPE_MEDIA_ATTR + \
        DEFINE_SDPATTR_MEDIA_PTIME + \
        DEFEIN_SDPVALUE_MEDIA_PTIME_1MS

    # Generate SDP preview
    # Video SDP
    MainWindow.ui.listWidget_SDPPreview_Video.clear()
    MainWindow.ui.listWidget_SDPPreview_Video.setStyleSheet(
        "alternate-background-color: #DEEAF6; font-family: Inconsolata; font-size: 15px")
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_proto_ver)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_sess_origin)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_sess_name_video)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_sess_info_video)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_sess_time)
    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_sess_group)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_sess_tool)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_desc_video_first)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_info_video_first)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_conn_video_first)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_rtpmap_video)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_fmtp_video)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_refclk)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_clock_isdirect)
    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_id_video_first)
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_desc_video_second)
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_info_video_second)
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_conn_video_second)
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_rtpmap_video)
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_fmtp_video)
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_refclk)
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_clock_isdirect)
        MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_id_video_second)
    # Audio SDP
    MainWindow.ui.listWidget_SDPPreview_Audio.clear()
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_proto_ver)
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_sess_origin)
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_sess_name_audio)
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_sess_info_audio)
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_sess_time)
    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_sess_group)
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_sess_tool)
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_desc_audio_first)
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_info_audio_first)
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_conn_audio_first)
    for i in range(4):
        if str_media_rtpmap_audio[i] != "":
            MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_rtpmap_audio[i])
            MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_fmtp_audio[i])
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_ptime)
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_refclk)
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_clock_isdirect)
    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_id_video_first)
        MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_desc_audio_second)
        MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_info_audio_second)
        MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_conn_audio_second)
        for i in range(4):
            if str_media_rtpmap_audio[i] != "":
                MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_rtpmap_audio[i])
                MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_fmtp_audio[i])
        MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_ptime)
        MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_refclk)
        MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_clock_isdirect)
        MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_id_video_second)
    # ANC SDP
    MainWindow.ui.listWidget_SDPPreview_ANC.clear()
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_proto_ver)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_sess_origin)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_sess_name_anc)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_sess_info_anc)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_sess_time)
    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_sess_group)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_sess_tool)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_desc_anc_first)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_info_anc_first)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_conn_anc_first)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_rtpmap_anc)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_refclk)
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_clock_isdirect)
    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_id_anc_first)
        MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_desc_anc_second)
        MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_info_anc_second)
        MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_conn_anc_second)
        MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_rtpmap_anc)
        MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_refclk)
        MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_clock_isdirect)
        MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_id_anc_second)
    # Channel SDPS
    MainWindow.ui.listWidget_SDPPreview_SDPS.clear()
    MainWindow.ui.listWidget_SDPPreview_SDPS.addItem(str_filename_sdp_video)
    MainWindow.ui.listWidget_SDPPreview_SDPS.addItem(str_filename_sdp_audio)
    MainWindow.ui.listWidget_SDPPreview_SDPS.addItem(str_filename_sdp_anc)
    MainWindow.ui.tabWidget_SDPPreview.setCurrentIndex(0)
    MainWindow.ui.pushButton_SavetoFile.setEnabled(True)

    # clear variables
    comboboxes_audio_format.clear()
    comboboxes_audio_trackqty.clear()
    comboboxes_audio_sample_size.clear()

    return True


def savetoFile() -> bool:
    global str_filename_sdp_video
    global str_filename_sdp_audio
    global str_filename_sdp_anc
    global str_filename_sdps
    global str_output_path
    global str_sub_path
    global str_tap_id
    global str_tap_channel
    global file

    str_output_path = QFileDialog.getExistingDirectory(None, "Choose Output Directory", os.getcwd())
    os.chdir(str_output_path or os.getcwd())
    str_sub_path = "Tap" + str_tap_id + str_tap_channel

    try:
        os.mkdir(str_sub_path)
    except FileExistsError:
        pass

    os.chdir((str_output_path or os.getcwd()) + "/" + str_sub_path)

    try:
        file = open(str_filename_sdp_video, 'w')
        for i in range(MainWindow.ui.listWidget_SDPPreview_Video.count()):
            file.write(MainWindow.ui.listWidget_SDPPreview_Video.item(i).text())
            file.write("\r\n")
    finally:
        if file:
            file.close()

    try:
        file = open(str_filename_sdp_audio, 'w')
        for i in range(MainWindow.ui.listWidget_SDPPreview_Audio.count()):
            file.write(MainWindow.ui.listWidget_SDPPreview_Audio.item(i).text())
            file.write("\r\n")
    finally:
        if file:
            file.close()

    try:
        file = open(str_filename_sdp_anc, 'w')
        for i in range(MainWindow.ui.listWidget_SDPPreview_ANC.count()):
            file.write(MainWindow.ui.listWidget_SDPPreview_ANC.item(i).text())
            file.write("\r\n")
    finally:
        if file:
            file.close()

    try:
        file = open(str_filename_sdps, 'w')
        for i in range(MainWindow.ui.listWidget_SDPPreview_SDPS.count()):
            file.write(MainWindow.ui.listWidget_SDPPreview_SDPS.item(i).text())
            file.write("\r\n")
    finally:
        if file:
            file.close()

    try:
        if os.path.getsize(str_filename_sdp_video) > 0:
            QMessageBox.information(None, "", "\nSDP files exported.", QMessageBox.Ok)
            return True
        else:
            QMessageBox.Warning(None, "", "\nSDP files export FAILED.", QMessageBox.Ok)
            return False
    except IOError:
        return False


def refresh_audio_combobox():
    global flag_is_slot_calling
    global comboboxes_audio_format
    global comboboxes_audio_trackqty
    global comboboxes_audio_sample_size
    flag_is_slot_calling = True
    track_qty_selected_in_current_line: str = ""

    int_audio_track_qty_already_used = 0

    comboboxes_audio_format = [
        MainWindow.ui.comboBox_Audio_Format_Ch1and2,
        MainWindow.ui.comboBox_Audio_Format_Ch3and4,
        MainWindow.ui.comboBox_Audio_Format_Ch5and6,
        MainWindow.ui.comboBox_Audio_Format_Ch7and8
    ]
    comboboxes_audio_trackqty = [
        MainWindow.ui.comboBox_Audio_Track_Qty_Ch1and2,
        MainWindow.ui.comboBox_Audio_Track_Qty_Ch3and4,
        MainWindow.ui.comboBox_Audio_Track_Qty_Ch5and6,
        MainWindow.ui.comboBox_Audio_Track_Qty_Ch7and8
    ]
    comboboxes_audio_sample_size = [
        MainWindow.ui.comboBox_Audio_Sample_Size_Ch1and2,
        MainWindow.ui.comboBox_Audio_Sample_Size_Ch3and4,
        MainWindow.ui.comboBox_Audio_Sample_Size_Ch5and6,
        MainWindow.ui.comboBox_Audio_Sample_Size_Ch7and8
    ]

    for i in range(4):
        if comboboxes_audio_format[i].currentIndex() == 0 and i < 3:  # if value is None
            comboboxes_audio_trackqty[i].clear()
            comboboxes_audio_trackqty[i].setDisabled(True)
            comboboxes_audio_sample_size[i].setDisabled(True)
            for j in range(i + 1, 4):  # Clear and disable lower lines
                comboboxes_audio_format[j].setCurrentIndex(0)
                comboboxes_audio_format[j].setDisabled(True)
                comboboxes_audio_trackqty[j].clear()
                comboboxes_audio_trackqty[j].setDisabled(True)
                comboboxes_audio_sample_size[j].setDisabled(True)
            break
        elif comboboxes_audio_format[i].currentIndex() == 0 and i == 3:  # if ch7&8 is "None"
            comboboxes_audio_trackqty[i].clear()
            comboboxes_audio_trackqty[i].setDisabled(True)
            comboboxes_audio_sample_size[i].setDisabled(True)
            break
        elif comboboxes_audio_format[i].currentIndex() in (1, 3):  # if value is PCM-ST, or DolbyE in AES frame
            if comboboxes_audio_trackqty[i].count() != 0:
                track_qty_selected_in_current_line = comboboxes_audio_trackqty[i].currentText()
                comboboxes_audio_trackqty[i].clear()
            for k in range(2, 10-int_audio_track_qty_already_used, 2):
                comboboxes_audio_trackqty[i].addItem(str(k))
                if str(k) == track_qty_selected_in_current_line:
                    comboboxes_audio_trackqty[i].setCurrentIndex(comboboxes_audio_trackqty[i].count()-1)
            comboboxes_audio_trackqty[i].setEnabled(True)
            if comboboxes_audio_trackqty[i].count() != 0:
                comboboxes_audio_sample_size[i].setEnabled(True)
        elif comboboxes_audio_format[i].currentIndex() == 2:  # if value is PCM 5.1
            comboboxes_audio_trackqty[i].clear()
            if int_audio_track_qty_already_used <= 2:
                comboboxes_audio_trackqty[i].addItem("6")
                comboboxes_audio_trackqty[i].setCurrentIndex(0)
                comboboxes_audio_trackqty[i].setEnabled(True)
            else:
                comboboxes_audio_trackqty[i].setDisabled(True)
                comboboxes_audio_sample_size[i].setDisabled(True)

        if int_audio_track_qty_already_used < 8 and i < 3:
            comboboxes_audio_format[i+1].setEnabled(True)
        if comboboxes_audio_trackqty[i].currentText() != "":
            int_audio_track_qty_already_used += int(comboboxes_audio_trackqty[i].currentText())

    comboboxes_audio_format.clear()
    comboboxes_audio_trackqty.clear()
    comboboxes_audio_sample_size.clear()
    flag_is_slot_calling = False
    return


class Main(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = SDPW_MainWindow.Ui_Main()
        self.ui.setupUi(self)

        self.ui.ip4Edit_origin_IpAddr = IP4Edit.Ip4Edit(self.ui.centralwidget)
        self.ui.ip4Edit_origin_IpAddr.setGeometry(QtCore.QRect(260, 130, 121, 21))
        self.ui.ip4Edit_origin_IpAddr.setAlignment(QtCore.Qt.AlignCenter)

        self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_Video)
        self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.setGeometry(QtCore.QRect(10, 50, 121, 21))
        self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)

        self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_Video)
        self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.setGeometry(QtCore.QRect(10, 100, 121, 21))
        self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)

        self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_Audio)
        self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.setGeometry(QtCore.QRect(10, 50, 121, 21))
        self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)

        self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_Audio)
        self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.setGeometry(QtCore.QRect(10, 100, 121, 21))
        self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)

        self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_ANC)
        self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.setGeometry(QtCore.QRect(10, 40, 121, 21))
        self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)

        self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_ANC)
        self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.setGeometry(QtCore.QRect(230, 40, 121, 21))
        self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)

        def checkBox_Media_DUP_Clicked():
            if self.ui.checkBox_Media_DUP.isChecked():
                self.ui.label_Media_Video_First_Dest.setText("First Destination:")
                self.ui.label_Media_Video_Second_Dest.show()
                self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.show()
                self.ui.label_Media_Video_Second_Colon.show()
                self.ui.lineEdit_Media_Video_Second_Dest_Mcast_Port.show()
                self.ui.label_Media_Audio_First_Dest.setText("First Destination:")
                self.ui.label_Media_Audio_Second_Dest.show()
                self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.show()
                self.ui.label_Media_Audio_Second_Colon.show()
                self.ui.lineEdit_Media_Audio_Second_Dest_Mcast_Port.show()
                self.ui.label_Media_ANC_First_Dest.setText("First Destination:")
                self.ui.label_Media_ANC_Second_Dest.show()
                self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.show()
                self.ui.label_Media_ANC_Second_Colon.show()
                self.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port.show()
            else:
                self.ui.label_Media_Video_First_Dest.setText("Destination:")
                self.ui.label_Media_Video_Second_Dest.hide()
                self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.hide()
                self.ui.label_Media_Video_Second_Colon.hide()
                self.ui.lineEdit_Media_Video_Second_Dest_Mcast_Port.hide()
                self.ui.label_Media_Audio_First_Dest.setText("Destination:")
                self.ui.label_Media_Audio_Second_Dest.hide()
                self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.hide()
                self.ui.label_Media_Audio_Second_Colon.hide()
                self.ui.lineEdit_Media_Audio_Second_Dest_Mcast_Port.hide()
                self.ui.label_Media_ANC_First_Dest.setText("Destination:")
                self.ui.label_Media_ANC_Second_Dest.hide()
                self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.hide()
                self.ui.label_Media_ANC_Second_Colon.hide()
                self.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port.hide()

        def checkBox_Sess_Generate_ID_Clicked():
            global str_ntp_timestamp
            if self.ui.checkBox_Sess_Generate_ID.isChecked():
                self.ui.lineEdit_Sess_ID.setDisabled(True)
                self.ui.lineEdit_Sess_Ver.setDisabled(True)
                str_ntp_timestamp = str(int((datetime.utcnow() - datetime(1900, 1, 1, 0, 0, 0)).total_seconds()))
                self.ui.lineEdit_Sess_ID.setText(str_ntp_timestamp)
                self.ui.lineEdit_Sess_Ver.setText(str_ntp_timestamp)
            else:
                self.ui.lineEdit_Sess_ID.setEnabled(True)
                self.ui.lineEdit_Sess_Ver.setEnabled(True)

        # A-Radio Button GROUP - Declare Variables for buttons in a group
        # A-1-Dir Model:
        self.radiobtns_dirmodel = [
            self.ui.radioButton_Media_Video_DirModel_VSX,
            self.ui.radioButton_Media_Video_DirModel_MIP9k,
            self.ui.radioButton_Media_Video_DirModel_NonSpectrum
        ]
        self.btngroup_dirmodel = QButtonGroup()
        # A-2-Res:
        self.radiobtns_res = [
            self.ui.radioButton_Media_Video_Res_HD1080i25,
            self.ui.radioButton_Media_Video_Res_HD1080p50,
            self.ui.radioButton_Media_Video_Res_UHD2160p50
        ]
        self.btngroup_res = QButtonGroup()
        # A-3-TCS:
        self.radiobtns_tcs = [
            self.ui.radioButton_Media_Video_TCS_SDR,
            self.ui.radioButton_Media_Video_TCS_HLG,
            self.ui.radioButton_Media_Video_TCS_PQ
        ]
        self.btngroup_tcs = QButtonGroup()
        # A-4-Sampling:
        self.radiobtns_sampling = [
            self.ui.radioButton_Media_Video_Sampling_422,
            self.ui.radioButton_Media_Video_Sampling_420
        ]
        self.btngroup_sampling = QButtonGroup()
        # A-5-Depth:
        self.radiobtns_depth = [
            self.ui.radioButton_Media_Video_Depth_8bit,
            self.ui.radioButton_Media_Video_Depth_10bit
        ]
        self.btngroup_depth = QButtonGroup()
        # A-6-Colorimetry:
        self.radiobtns_colorimetry = [
            self.ui.radioButton_Media_Video_Colorimetry_BT709,
            self.ui.radioButton_Media_Video_Colorimetry_BT2020
        ]
        self.btngroup_colorimetry = QButtonGroup()
        # A-7-Packing Mode:
        self.radiobtns_pm = [
            self.ui.radioButton_Media_Video_PM_GPM,
            self.ui.radioButton_Media_Video_PM_BPM
        ]
        self.btngroup_pm = QButtonGroup()
        # A-8-Channel Role:
        self.radiobtns_chnrole = [
            self.ui.radioButton_Channel_Role_Main,
            self.ui.radioButton_Channel_Role_Backup
        ]
        self.btngroup_chnrole = QButtonGroup()
        # A-9-Tap Channel:
        self.radiobtns_tapchn = [
            self.ui.radioButton_Tap_Channel_A,
            self.ui.radioButton_Tap_Channel_B
        ]
        self.btngroup_tapchn = QButtonGroup()

        # B-0-Slot for buttons
        def pushButton_GenSDP_Clicked():
            configSDP()

        def pushButton_SavetoFile_Clicked():
            savetoFile()

        # B-x-Radio Button GROUP - Slot for clicked
        # B-1-Dir Model:
        def slot_radiobtn_clicked_dirmodel():
            global str_media_video_fmtp_value_tp
            if self.btngroup_dirmodel.checkedId() == 0:
                str_media_video_fmtp_value_tp = "2110TPN;"
            elif self.btngroup_dirmodel.checkedId() == 1:
                str_media_video_fmtp_value_tp = "2110TPW;"
            else:
                str_media_video_fmtp_value_tp = "2110TPW;"

        # B-2-Res&FR
        def slot_radiobtn_clicked_res():
            global str_media_video_fmtp_value_width
            global str_media_video_fmtp_value_height
            global str_media_video_fmtp_value_exactframerate
            global str_media_video_fmtp_value_interlace
            if self.btngroup_res.checkedId() == 0:
                str_media_video_fmtp_value_width = "1920;"
                str_media_video_fmtp_value_height = "1080;"
                str_media_video_fmtp_value_exactframerate = "25;"
                str_media_video_fmtp_value_interlace = "interlace; "
            elif self.btngroup_res.checkedId() == 1:
                str_media_video_fmtp_value_width = "1920;"
                str_media_video_fmtp_value_height = "1080;"
                str_media_video_fmtp_value_exactframerate = "50;"
                str_media_video_fmtp_value_interlace = ""
            elif self.btngroup_res.checkedId() == 2:
                str_media_video_fmtp_value_width = "3840;"
                str_media_video_fmtp_value_height = "2160;"
                str_media_video_fmtp_value_exactframerate = "50;"
                str_media_video_fmtp_value_interlace = ""

        # B-3-TCS:
        def slot_radiobtn_clicked_tcs():
            global str_media_video_fmtp_value_tcs
            if self.btngroup_tcs.checkedId() == 0:
                str_media_video_fmtp_value_tcs = "SDR;"
            elif self.btngroup_tcs.checkedId() == 1:
                str_media_video_fmtp_value_tcs = "HLG;"
            elif self.btngroup_tcs.checkedId() == 2:
                str_media_video_fmtp_value_tcs = "PQ;"

        # B-4-sampling:
        def slot_radiobtn_clicked_sampling():
            global str_media_video_fmtp_value_sampling
            if self.btngroup_sampling.checkedId() == 0:
                str_media_video_fmtp_value_sampling = "YCbCr-4:2:2;"
            elif self.btngroup_sampling.checkedId() == 1:
                str_media_video_fmtp_value_sampling = "YCbCr-4:2:0;"

        # B-5-depth:
        def slot_radiobtn_clicked_depth():
            global str_media_video_fmtp_value_depth
            if self.btngroup_depth.checkedId() == 0:
                str_media_video_fmtp_value_depth = "8;"
            elif self.btngroup_depth.checkedId() == 1:
                str_media_video_fmtp_value_depth = "10;"

        # B-6-colorimetry:
        def slot_radiobtn_clicked_colorimetry():
            global str_media_video_fmtp_value_colorimetry
            if self.btngroup_colorimetry.checkedId() == 0:
                str_media_video_fmtp_value_colorimetry = "BT709;"
            elif self.btngroup_depth.checkedId() == 1:
                str_media_video_fmtp_value_colorimetry = "BT2020;"

        # B-7-Packing Mode:
        def slot_radiobtn_clicked_pm():
            global str_media_video_fmtp_value_pm
            if self.btngroup_pm.checkedId() == 0:
                str_media_video_fmtp_value_pm = "2110GPM;"
            elif self.btngroup_depth.checkedId() == 1:
                str_media_video_fmtp_value_pm = "2110BPM;"

        # B-8-Channel Role:
        def slot_radiobtn_clicked_chnrole():
            global str_channel_role
            global str_channel_role_short
            if self.btngroup_chnrole.checkedId() == 0:
                str_channel_role = "Main"
                str_channel_role_short = "M"
            elif self.btngroup_chnrole.checkedId() == 1:
                str_channel_role = "Backup"
                str_channel_role_short = "B"

        # B-9-Tap Channel:
        def slot_radiobtn_clicked_tapchn():
            global str_tap_channel
            if self.btngroup_tapchn.checkedId() == 0:
                str_tap_channel = "A"
            elif self.btngroup_tapchn.checkedId() == 1:
                str_tap_channel = "B"

        # B-10-Slots for (audio) combobox on index change
        def slot_combobox_indexchanged_audfmt_ch1and2():
            if not flag_is_slot_calling:
                refresh_audio_combobox()

        def slot_combobox_indexchanged_audfmt_ch3and4():
            if not flag_is_slot_calling:
                refresh_audio_combobox()

        def slot_combobox_indexchanged_audfmt_ch5and6():
            if not flag_is_slot_calling:
                refresh_audio_combobox()

        def slot_combobox_indexchanged_audfmt_ch7and8():
            if not flag_is_slot_calling:
                refresh_audio_combobox()

        def slot_combobox_indexchanged_trackqty_ch1and2():
            if not flag_is_slot_calling:
                refresh_audio_combobox()

        def slot_combobox_indexchanged_trackqty_ch3and4():
            if not flag_is_slot_calling:
                refresh_audio_combobox()

        def slot_combobox_indexchanged_trackqty_ch5and6():
            if not flag_is_slot_calling:
                refresh_audio_combobox()

        def slot_combobox_indexchanged_trackqty_ch7and8():
            if not flag_is_slot_calling:
                refresh_audio_combobox()

        # C-Connect to SLot
        # C-1-Dir Model:
        for i in range(len(self.radiobtns_dirmodel)):
            self.btngroup_dirmodel.addButton(self.radiobtns_dirmodel[i], i)
            self.radiobtns_dirmodel[i].clicked.connect(slot_radiobtn_clicked_dirmodel)
        # C-2-Res:
        for i in range(len(self.radiobtns_res)):
            self.btngroup_res.addButton(self.radiobtns_res[i], i)
            self.radiobtns_res[i].clicked.connect(slot_radiobtn_clicked_res)
        # C-3-TCS:
        for i in range(len(self.radiobtns_tcs)):
            self.btngroup_tcs.addButton(self.radiobtns_tcs[i], i)
            self.radiobtns_tcs[i].clicked.connect(slot_radiobtn_clicked_tcs)
        # C-4-Sampling:
        for i in range(len(self.radiobtns_sampling)):
            self.btngroup_sampling.addButton(self.radiobtns_sampling[i], i)
            self.radiobtns_sampling[i].clicked.connect(slot_radiobtn_clicked_sampling)
        # C-5-Depth:
        for i in range(len(self.radiobtns_depth)):
            self.btngroup_depth.addButton(self.radiobtns_depth[i], i)
            self.radiobtns_depth[i].clicked.connect(slot_radiobtn_clicked_depth)
        # C-6-Colorimetry:
        for i in range(len(self.radiobtns_colorimetry)):
            self.btngroup_colorimetry.addButton(self.radiobtns_colorimetry[i], i)
            self.radiobtns_colorimetry[i].clicked.connect(slot_radiobtn_clicked_colorimetry)
        # C-7-Packing Mode:
        for i in range(len(self.radiobtns_pm)):
            self.btngroup_pm.addButton(self.radiobtns_pm[i], i)
            self.radiobtns_pm[i].clicked.connect(slot_radiobtn_clicked_pm)
        # C-8-Channel Role:
        for i in range(len(self.radiobtns_chnrole)):
            self.btngroup_chnrole.addButton(self.radiobtns_chnrole[i], i)
            self.radiobtns_chnrole[i].clicked.connect(slot_radiobtn_clicked_chnrole)
        # C-9-Tap Channel:
        for i in range(len(self.radiobtns_tapchn)):
            self.btngroup_tapchn.addButton(self.radiobtns_tapchn[i], i)
            self.radiobtns_tapchn[i].clicked.connect(slot_radiobtn_clicked_tapchn)

        # C-10 single object
        self.ui.pushButton_GenSDP.clicked.connect(pushButton_GenSDP_Clicked)
        self.ui.pushButton_SavetoFile.clicked.connect(pushButton_SavetoFile_Clicked)
        self.ui.checkBox_Sess_Generate_ID.clicked.connect(checkBox_Sess_Generate_ID_Clicked)
        self.ui.checkBox_Media_DUP.clicked.connect(checkBox_Media_DUP_Clicked)
        self.ui.comboBox_Audio_Format_Ch1and2.currentIndexChanged.connect(slot_combobox_indexchanged_audfmt_ch1and2)
        self.ui.comboBox_Audio_Format_Ch3and4.currentIndexChanged.connect(slot_combobox_indexchanged_audfmt_ch3and4)
        self.ui.comboBox_Audio_Format_Ch5and6.currentIndexChanged.connect(slot_combobox_indexchanged_audfmt_ch5and6)
        self.ui.comboBox_Audio_Format_Ch7and8.currentIndexChanged.connect(slot_combobox_indexchanged_audfmt_ch7and8)
        self.ui.comboBox_Audio_Track_Qty_Ch1and2.currentIndexChanged.connect(
            slot_combobox_indexchanged_trackqty_ch1and2)
        self.ui.comboBox_Audio_Track_Qty_Ch3and4.currentIndexChanged.connect(
            slot_combobox_indexchanged_trackqty_ch3and4)
        self.ui.comboBox_Audio_Track_Qty_Ch5and6.currentIndexChanged.connect(
            slot_combobox_indexchanged_trackqty_ch5and6)
        self.ui.comboBox_Audio_Track_Qty_Ch7and8.currentIndexChanged.connect(
            slot_combobox_indexchanged_trackqty_ch7and8)

        # D-init value for each radio button group
        checkBox_Sess_Generate_ID_Clicked()
        checkBox_Media_DUP_Clicked()
        slot_radiobtn_clicked_dirmodel()
        slot_radiobtn_clicked_res()
        slot_radiobtn_clicked_tcs()
        slot_radiobtn_clicked_sampling()
        slot_radiobtn_clicked_depth()
        slot_radiobtn_clicked_colorimetry()
        slot_radiobtn_clicked_pm()
        slot_radiobtn_clicked_chnrole()
        slot_radiobtn_clicked_tapchn()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_())
