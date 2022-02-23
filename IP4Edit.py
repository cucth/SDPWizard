# 版权声明：本文为CSDN博主「softdzf」的原创文章，遵循CC
# 4.0
# BY - SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/softdzf/article/details/6624046

# Original code was implemented with Python2 + PyQt4.
# CSUN modified with Python3 + PyQt5 in Feb 2022

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class IpPartEdit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)

        self.nextTab = None
        self.setMaxLength(3)
        self.setFrame(False)
        self.setAlignment(Qt.AlignCenter)

        validator = QIntValidator(0, 255, self)
        self.setValidator(validator)

        self.textEdited.connect(self.text_edited)

    def set_nextTabEdit(self, nextTab):
        self.nextTab = nextTab

    def focusInEvent(self, event):
        self.selectAll()
        super(IpPartEdit, self).focusInEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Period:
            if self.nextTab:
                self.nextTab.setFocus()
                self.nextTab.selectAll()
        super(IpPartEdit, self).keyPressEvent(event)

    # @pyqtSlot(str)
    def text_edited(self, text: str):
        validator = QIntValidator(0, 255, self)
        ipaddr = text
        pos = 0
        state = validator.validate(ipaddr, pos)[0]
        if state == QValidator.Acceptable:
            if len(ipaddr) == 2:
                ipnum = int(ipaddr)
                if ipnum > 25:
                    if self.nextTab:
                        self.nextTab.setFocus()
                        self.nextTab.selectAll()
            elif len(ipaddr) == 3:
                if self.nextTab:
                    self.nextTab.setFocus()
                    self.nextTab.selectAll()
        else:
            self.setFocus()
            self.selectAll()


class Ip4Edit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        self.setFocusPolicy(Qt.NoFocus)

        self.ip_part1 = IpPartEdit()
        self.ip_part2 = IpPartEdit()
        self.ip_part3 = IpPartEdit()
        self.ip_part4 = IpPartEdit()
        self.ip_part1.setAlignment(Qt.AlignRight)
        self.ip_part2.setAlignment(Qt.AlignRight)
        self.ip_part3.setAlignment(Qt.AlignRight)
        self.ip_part4.setAlignment(Qt.AlignRight)

        self.labeldot1 = QLabel('.')
        self.labeldot2 = QLabel('.')
        self.labeldot3 = QLabel('.')
        self.labeldot1.setAlignment(Qt.AlignCenter)
        self.labeldot2.setAlignment(Qt.AlignCenter)
        self.labeldot3.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()
        layout.addWidget(self.ip_part1, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.labeldot1, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.ip_part2, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.labeldot2, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.ip_part3, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.labeldot3, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.ip_part4, stretch=0, alignment=Qt.Alignment())
        layout.setSpacing(0)
        layout.setContentsMargins(QMargins(2, 2, 2, 2))

        self.setLayout(layout)

        QWidget.setTabOrder(self.ip_part1, self.ip_part2)
        QWidget.setTabOrder(self.ip_part2, self.ip_part3)
        QWidget.setTabOrder(self.ip_part3, self.ip_part4)
        self.ip_part1.set_nextTabEdit(self.ip_part2)
        self.ip_part2.set_nextTabEdit(self.ip_part3)
        self.ip_part3.set_nextTabEdit(self.ip_part4)

        self.ip_part1.textChanged.connect(self.textChangedSlot)
        self.ip_part2.textChanged.connect(self.textChangedSlot)
        self.ip_part3.textChanged.connect(self.textChangedSlot)
        self.ip_part4.textChanged.connect(self.textChangedSlot)
        self.ip_part1.textEdited.connect(self.textEditedSlot)
        self.ip_part2.textEdited.connect(self.textEditedSlot)
        self.ip_part3.textEdited.connect(self.textEditedSlot)
        self.ip_part4.textEdited.connect(self.textEditedSlot)

    # @pyqtSlot('QString')
    def textChangedSlot(self):
        ippart1 = self.ip_part1.text()
        ippart2 = self.ip_part2.text()
        ippart3 = self.ip_part3.text()
        ippart4 = self.ip_part4.text()
        ipaddr = "{}.{}.{}.{}".format(ippart1, ippart2, ippart3, ippart4)
        self.textChanged.emit(ipaddr)

    # @pyqtSlot('QString')
    def textEditedSlot(self):
        ippart1 = self.ip_part1.text()
        ippart2 = self.ip_part2.text()
        ippart3 = self.ip_part3.text()
        ippart4 = self.ip_part4.text()
        ipaddr = "{}.{}.{}.{}".format(ippart1, ippart2, ippart3, ippart4)
        self.textEdited.emit(ipaddr)

    def setText(self, text):
        regexp = QRegExp('^((2[0-4]\\d|25[0-5]|[01]?\\d\\d?).){3}(2[0-4]\\d||25[0-5]|[01]?\\d\\d?)$')
        validator = QRegExpValidator(regexp, self)
        npos = 0
        state = validator.validate(text, npos)[0]
        ippart1 = ""
        ippart2 = ""
        ippart3 = ""
        ippart4 = ""

        if state == QValidator.Acceptable:  # valid
            ippartlist = text.split('.')

            strcount = len(ippartlist)
            index = 0
            if index < strcount:
                ippart1 = ippartlist[index]
            index += 1
            if index < strcount:
                ippart2 = ippartlist[index]
                index += 1
            if index < strcount:
                ippart3 = ippartlist[index]
                index += 1
            if index < strcount:
                ippart4 = ippartlist[index]

        self.ip_part1.setText(ippart1)
        self.ip_part2.setText(ippart2)
        self.ip_part3.setText(ippart3)
        self.ip_part4.setText(ippart4)

    def text(self):
        ippart1 = self.ip_part1.text()
        ippart2 = self.ip_part2.text()
        ippart3 = self.ip_part3.text()
        ippart4 = self.ip_part4.text()

        return "{}.{}.{}.{}".format(ippart1, ippart2, ippart3, ippart4)

    def setStyleSheet(self, styleSheet):
        self.ip_part1.setStyleSheet(styleSheet)
        self.ip_part2.setStyleSheet(styleSheet)
        self.ip_part3.setStyleSheet(styleSheet)
        self.ip_part4.setStyleSheet(styleSheet)
