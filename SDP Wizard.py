import _io
import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, \
    QWidget, QFileDialog, QMessageBox, QAction, QDialog, QSizePolicy
from PyQt5 import QtCore
from lxml import etree
import SDPW_MainWindow
import Dialog_About
import IP4Edit

DEFINE_NBSP = " "
DEFINE_MY_NAME = "SDP Wizard (for Spectrum)"
DEFINE_MY_VERSION = "0.5.1-Beta"
DEFINE_MY_AUTHOR = "CharlesSun@HarmonicInc(2022)"

DEFINE_STYLESHEET_CODESTYLE_LISTWIDGET_WIN = \
    "alternate-background-color: #DEEAF6; font-family: Consolas; font-size: 15px"
DEFINE_STYLESHEET_CODESTYLE_LISTWIDGET_MACOS = \
    "alternate-background-color: #DEEAF6; font-family: Menlo; font-size: 14px"
DEFINE_STYLESHEET_CODESTYLE_COMBOBOX_WIN = "font-family: Consolas; font-size: 13px"
DEFINE_STYLESHEET_CODESTYLE_COMBOBOX_MACOS = "font-family: Menlo; font-size: 12px"
DEFINE_STYLESHEET_CODESTYLE_LINEEDIT_WIN = "font-family: Consolas; font-size: 12px"
DEFINE_STYLESHEET_CODESTYLE_LINEEDIT_MACOS = "font-family: Menlo; font-size: 12px"
DEFINE_LABEL_DIRECTION_SEND = "Destination:"
DEFINE_LABEL_DIRECTION_RECV = "Source:"
DEFINE_FILENAME_PREFIX_SEND = "Out_"
DEFINE_FILENAME_PREFIX_RECV = "In_"
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
DEFINE_SDPVALUE_MEDIA_DIRECTION_SENDONLY: str = "sendonly"
DEFINE_SDPVALUE_MEDIA_DIRECTION_RECVONLY: str = "recvonly"
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
str_media_direction: str = ""
str_media_direction_for_sess_name: str = ""
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
file_omdb_original: _io.TextIOWrapper
file_omdb_target: _io.TextIOWrapper
list_str_tap: list[str] = []
list_str_tapfamily: list[str] = []
str_lable_direction: str = ""
str_tooltip_multicast_addr: str = "Example Multicast Address:\n" \
                                  "239.210.120.011\n" \
                                  "    ????????? ????????? ????????????Stream ID in channel: 1:first, 2: second(in 2022-7 group)\n" \
                                  "    ????????? ????????? ????????????Channel ID\n" \
                                  "    ????????? ????????????????????????Stream type: 20:video(ST 2110-20), 30:audio, 40:ANC\n" \
                                  "    ????????? ????????????????????????Channel role: 1: Main, 2: Backup\n" \
                                  "    ????????????????????????????????????Protocol: 210:ST2110, 217:ST2110 with 2022-7\n"
str_tooltip_multicast_port: str = "Example Multicast Port:\n" \
                                  "45481\n" \
                                  "??????????????????Stream ID in channel: 1:first 2: second(in 2022-7 group)\n" \
                                  "??????????????????For \"HLIT\""
str_stylesheet_codestyle_listwidget: str = ""
str_stylesheet_codestyle_combobox: str = ""
str_stylesheet_codestyle_lineedit: str = ""
str_filename_prefix_direction: str = ""


def display_alarm(set_focus_QWidget=None, str_alarm=""):
    MainWindow.ui.tabWidget_SDPPreview.setCurrentIndex(0)
    MainWindow.ui.listWidget_SDPPreview_Video.clear()
    MainWindow.ui.listWidget_SDPPreview_Video.setStyleSheet(
        "color: red; font-style: bold; font-size: 20px")
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_alarm)
    if set_focus_QWidget is not None:
        set_focus_QWidget.setFocus()
    return


def parseOMDB() -> bool:
    global list_str_tap
    global list_str_tapfamily
    global file_omdb_original
    global file_omdb_target

    _tup_omdb_filename = QFileDialog.getOpenFileName(None,
                                                     "Choose OMDB file",
                                                     os.getcwd(),
                                                     "Omneon database (manager.oda);;All files (*.*)",
                                                     )
    if len(_tup_omdb_filename[0]) > 0:
        try:
            file_omdb_original = open(_tup_omdb_filename[0], 'r')
            file_omdb_target = open(_tup_omdb_filename[0] + ".tmp", 'w')
            for _str_tmp_line in file_omdb_original.readlines():
                _str_tmp_line = _str_tmp_line.replace("[", "_", -1)
                _str_tmp_line = _str_tmp_line.replace("]", "_", -1)
                file_omdb_target.write(_str_tmp_line)
            file_omdb_original.close()
            file_omdb_target.close()
        finally:
            if file_omdb_original:
                file_omdb_original.close()
            if file_omdb_target:
                file_omdb_target.close()
    else:
        MainWindow.ui.comboBox_Tap_ID.clear()
        display_alarm(None, "Open OMDB file failed. Please try again, or enter Tap ID manually.")
        return False

    _parser = etree.XMLParser(encoding="utf-8", recover=False)

    try:
        etree_omdb = etree.parse(_tup_omdb_filename[0] + ".tmp", parser=_parser)
    except OSError:
        display_alarm(None, "Open OMDB file failed. Please try again, or enter Tap ID manually.")
        return False

    os.remove(_tup_omdb_filename[0] + ".tmp")

    _list_node_tapsn = etree_omdb.xpath("/OmneonDatabase/Object[m_objectType/Uint32=65]/m_serialNum/String")
    _list_node_platformsn = etree_omdb.xpath("/OmneonDatabase/Object[m_objectType/Uint32=65]/m_strPlatformSN/String")
    _list_node_mipfamily = etree_omdb.xpath("/OmneonDatabase/Object[m_objectType/Uint32=65]/m_mediaPortFamily/String")

    MainWindow.ui.comboBox_Tap_ID.clear()
    MainWindow.ui.comboBox_Tap_ID.addItem("")

    if len(_list_node_tapsn) > 0:
        for i in range(len(_list_node_tapsn)):
            list_str_tap.append(_list_node_tapsn[i].text[1:-2] + " on " + _list_node_platformsn[i].text[1:-2])
            list_str_tapfamily.append(_list_node_mipfamily[i].text[1:-2])
            MainWindow.ui.comboBox_Tap_ID.addItem(list_str_tap[i])
        return True
    else:
        display_alarm(None, "OMDB parsing failed. Please try again, or enter Tap ID manually.")
        return False


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
    global str_media_direction

    str_proto_ver = DEFINE_SDPTYPE_PROTO_VER + DEFINE_SDPVALUE_PROTO_VER
    str_sess_id = MainWindow.ui.lineEdit_Sess_ID.text()
    str_sess_ver = MainWindow.ui.lineEdit_Sess_Ver.text()
    str_origin_unicast_ipaddr = MainWindow.ui.ip4Edit_origin_IpAddr.text()
    str_channel_name = MainWindow.ui.lineEdit_Channel_ID.text()
    str_tap_id = MainWindow.ui.comboBox_Tap_ID.currentText()

    if str_tap_id == "":
        display_alarm(MainWindow.ui.comboBox_Tap_ID,
                      "Tap ID is necessary. Enter \"00000\" or anything else if it's unknown.")
        return False

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

    def verify_mcast_addr(str_mcast_addr_to_verify: str, alarm_focus: QWidget):
        # default multicast address:
        """
        239.210.120.011
            ????????? ????????? ????????????stream ID in channel: 1:first 2: second(in 2022-7 group)
            ????????? ????????? ????????????channel ID
            ????????? ????????????????????????stream type: 20:video(ST 2110-20), 30:audio, 40:ANC
            ????????? ????????????????????????channel role: 1: Main, 2: Backup
            ????????????????????????????????????protocol: 210:ST2110, 217:ST2110 with 2022-7
        """
        list_str_mcast_addr_to_verify = str_mcast_addr_to_verify.split(".")
        for j in list_str_mcast_addr_to_verify[:]:
            if j == "":
                display_alarm(alarm_focus.ip_byte1, "Please complete input")
                return False
        if 223 < int(list_str_mcast_addr_to_verify[0]) < 240:
            if int(list_str_mcast_addr_to_verify[0]) == 224:
                if 0 < int(list_str_mcast_addr_to_verify[1]) < 5:
                    display_alarm(alarm_focus.ip_byte2,
                                  "The destination multicast address is allocate by IANA. \n \
                                  Allocation by IANA / IETF RFC-5771: \n \
                                  Address Range                 Size       Designation \n \
                                  -------------                 ----       ----------- \n \
                                  224.0.0.0 - 224.0.0.255       (/24)      Local Network Control Block \n \
                                  224.0.1.0 - 224.0.1.255       (/24)      Internetwork Control Block \n \
                                  224.0.2.0 - 224.0.255.255     (65024)    AD-HOC Block I \n \
                                  224.1.0.0 - 224.1.255.255     (/16)      RESERVED \n \
                                  224.2.0.0 - 224.2.255.255     (/16)      SDP/SAP Block \n \
                                  224.3.0.0 - 224.4.255.255     (2 /16s)   AD-HOC Block II \n \
                                  \n \
                                  Recommend to use 239.0.0.0 - 239.255.255.255"
                                  )
                    return False
            elif int(list_str_mcast_addr_to_verify[0]) == 232:
                display_alarm(alarm_focus.ip_byte1,
                              "The destination multicast address 232.x.x.x is allocate by IANA \n \
                              for Source-Specific Multicast(SSM). \n \
                              Please don't use 232/8 unless SSM is configured."
                              )
                return True
            elif int(list_str_mcast_addr_to_verify[0]) == 233:
                display_alarm(alarm_focus.ip_byte1,
                              "The destination multicast address is allocate by IANA. \n \
                              Allocation by IANA / IETF RFC-5771: \n \
                              Address Range                 Size       Designation \n \
                              -------------                 ----       ----------- \n \
                              233.0.0.0 - 233.251.255.255   (16515072) GLOP Block \n \
                              233.252.0.0 - 233.255.255.255 (/14)      AD-HOC Block III \n \
                              \n \
                              Recommend to use 239.0.0.0 - 239.255.255.255"
                              )
                return True
        else:
            display_alarm(alarm_focus.ip_byte1,
                          "Please enter a valid Multicast IP Address."
                          )
            return False
        return True

    def verify_mcast_port(str_mcast_port_to_verify: str, alarm_focus: QWidget):
        if str_mcast_port_to_verify.isdigit():
            if 0 < int(str_mcast_port_to_verify) < 65535:
                if int(str_mcast_port_to_verify) < 1024:
                    display_alarm(alarm_focus,
                                  "To avoid portantial confliction with system ports, \n \
                                  It's recommended to set multicast desination port between 1025 - 65535"
                                  )
                    return True
                return True
            else:
                display_alarm(alarm_focus, "Multicast desination port invalid!")
                return False
        else:
            display_alarm(alarm_focus, "Please enter multicast desination port!")
            return False

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
        ", " + str_media_direction_for_sess_name + \
        "Tap_" + str_tap_id[0:5] + "-" + \
        str_tap_channel + str_tap_id[5:]
    str_sess_name_audio = \
        DEFINE_SDPTYPE_SESS_NAME + "Audio SDP file for Channel-" + \
        str_channel_name + "-" + str_channel_role + \
        ", " + str_media_direction_for_sess_name + \
        "Tap_" + str_tap_id[0:5] + "-" + \
        str_tap_channel + str_tap_id[5:]
    str_sess_name_anc = \
        DEFINE_SDPTYPE_SESS_NAME + "Ancillary Data SDP file for Channel-" + \
        str_channel_name + "-" + str_channel_role + \
        ", " + str_media_direction_for_sess_name + \
        "Tap_" + str_tap_id[0:5] + "-" + \
        str_tap_channel + str_tap_id[5:]

    # SDP file Name - Video, Audio, ANC
    str_filename_sdp_video = \
        str_filename_prefix_direction + "Tap" + \
        str_tap_id + str_tap_channel[:5] + \
        "_CH-" + str_channel_name.upper() + \
        "-" + str_channel_role_short + \
        "_Video.sdp"
    str_filename_sdp_audio = \
        str_filename_prefix_direction + "Tap" + \
        str_tap_id + str_tap_channel[:5] + \
        "_CH-" + str_channel_name.upper() + \
        "-" + str_channel_role_short + \
        "_Audio.sdp"
    str_filename_sdp_anc = \
        str_filename_prefix_direction + "Tap" + \
        str_tap_id + str_tap_channel[:5] + \
        "_CH-" + str_channel_name.upper() + \
        "-" + str_channel_role_short + \
        "_ANC_Data.sdp"
    str_filename_sdps = \
        str_filename_prefix_direction + "Tap" + \
        str_tap_id + str_tap_channel[:5] + \
        "_CH-" + str_channel_name.upper() + \
        "-" + str_channel_role_short + \
        ".sdps"
    str_sub_path = \
        str_filename_prefix_direction + "Tap" + \
        str_tap_id[:5] + str_tap_channel

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
    str_media_video_fmtp_value_pm = "2110GPM;"
    str_media_fmtp_video = \
        DEFINE_SDPTYPE_MEDIA_ATTR + \
        DEFINE_SDPATTR_MEDIA_FMTP + \
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
        DEFINE_SDPPARAM_VIDEO_FMTP_SSN + \
        DEFINE_SDPVALUE_FMTP_PARAM_SSN + \
        DEFINE_NBSP

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
        DEFINE_SDPVALUE_MEDIA_PROTOCOL_ANC + DEFINE_NBSP + \
        DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_ANC

    str_media_anc_dest_mcaddr_first = MainWindow.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.text()
    str_media_anc_dest_mcport_first = MainWindow.ui.lineEdit_Media_ANC_First_Dest_Mcast_Port.text()
    str_media_ttl_anc = MainWindow.ui.lineEdit_Media_Conn_TTL.text()

    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        str_media_anc_dest_mcport_second = MainWindow.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port.text()
        str_media_desc_anc_second = \
            DEFINE_SDPTYPE_MEDIA + DEFINE_SDPVALUE_MEDIA_TYPE_ANC + DEFINE_NBSP + \
            str_media_anc_dest_mcport_second + DEFINE_NBSP + \
            DEFINE_SDPVALUE_MEDIA_PROTOCOL_ANC + DEFINE_NBSP + \
            DEFINE_SDPVALUE_MEDIA_RTPPAYLOAD_TYPE_ANC

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
    # F-1 verify origin unicast IP
    ipaddrlist_origin = str_origin_unicast_ipaddr.split(".")
    for i in ipaddrlist_origin[:]:
        if i == "":
            display_alarm(MainWindow.ui.ip4Edit_origin_IpAddr.ip_byte1, "Please complete input")
            return False
    if int(ipaddrlist_origin[0]) >= 224:
        display_alarm(MainWindow.ui.ip4Edit_origin_IpAddr.ip_byte1,
                      "IP should be unicast address. Multicast or reserved address cannot be used!")
        return False
    if int(ipaddrlist_origin[0]) == 127:
        display_alarm(MainWindow.ui.ip4Edit_origin_IpAddr.ip_byte1,
                      "127.x.x.x is local loopback address. Please use valid unicast address!")
        return False
    if int(ipaddrlist_origin[0]) == 169 and int(ipaddrlist_origin[1]) == 254:
        display_alarm(MainWindow.ui.ip4Edit_origin_IpAddr.ip_byte1,
                      "169.254.x.x is automatic private address. Please use valid unicast address!")
        return False

    # F-2 verify TTL
    if str_media_ttl_video.isdigit():
        if 0 < int(str_media_ttl_video) < 256:
            pass
        else:
            display_alarm(MainWindow.ui.lineEdit_Media_Conn_TTL,
                          "TTL should ba larger than 0. Max is 255. Recommended is 64.")

    # F-3 verify destination multicast address
    if not verify_mcast_addr(
            str_media_video_dest_mcaddr_first,
            MainWindow.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr):
        return False
    if not verify_mcast_addr(
            str_media_audio_dest_mcaddr_first,
            MainWindow.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr):
        return False
    if not verify_mcast_addr(
            str_media_anc_dest_mcaddr_first,
            MainWindow.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr):
        return False

    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        if not verify_mcast_addr(
                str_media_video_dest_mcaddr_second,
                MainWindow.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr):
            return False
        if not verify_mcast_addr(
                str_media_audio_dest_mcaddr_second,
                MainWindow.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr):
            return False
        if not verify_mcast_addr(
                str_media_anc_dest_mcaddr_second,
                MainWindow.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr):
            return False

    # F-4 verify destination multicast port
    if not verify_mcast_port(
            str_media_video_dest_mcport_first,
            MainWindow.ui.lineEdit_Media_Video_First_Dest_Mcast_Port):
        return False
    if not verify_mcast_port(
            str_media_audio_dest_mcport_first,
            MainWindow.ui.lineEdit_Media_Audio_First_Dest_Mcast_Port):
        return False
    if not verify_mcast_port(
            str_media_anc_dest_mcport_first,
            MainWindow.ui.lineEdit_Media_ANC_First_Dest_Mcast_Port):
        return False

    if MainWindow.ui.checkBox_Media_DUP.isChecked():
        if not verify_mcast_port(
                str_media_video_dest_mcport_second,
                MainWindow.ui.lineEdit_Media_Video_Second_Dest_Mcast_Port):
            return False
        if not verify_mcast_port(
                str_media_audio_dest_mcport_second,
                MainWindow.ui.lineEdit_Media_Audio_Second_Dest_Mcast_Port):
            return False
        if not verify_mcast_port(
                str_media_anc_dest_mcport_second,
                MainWindow.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port):
            return False

    # Audio Packet Time
    str_ptime = \
        DEFINE_SDPTYPE_MEDIA_ATTR + \
        DEFINE_SDPATTR_MEDIA_PTIME + \
        DEFEIN_SDPVALUE_MEDIA_PTIME_1MS

    # Generate SDP preview
    # Video SDP
    MainWindow.ui.listWidget_SDPPreview_Video.clear()
    if os.name == "posix":
        MainWindow.ui.listWidget_SDPPreview_Video.setStyleSheet(DEFINE_STYLESHEET_CODESTYLE_LISTWIDGET_MACOS)
    elif os.name == "nt":
        MainWindow.ui.listWidget_SDPPreview_Video.setStyleSheet(DEFINE_STYLESHEET_CODESTYLE_LISTWIDGET_WIN)

    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_proto_ver)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_sess_origin)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_sess_name_video)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_sess_info_video)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_sess_time)
    MainWindow.ui.listWidget_SDPPreview_Video.addItem(str_media_direction)
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
    MainWindow.ui.listWidget_SDPPreview_Audio.addItem(str_media_direction)
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
    MainWindow.ui.listWidget_SDPPreview_ANC.addItem(str_media_direction)
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
    str_sub_path = "Tap" + str_tap_id[:5] + str_tap_channel

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
            for k in range(2, 10 - int_audio_track_qty_already_used, 2):
                comboboxes_audio_trackqty[i].addItem(str(k))
                if str(k) == track_qty_selected_in_current_line:
                    comboboxes_audio_trackqty[i].setCurrentIndex(comboboxes_audio_trackqty[i].count() - 1)
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
            comboboxes_audio_format[i + 1].setEnabled(True)
        if comboboxes_audio_trackqty[i].currentText() != "":
            int_audio_track_qty_already_used += int(comboboxes_audio_trackqty[i].currentText())

    comboboxes_audio_format.clear()
    comboboxes_audio_trackqty.clear()
    comboboxes_audio_sample_size.clear()
    flag_is_slot_calling = False
    return


class About(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Dialog_About.Ui_Dlg_About()
        self.ui.setupUi(self)


class Main(QMainWindow):
    def __init__(self, parent=None):
        global str_stylesheet_codestyle_listwidget
        global str_stylesheet_codestyle_combobox
        global str_stylesheet_codestyle_lineedit
        super().__init__(parent)
        self.ui = SDPW_MainWindow.Ui_Main()
        self.ui.setupUi(self)
        self.about_action = QAction("About", self)

        if os.name == "posix":
            self.menubar = self.menuBar()
            self.about_menu = self.menubar.addMenu("About")
            self.about_menu.addAction(self.about_action)
            str_stylesheet_codestyle_listwidget = DEFINE_STYLESHEET_CODESTYLE_LISTWIDGET_MACOS
            str_stylesheet_codestyle_combobox = DEFINE_STYLESHEET_CODESTYLE_COMBOBOX_MACOS
            str_stylesheet_codestyle_lineedit = DEFINE_STYLESHEET_CODESTYLE_LINEEDIT_MACOS
        elif os.name == "nt":
            str_stylesheet_codestyle_listwidget = DEFINE_STYLESHEET_CODESTYLE_LISTWIDGET_WIN
            str_stylesheet_codestyle_combobox = DEFINE_STYLESHEET_CODESTYLE_COMBOBOX_WIN
            str_stylesheet_codestyle_lineedit = DEFINE_STYLESHEET_CODESTYLE_LINEEDIT_WIN

        self.ui.listWidget_SDPPreview_Video.setStyleSheet(str_stylesheet_codestyle_listwidget)
        self.ui.listWidget_SDPPreview_Audio.setStyleSheet(str_stylesheet_codestyle_listwidget)
        self.ui.listWidget_SDPPreview_ANC.setStyleSheet(str_stylesheet_codestyle_listwidget)
        self.ui.listWidget_SDPPreview_SDPS.setStyleSheet(str_stylesheet_codestyle_listwidget)
        self.ui.comboBox_Tap_ID.setStyleSheet(str_stylesheet_codestyle_combobox)

        self.ui.ip4Edit_origin_IpAddr = IP4Edit.Ip4Edit(self.ui.horizontalLayoutWidget)
        _sizepolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        _sizepolicy.setHorizontalStretch(0)
        _sizepolicy.setVerticalStretch(0)
        _sizepolicy.setHeightForWidth(self.ui.ip4Edit_origin_IpAddr.sizePolicy().hasHeightForWidth())
        self.ui.ip4Edit_origin_IpAddr.setSizePolicy(_sizepolicy)
        self.ui.ip4Edit_origin_IpAddr.setMinimumSize(QtCore.QSize(121, 21))
        self.ui.ip4Edit_origin_IpAddr.setMaximumSize(QtCore.QSize(121, 21))
        self.ui.ip4Edit_origin_IpAddr.setBaseSize(QtCore.QSize(121, 21))
        self.ui.ip4Edit_origin_IpAddr.setAcceptDrops(False)
        self.ui.ip4Edit_origin_IpAddr.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.ip4Edit_origin_IpAddr.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.verticalLayout_28.addWidget(self.ui.ip4Edit_origin_IpAddr)

        self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_Video)
        self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.setGeometry(QtCore.QRect(10, 50, 121, 21))
        self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.setToolTip(str_tooltip_multicast_addr)
        self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.setToolTipDuration(100000)
        self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.ip_byte1.setText("239")

        self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_Video)
        self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.setGeometry(QtCore.QRect(10, 100, 121, 21))
        self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.setToolTip(str_tooltip_multicast_addr)
        self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.setToolTipDuration(100000)
        self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.ip_byte1.setText("239")

        self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_Audio)
        self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.setGeometry(QtCore.QRect(10, 50, 121, 21))
        self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.setToolTip(str_tooltip_multicast_addr)
        self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.setToolTipDuration(100000)
        self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.ip_byte1.setText("239")

        self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_Audio)
        self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.setGeometry(QtCore.QRect(10, 100, 121, 21))
        self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.setToolTip(str_tooltip_multicast_addr)
        self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.setToolTipDuration(100000)
        self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.ip_byte1.setText("239")

        self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_ANC)
        self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.setGeometry(QtCore.QRect(10, 40, 121, 21))
        self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.setToolTip(str_tooltip_multicast_addr)
        self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.setToolTipDuration(100000)
        self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.ip_byte1.setText("239")

        self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr = IP4Edit.Ip4Edit(self.ui.groupBox_Dest_ANC)
        self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.setGeometry(QtCore.QRect(230, 40, 121, 21))
        self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.setToolTip(str_tooltip_multicast_addr)
        self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.setToolTipDuration(100000)
        self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.ip_byte1.setText("239")

        self.ui.lineEdit_Media_Video_First_Dest_Mcast_Port.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.lineEdit_Media_Video_Second_Dest_Mcast_Port.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.lineEdit_Media_Audio_First_Dest_Mcast_Port.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.lineEdit_Media_Audio_Second_Dest_Mcast_Port.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.lineEdit_Media_ANC_First_Dest_Mcast_Port.setStyleSheet(str_stylesheet_codestyle_lineedit)
        self.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port.setStyleSheet(str_stylesheet_codestyle_lineedit)

        self.ui.lineEdit_Media_Video_First_Dest_Mcast_Port.setToolTip(str_tooltip_multicast_port)
        self.ui.lineEdit_Media_Video_Second_Dest_Mcast_Port.setToolTip(str_tooltip_multicast_port)
        self.ui.lineEdit_Media_Audio_First_Dest_Mcast_Port.setToolTip(str_tooltip_multicast_port)
        self.ui.lineEdit_Media_Audio_Second_Dest_Mcast_Port.setToolTip(str_tooltip_multicast_port)
        self.ui.lineEdit_Media_ANC_First_Dest_Mcast_Port.setToolTip(str_tooltip_multicast_port)
        self.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port.setToolTip(str_tooltip_multicast_port)

        self.ui.lineEdit_Media_Video_First_Dest_Mcast_Port.setToolTipDuration(100000)
        self.ui.lineEdit_Media_Video_Second_Dest_Mcast_Port.setToolTipDuration(100000)
        self.ui.lineEdit_Media_Audio_First_Dest_Mcast_Port.setToolTipDuration(100000)
        self.ui.lineEdit_Media_Audio_Second_Dest_Mcast_Port.setToolTipDuration(100000)
        self.ui.lineEdit_Media_ANC_First_Dest_Mcast_Port.setToolTipDuration(100000)
        self.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port.setToolTipDuration(100000)

        # slot for some widgets
        def slot_checkBox_Media_DUP_Clicked():
            if self.ui.checkBox_Media_DUP.isChecked():
                self.ui.label_Media_Video_First_Dest.setText("First " + str_lable_direction)
                self.ui.label_Media_Video_Second_Dest.setText("Second " + str_lable_direction)
                self.ui.label_Media_Video_Second_Dest.show()
                self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.show()
                self.ui.label_Media_Video_Second_Colon.show()
                self.ui.lineEdit_Media_Video_Second_Dest_Mcast_Port.show()
                self.ui.label_Media_Audio_First_Dest.setText("First " + str_lable_direction)
                self.ui.label_Media_Audio_Second_Dest.setText("Second " + str_lable_direction)
                self.ui.label_Media_Audio_Second_Dest.show()
                self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.show()
                self.ui.label_Media_Audio_Second_Colon.show()
                self.ui.lineEdit_Media_Audio_Second_Dest_Mcast_Port.show()
                self.ui.label_Media_ANC_First_Dest.setText("First " + str_lable_direction)
                self.ui.label_Media_ANC_Second_Dest.setText("Second " + str_lable_direction)
                self.ui.label_Media_ANC_Second_Dest.show()
                self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.show()
                self.ui.label_Media_ANC_Second_Colon.show()
                self.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port.show()
                self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.ip_byte2.setText("217")
                self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.ip_byte2.setText("217")
                self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.ip_byte2.setText("217")
                self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.ip_byte2.setText("217")
                self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.ip_byte2.setText("217")
                self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.ip_byte2.setText("217")
            else:
                self.ui.label_Media_Video_First_Dest.setText(str_lable_direction)
                self.ui.label_Media_Video_Second_Dest.hide()
                self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.hide()
                self.ui.label_Media_Video_Second_Colon.hide()
                self.ui.lineEdit_Media_Video_Second_Dest_Mcast_Port.hide()
                self.ui.label_Media_Audio_First_Dest.setText(str_lable_direction)
                self.ui.label_Media_Audio_Second_Dest.hide()
                self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.hide()
                self.ui.label_Media_Audio_Second_Colon.hide()
                self.ui.lineEdit_Media_Audio_Second_Dest_Mcast_Port.hide()
                self.ui.label_Media_ANC_First_Dest.setText(str_lable_direction)
                self.ui.label_Media_ANC_Second_Dest.hide()
                self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.hide()
                self.ui.label_Media_ANC_Second_Colon.hide()
                self.ui.lineEdit_Media_ANC_Second_Dest_Mcast_Port.hide()
                self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.ip_byte2.setText("210")
                self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.ip_byte2.setText("210")
                self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.ip_byte2.setText("210")
                self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.ip_byte2.setText("210")
                self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.ip_byte2.setText("210")
                self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.ip_byte2.setText("210")

        def slot_checkBox_Sess_Generate_ID_Clicked():
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

        def slot_lineEdit_Channel_ID_Edited():
            global str_channel_name
            str_channel_name = self.ui.lineEdit_Channel_ID.text()
            if str_channel_name.isdigit() and 0 < int(str_channel_name) < 26:
                str_temp = str_channel_name
            else:
                str_temp = "1"
            self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.ip_byte4.setText(str_temp + "1")
            self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.ip_byte4.setText(str_temp + "2")
            self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.ip_byte4.setText(str_temp + "1")
            self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.ip_byte4.setText(str_temp + "2")
            self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.ip_byte4.setText(str_temp + "1")
            self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.ip_byte4.setText(str_temp + "2")

        def slot_checkBox_Tap_ID_Edited():
            _int_current_index = self.ui.comboBox_Tap_ID.currentIndex()
            if 0 < _int_current_index < len(list_str_tapfamily) + 1:
                self.ui.comboBox_Tap_ID.setEditable(False)
                if list_str_tapfamily[_int_current_index - 1] == "tap8_vsx":
                    self.ui.radioButton_Media_Video_DirModel_VSX.setEnabled(True)
                    self.ui.radioButton_Media_Video_DirModel_VSX.setChecked(True)
                    self.ui.radioButton_Media_Video_DirModel_MIP9k.setChecked(False)
                    self.ui.radioButton_Media_Video_DirModel_MIP9k.setDisabled(True)
                elif list_str_tapfamily[_int_current_index - 1] == "tap8":
                    self.ui.radioButton_Media_Video_DirModel_MIP9k.setEnabled(True)
                    self.ui.radioButton_Media_Video_DirModel_MIP9k.setChecked(True)
                    self.ui.radioButton_Media_Video_DirModel_VSX.setChecked(False)
                    self.ui.radioButton_Media_Video_DirModel_VSX.setDisabled(True)
                else:
                    self.ui.radioButton_Media_Video_DirModel_VSX.setEnabled(True)
                    self.ui.radioButton_Media_Video_DirModel_MIP9k.setEnabled(True)
            else:
                self.ui.radioButton_Media_Video_DirModel_VSX.setEnabled(True)
                self.ui.radioButton_Media_Video_DirModel_MIP9k.setEnabled(True)
                self.ui.comboBox_Tap_ID.setEditable(True)
                if len(self.ui.comboBox_Tap_ID.currentText()) > 5:
                    self.ui.comboBox_Tap_ID.setCurrentText(self.ui.comboBox_Tap_ID.currentText()[:5])

        # A-Radio Button GROUP - Declare Variables for buttons in a group
        # A-1-Dir Model:
        self.radiobtns_dirmodel = [
            self.ui.radioButton_Media_Video_DirModel_VSX,
            self.ui.radioButton_Media_Video_DirModel_MIP9k
        ]
        self.btngroup_dirmodel = QButtonGroup()
        # A-2-Res:
        self.radiobtns_res = [
            self.ui.radioButton_Media_Video_Res_1080,
            self.ui.radioButton_Media_Video_Res_2160,
            self.ui.radioButton_Media_Video_Res_720
        ]
        self.btngroup_res = QButtonGroup()
        # A-3-Scan Mode:
        self.radiobtns_scanmode = [
            self.ui.radioButton_Media_Video_ScanMode_Interlaced,
            self.ui.radioButton_Media_Video_ScanMode_Progressive
        ]
        self.btngroup_scanmode = QButtonGroup()
        # A-4-Frame Rate:
        self.radiobtns_framerate = [
            self.ui.radioButton_Media_Video_FrameRate_Upper,
            self.ui.radioButton_Media_Video_FrameRate_Lower
        ]
        self.btngroup_framerate = QButtonGroup()
        # A-5-Direction:
        self.radiobtns_direction = [
            self.ui.radioButton_Channel_Direction_Send,
            self.ui.radioButton_Channel_Direction_Recv
        ]
        self.btngroup_direction = QButtonGroup()
        # A-6-TCS:
        self.radiobtns_tcs = [
            self.ui.radioButton_Media_Video_TCS_SDR,
            self.ui.radioButton_Media_Video_TCS_HLG,
            self.ui.radioButton_Media_Video_TCS_PQ
        ]
        self.btngroup_tcs = QButtonGroup()
        # A-7-Sampling:
        self.radiobtns_sampling = [
            self.ui.radioButton_Media_Video_Sampling_422,
            self.ui.radioButton_Media_Video_Sampling_420
        ]
        self.btngroup_sampling = QButtonGroup()
        # A-8-Depth:
        self.radiobtns_depth = [
            self.ui.radioButton_Media_Video_Depth_8bit,
            self.ui.radioButton_Media_Video_Depth_10bit
        ]
        self.btngroup_depth = QButtonGroup()
        # A-9-Colorimetry:
        self.radiobtns_colorimetry = [
            self.ui.radioButton_Media_Video_Colorimetry_BT709,
            self.ui.radioButton_Media_Video_Colorimetry_BT2020
        ]
        self.btngroup_colorimetry = QButtonGroup()
        # A-10-Packing Mode:
        """self.radiobtns_pm = [
            self.ui.radioButton_Media_Video_PM_GPM,
            self.ui.radioButton_Media_Video_PM_BPM
        ]
        """
        self.btngroup_pm = QButtonGroup()
        # A-11-Channel Role:
        self.radiobtns_chnrole = [
            self.ui.radioButton_Channel_Role_Main,
            self.ui.radioButton_Channel_Role_Backup
        ]
        self.btngroup_chnrole = QButtonGroup()
        # A-12-Tap Channel:
        self.radiobtns_tapchn = [
            self.ui.radioButton_Tap_Channel_A,
            self.ui.radioButton_Tap_Channel_B
        ]
        self.btngroup_tapchn = QButtonGroup()

        # B-0-Slot for buttons
        def slot_pushButton_ParsrOMDB_Clicked():
            parseOMDB()

        def slot_pushButton_GenSDP_Clicked():
            configSDP()

        def slot_pushButton_SavetoFile_Clicked():
            savetoFile()

        # B-x-Radio Button GROUP - Slot for clicked
        # B-1-Dir Model:
        def slot_radiobtn_clicked_dirmodel():
            global str_media_video_fmtp_value_tp
            str_media_video_fmtp_value_tp = "2110TPW;" if self.btngroup_dirmodel.checkedId() else "2110TPN;"

        # B-2-Resolution
        def slot_radiobtn_clicked_res():
            global str_media_video_fmtp_value_width
            global str_media_video_fmtp_value_height
            if self.btngroup_res.checkedId() == 0:
                str_media_video_fmtp_value_width = "1920;"
                str_media_video_fmtp_value_height = "1080;"
                self.ui.radioButton_Media_Video_ScanMode_Interlaced.setEnabled(True)
                self.ui.radioButton_Media_Video_ScanMode_Progressive.setEnabled(True)
                slot_radiobtn_clicked_scanmode()
                slot_radiobtn_clicked_framerate()
            elif self.btngroup_res.checkedId() == 1:
                str_media_video_fmtp_value_width = "3840;"
                str_media_video_fmtp_value_height = "2160;"
                self.ui.radioButton_Media_Video_ScanMode_Interlaced.setDisabled(True)
                self.ui.radioButton_Media_Video_ScanMode_Progressive.setEnabled(True)
                self.ui.radioButton_Media_Video_ScanMode_Progressive.setChecked(True)
                self.ui.radioButton_Media_Video_FrameRate_Upper.setText("50")
                self.ui.radioButton_Media_Video_FrameRate_Lower.setText("59.94")
                slot_radiobtn_clicked_scanmode()
                slot_radiobtn_clicked_framerate()
            elif self.btngroup_res.checkedId() == 2:
                str_media_video_fmtp_value_width = "1280;"
                str_media_video_fmtp_value_height = "720;"
                self.ui.radioButton_Media_Video_ScanMode_Interlaced.setDisabled(True)
                self.ui.radioButton_Media_Video_ScanMode_Progressive.setEnabled(True)
                self.ui.radioButton_Media_Video_ScanMode_Progressive.setChecked(True)
                self.ui.radioButton_Media_Video_FrameRate_Upper.setText("50")
                self.ui.radioButton_Media_Video_FrameRate_Lower.setText("59.94")
                slot_radiobtn_clicked_scanmode()
                slot_radiobtn_clicked_framerate()

        # B-3-Scan Mode
        def slot_radiobtn_clicked_scanmode():
            global str_media_video_fmtp_value_interlace
            if self.btngroup_scanmode.checkedId() == 0:
                str_media_video_fmtp_value_interlace = "interlace; "
                self.ui.radioButton_Media_Video_FrameRate_Upper.setText("25")
                self.ui.radioButton_Media_Video_FrameRate_Lower.setText("29.97")
                slot_radiobtn_clicked_framerate()
            else:
                str_media_video_fmtp_value_interlace = ""
                self.ui.radioButton_Media_Video_FrameRate_Upper.setText("50")
                self.ui.radioButton_Media_Video_FrameRate_Lower.setText("59.94")
                slot_radiobtn_clicked_framerate()

        # B-4-FrameRate
        def slot_radiobtn_clicked_framerate():
            global str_media_video_fmtp_value_exactframerate
            if self.btngroup_scanmode.checkedId() == 0:
                if self.btngroup_framerate.checkedId() == 0:
                    str_media_video_fmtp_value_exactframerate = "25;"
                else:
                    str_media_video_fmtp_value_exactframerate = "30000/1001;"
            else:
                if self.btngroup_framerate.checkedId() == 0:
                    str_media_video_fmtp_value_exactframerate = "50;"
                else:
                    str_media_video_fmtp_value_exactframerate = "60000/1001;"

        # B-5-TCS:
        def slot_radiobtn_clicked_tcs():
            global str_media_video_fmtp_value_tcs
            if self.btngroup_tcs.checkedId() == 0:
                str_media_video_fmtp_value_tcs = "SDR;"
            elif self.btngroup_tcs.checkedId() == 1:
                str_media_video_fmtp_value_tcs = "HLG;"
            elif self.btngroup_tcs.checkedId() == 2:
                str_media_video_fmtp_value_tcs = "PQ;"

        # B-6-sampling:
        def slot_radiobtn_clicked_sampling():
            global str_media_video_fmtp_value_sampling
            if self.btngroup_sampling.checkedId() == 0:
                str_media_video_fmtp_value_sampling = "YCbCr-4:2:2;"
            elif self.btngroup_sampling.checkedId() == 1:
                str_media_video_fmtp_value_sampling = "YCbCr-4:2:0;"

        # B-7-depth:
        def slot_radiobtn_clicked_depth():
            global str_media_video_fmtp_value_depth
            if self.btngroup_depth.checkedId() == 0:
                str_media_video_fmtp_value_depth = "8;"
            elif self.btngroup_depth.checkedId() == 1:
                str_media_video_fmtp_value_depth = "10;"

        # B-8-colorimetry:
        def slot_radiobtn_clicked_colorimetry():
            global str_media_video_fmtp_value_colorimetry
            if self.btngroup_colorimetry.checkedId() == 0:
                str_media_video_fmtp_value_colorimetry = "BT709;"
            elif self.btngroup_depth.checkedId() == 1:
                str_media_video_fmtp_value_colorimetry = "BT2020;"

        # B-9-Packing Mode:
        """def slot_radiobtn_clicked_pm():
            global str_media_video_fmtp_value_pm
            if self.btngroup_pm.checkedId() == 0:
                str_media_video_fmtp_value_pm = "2110GPM;"
            elif self.btngroup_depth.checkedId() == 1:
                str_media_video_fmtp_value_pm = "2110BPM;"
        """

        # B-10-Channel Role:
        def slot_radiobtn_clicked_chnrole():
            global str_channel_role
            global str_channel_role_short
            if self.btngroup_chnrole.checkedId() == 0:
                str_channel_role = "Main"
                str_channel_role_short = "M"
                self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.ip_byte3.setText("120")
                self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.ip_byte3.setText("120")
                self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.ip_byte3.setText("130")
                self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.ip_byte3.setText("130")
                self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.ip_byte3.setText("140")
                self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.ip_byte3.setText("140")

            elif self.btngroup_chnrole.checkedId() == 1:
                str_channel_role = "Backup"
                str_channel_role_short = "B"
                self.ui.ip4Edit_Media_Video_First_Dest_Mcast_Addr.ip_byte3.setText("220")
                self.ui.ip4Edit_Media_Video_Second_Dest_Mcast_Addr.ip_byte3.setText("220")
                self.ui.ip4Edit_Media_Audio_First_Dest_Mcast_Addr.ip_byte3.setText("230")
                self.ui.ip4Edit_Media_Audio_Second_Dest_Mcast_Addr.ip_byte3.setText("230")
                self.ui.ip4Edit_Media_ANC_First_Dest_Mcast_Addr.ip_byte3.setText("240")
                self.ui.ip4Edit_Media_ANC_Second_Dest_Mcast_Addr.ip_byte3.setText("240")

        # B-11-Tap Channel:
        def slot_radiobtn_clicked_tapchn():
            global str_tap_channel
            if self.btngroup_tapchn.checkedId() == 0:
                str_tap_channel = "A"
            elif self.btngroup_tapchn.checkedId() == 1:
                str_tap_channel = "B"

        # B-12-Direction:
        def slot_radiobtn_clicked_direction():
            global str_media_direction
            global str_media_direction_for_sess_name
            global str_lable_direction
            global str_filename_prefix_direction
            if self.btngroup_direction.checkedId() == 0:
                str_media_direction = \
                    DEFINE_SDPTYPE_SESS_ATTR + \
                    DEFINE_SDPVALUE_MEDIA_DIRECTION_SENDONLY
                str_media_direction_for_sess_name = "output from "
                str_lable_direction = DEFINE_LABEL_DIRECTION_SEND
                str_filename_prefix_direction = DEFINE_FILENAME_PREFIX_SEND
            elif self.btngroup_direction.checkedId() == 1:
                str_media_direction = \
                    DEFINE_SDPTYPE_SESS_ATTR + \
                    DEFINE_SDPVALUE_MEDIA_DIRECTION_RECVONLY
                str_media_direction_for_sess_name = "input to "
                str_lable_direction = DEFINE_LABEL_DIRECTION_RECV
                str_filename_prefix_direction = DEFINE_FILENAME_PREFIX_RECV

            self.ui.label_Media_Video_First_Dest.setText("First " + str_lable_direction)
            self.ui.label_Media_Audio_First_Dest.setText("First " + str_lable_direction)
            self.ui.label_Media_ANC_First_Dest.setText("First " + str_lable_direction)
            self.ui.label_Media_Video_Second_Dest.setText("Second " + str_lable_direction)
            self.ui.label_Media_Audio_Second_Dest.setText("Second " + str_lable_direction)
            self.ui.label_Media_ANC_Second_Dest.setText("Second " + str_lable_direction)

        # B-13-Slots for (audio) combobox on index change
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
        # C-2-Resolution:
        for i in range(len(self.radiobtns_res)):
            self.btngroup_res.addButton(self.radiobtns_res[i], i)
            self.radiobtns_res[i].clicked.connect(slot_radiobtn_clicked_res)
        # C-3-Scan Mode:
        for i in range(len(self.radiobtns_scanmode)):
            self.btngroup_scanmode.addButton(self.radiobtns_scanmode[i], i)
            self.radiobtns_scanmode[i].clicked.connect(slot_radiobtn_clicked_scanmode)
        # C-4-Frame Rate:
        for i in range(len(self.radiobtns_framerate)):
            self.btngroup_framerate.addButton(self.radiobtns_framerate[i], i)
            self.radiobtns_framerate[i].clicked.connect(slot_radiobtn_clicked_framerate)
        # C-5-TCS:
        for i in range(len(self.radiobtns_tcs)):
            self.btngroup_tcs.addButton(self.radiobtns_tcs[i], i)
            self.radiobtns_tcs[i].clicked.connect(slot_radiobtn_clicked_tcs)
        # C-6-Sampling:
        for i in range(len(self.radiobtns_sampling)):
            self.btngroup_sampling.addButton(self.radiobtns_sampling[i], i)
            self.radiobtns_sampling[i].clicked.connect(slot_radiobtn_clicked_sampling)
        # C-7-Depth:
        for i in range(len(self.radiobtns_depth)):
            self.btngroup_depth.addButton(self.radiobtns_depth[i], i)
            self.radiobtns_depth[i].clicked.connect(slot_radiobtn_clicked_depth)
        # C-8-Colorimetry:
        for i in range(len(self.radiobtns_colorimetry)):
            self.btngroup_colorimetry.addButton(self.radiobtns_colorimetry[i], i)
            self.radiobtns_colorimetry[i].clicked.connect(slot_radiobtn_clicked_colorimetry)
        # C-9-Packing Mode:
        """for i in range(len(self.radiobtns_pm)):
            self.btngroup_pm.addButton(self.radiobtns_pm[i], i)
            self.radiobtns_pm[i].clicked.connect(slot_radiobtn_clicked_pm)
        """
        # C-10-Channel Role:
        for i in range(len(self.radiobtns_chnrole)):
            self.btngroup_chnrole.addButton(self.radiobtns_chnrole[i], i)
            self.radiobtns_chnrole[i].clicked.connect(slot_radiobtn_clicked_chnrole)
        # C-11-Tap Channel:
        for i in range(len(self.radiobtns_tapchn)):
            self.btngroup_tapchn.addButton(self.radiobtns_tapchn[i], i)
            self.radiobtns_tapchn[i].clicked.connect(slot_radiobtn_clicked_tapchn)
        # C-12-Direction:
        for i in range(len(self.radiobtns_direction)):
            self.btngroup_direction.addButton(self.radiobtns_direction[i], i)
            self.radiobtns_direction[i].clicked.connect(slot_radiobtn_clicked_direction)
        # C-13 single object
        self.ui.pushButton_ParseOMDB.clicked.connect(slot_pushButton_ParsrOMDB_Clicked)
        self.ui.pushButton_GenSDP.clicked.connect(slot_pushButton_GenSDP_Clicked)
        self.ui.pushButton_SavetoFile.clicked.connect(slot_pushButton_SavetoFile_Clicked)
        self.ui.checkBox_Sess_Generate_ID.clicked.connect(slot_checkBox_Sess_Generate_ID_Clicked)
        self.ui.checkBox_Media_DUP.clicked.connect(slot_checkBox_Media_DUP_Clicked)
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
        self.ui.lineEdit_Channel_ID.editingFinished.connect(slot_lineEdit_Channel_ID_Edited)
        self.ui.lineEdit_Channel_ID.textChanged.connect(slot_lineEdit_Channel_ID_Edited)
        self.ui.comboBox_Tap_ID.currentTextChanged.connect(slot_checkBox_Tap_ID_Edited)
        self.ui.comboBox_Tap_ID.editTextChanged.connect(slot_checkBox_Tap_ID_Edited)
        self.ui.comboBox_Tap_ID.currentIndexChanged.connect(slot_checkBox_Tap_ID_Edited)

        # D-init value for each radio button group
        slot_checkBox_Sess_Generate_ID_Clicked()
        slot_checkBox_Media_DUP_Clicked()
        slot_radiobtn_clicked_dirmodel()
        slot_radiobtn_clicked_res()
        slot_radiobtn_clicked_tcs()
        slot_radiobtn_clicked_sampling()
        slot_radiobtn_clicked_depth()
        slot_radiobtn_clicked_colorimetry()
        # slot_radiobtn_clicked_pm()
        slot_radiobtn_clicked_chnrole()
        slot_radiobtn_clicked_tapchn()
        slot_lineEdit_Channel_ID_Edited()
        slot_radiobtn_clicked_direction()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Main()
    if os.name == "posix":
        about_dlg = About()
        MainWindow.about_action.triggered.connect(about_dlg.show)
    MainWindow.show()
    sys.exit(app.exec_())
