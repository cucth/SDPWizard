from PyQt5.QtGui import QIntValidator, QValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QMargins, QRegExp
from PyQt5.QtWidgets import QLineEdit, QLabel, QWidget, QHBoxLayout


class IpByteEdit(QLineEdit):
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)

        self.nextTab = None
        self.setMaxLength(3)
        self.setFrame(False)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("font-family: Arial; font-size: 13px")

        validator = QIntValidator(0, 255, self)
        self.setValidator(validator)

        self.textEdited.connect(self.text_edited)

    def set_nextTabEdit(self, nextTab):
        self.nextTab = nextTab

    def focusInEvent(self, event):
        self.selectAll()
        super(IpByteEdit, self).focusInEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Period:
            if self.nextTab:
                self.nextTab.setFocus()
                self.nextTab.selectAll()
        super(IpByteEdit, self).keyPressEvent(event)

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

        self.ip_byte1 = IpByteEdit()
        self.ip_byte2 = IpByteEdit()
        self.ip_byte3 = IpByteEdit()
        self.ip_byte4 = IpByteEdit()
        self.ip_byte1.setAlignment(Qt.AlignRight)
        self.ip_byte2.setAlignment(Qt.AlignRight)
        self.ip_byte3.setAlignment(Qt.AlignRight)
        self.ip_byte4.setAlignment(Qt.AlignRight)

        self.labeldot1 = QLabel('.')
        self.labeldot2 = QLabel('.')
        self.labeldot3 = QLabel('.')
        self.labeldot1.setAlignment(Qt.AlignCenter)
        self.labeldot2.setAlignment(Qt.AlignCenter)
        self.labeldot3.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout()
        layout.addWidget(self.ip_byte1, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.labeldot1, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.ip_byte2, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.labeldot2, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.ip_byte3, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.labeldot3, stretch=0, alignment=Qt.Alignment())
        layout.addWidget(self.ip_byte4, stretch=0, alignment=Qt.Alignment())
        layout.setSpacing(0)
        layout.setContentsMargins(QMargins(2, 2, 2, 2))

        self.setLayout(layout)

        QWidget.setTabOrder(self.ip_byte1, self.ip_byte2)
        QWidget.setTabOrder(self.ip_byte2, self.ip_byte3)
        QWidget.setTabOrder(self.ip_byte3, self.ip_byte4)
        self.ip_byte1.set_nextTabEdit(self.ip_byte2)
        self.ip_byte2.set_nextTabEdit(self.ip_byte3)
        self.ip_byte3.set_nextTabEdit(self.ip_byte4)

        self.ip_byte1.textChanged.connect(self.textChangedSlot)
        self.ip_byte2.textChanged.connect(self.textChangedSlot)
        self.ip_byte3.textChanged.connect(self.textChangedSlot)
        self.ip_byte4.textChanged.connect(self.textChangedSlot)
        self.ip_byte1.textEdited.connect(self.textEditedSlot)
        self.ip_byte2.textEdited.connect(self.textEditedSlot)
        self.ip_byte3.textEdited.connect(self.textEditedSlot)
        self.ip_byte4.textEdited.connect(self.textEditedSlot)

    def textChangedSlot(self):
        ipbyte1 = self.ip_byte1.text()
        ipbyte2 = self.ip_byte2.text()
        ipbyte3 = self.ip_byte3.text()
        ipbyte4 = self.ip_byte4.text()
        ipaddr = "{}.{}.{}.{}".format(ipbyte1, ipbyte2, ipbyte3, ipbyte4)
        self.textChanged.emit(ipaddr)

    def textEditedSlot(self):
        ipbyte1 = self.ip_byte1.text()
        ipbyte2 = self.ip_byte2.text()
        ipbyte3 = self.ip_byte3.text()
        ipbyte4 = self.ip_byte4.text()
        ipaddr = "{}.{}.{}.{}".format(ipbyte1, ipbyte2, ipbyte3, ipbyte4)
        self.textEdited.emit(ipaddr)

    def setText(self, text):
        regexp = QRegExp('^((2[0-4]\\d|25[0-5]|[01]?\\d\\d?).){3}(2[0-4]\\d||25[0-5]|[01]?\\d\\d?)$')
        validator = QRegExpValidator(regexp, self)
        npos = 0
        state = validator.validate(text, npos)[0]
        ipbyte1 = ""
        ipbyte2 = ""
        ipbyte3 = ""
        ipbyte4 = ""

        if state == QValidator.Acceptable:  # valid
            ipbytelist = text.split('.')

            strcount = len(ipbytelist)
            index = 0
            if index < strcount:
                ipbyte1 = ipbytelist[index]
            index += 1
            if index < strcount:
                ipbyte2 = ipbytelist[index]
                index += 1
            if index < strcount:
                ipbyte3 = ipbytelist[index]
                index += 1
            if index < strcount:
                ipbyte4 = ipbytelist[index]

        self.ip_byte1.setText(ipbyte1)
        self.ip_byte2.setText(ipbyte2)
        self.ip_byte3.setText(ipbyte3)
        self.ip_byte4.setText(ipbyte4)

    def text(self):
        ipbyte1 = self.ip_byte1.text()
        ipbyte2 = self.ip_byte2.text()
        ipbyte3 = self.ip_byte3.text()
        ipbyte4 = self.ip_byte4.text()

        return "{}.{}.{}.{}".format(ipbyte1, ipbyte2, ipbyte3, ipbyte4)

    def setStyleSheet(self, styleSheet):
        self.ip_byte1.setStyleSheet(styleSheet)
        self.ip_byte2.setStyleSheet(styleSheet)
        self.ip_byte3.setStyleSheet(styleSheet)
        self.ip_byte4.setStyleSheet(styleSheet)
