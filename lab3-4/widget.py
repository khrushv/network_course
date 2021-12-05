# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import socket
from scapy.all import sniff, IP, TCP, UDP, Raw, ICMP, sr
import datetime
import threading
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtWidgets import QTreeWidgetItem, QMessageBox
from PySide2.QtCore import QFile, QRegExp
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QRegExpValidator
import qdarktheme


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()

    def _sniff(self, e):
        sniff(prn=self.network_sniff,
              filter="host " + socket.gethostbyname(socket.gethostname()),
              stop_filter=lambda p: e.is_set())

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.ui.StartButton.setEnabled(True)
        self.ui.StopButton.setEnabled(False)
        self.ui.packetList.setColumnCount(3)
        self.ui.packetList.setHeaderLabels(["Protocol", "Params", "Datetime"])
        ipRegex = QRegExp("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.)"
                          "{3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        ipValidator = QRegExpValidator(ipRegex)
        self.ui.SendFromLineEdit.setValidator(ipValidator)
        self.ui.SendFromLineEdit.setText("8.8.8.8")
        self.ui.StartButton.clicked.connect(
                               lambda: self.start_button_clicked())
        self.ui.StopButton.clicked.connect(
                               lambda: self.stop_button_clicked())
        self.ui.ClearButton.clicked.connect(
                               lambda: self.clear_button_clicked())
        self.ui.SendButton.clicked.connect(
                               lambda: self.send_button_clicked())

    def start_button_clicked(self):
        if (self.ui.IP.isChecked() or self.ui.UDP.isChecked() or
                self.ui.TCP.isChecked() or self.ui.ICMP.isChecked()):
            self.ui.StartButton.setEnabled(False)
            self.ui.StopButton.setEnabled(True)
            self.x = {}
            self.x['TCP'] = self.ui.TCP.isChecked()
            self.x['UDP'] = self.ui.UDP.isChecked()
            self.x['IP'] = self.ui.IP.isChecked()
            self.x['ICMP'] = self.ui.ICMP.isChecked()
            self.ui.TCP.setEnabled(False)
            self.ui.UDP.setEnabled(False)
            self.ui.IP.setEnabled(False)
            self.ui.ICMP.setEnabled(False)
            self.e = threading.Event()
            t = threading.Thread(target=self._sniff, args=(self.e,))
            t.start()
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error!")
            msgBox.setText("Choose one or more protocol!")
            msgBox.exec()

    def stop_button_clicked(self):
        self.e.set()
        self.ui.StartButton.setEnabled(True)
        self.ui.StopButton.setEnabled(False)
        self.ui.TCP.setEnabled(True)
        self.ui.UDP.setEnabled(True)
        self.ui.IP.setEnabled(True)
        self.ui.ICMP.setEnabled(True)

    def clear_button_clicked(self):
        self.ui.packetList.clear()

    def send_button_clicked(self):
        ipRegex = QRegExp("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.)"
                          "{3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        if ipRegex.exactMatch(self.ui.SendFromLineEdit.text()):
            sr(IP(dst=self.ui.SendFromLineEdit.text())/ICMP(),
               retry=0, timeout=5)
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error!")
            msgBox.setText("IP doesn't correct!")
            msgBox.exec()

    def network_sniff(self, pkt):
        time = datetime.datetime.now()
        # classifying packets into IP
        if pkt.haslayer(IP):
            if self.x["IP"]:
                self.get_IP_packet(pkt, time)

        # classifying packets into TCP
        if pkt.haslayer(TCP):
            if self.x["TCP"]:
                self.get_TCP_packet(pkt, time)

        # classifying packets into UDP
        if pkt.haslayer(UDP):
            if self.x["UDP"]:
                self.get_UDP_packet(pkt, time)

        # classifying packets into ICMP
        if pkt.haslayer(ICMP):
            if self.x["ICMP"]:
                self.get_ICMP_packet(pkt, time)

    def get_IP_packet(self, pkt, time):
        # classyfying packets into IP Incoming packets
        item = QTreeWidgetItem(["IP", "", str(time)])
        child = QTreeWidgetItem(["Version", str(pkt[IP].version)])
        item.addChild(child)
        child = QTreeWidgetItem(["Tos", str(pkt[IP].tos)])
        item.addChild(child)
        child = QTreeWidgetItem(["Tlen", str(pkt[IP].len)])
        item.addChild(child)
        child = QTreeWidgetItem(["Id", str(pkt[IP].id)])
        item.addChild(child)
        child = QTreeWidgetItem(["Flags", str(pkt[IP].flags)])
        item.addChild(child)
        child = QTreeWidgetItem(["TTL", str(pkt[IP].ttl)])
        item.addChild(child)
        proto_field = pkt[IP].get_field('proto')
        try:
            child = QTreeWidgetItem(["Proto",
                                    (proto_field.i2s[pkt[IP].proto])
                                    .upper()])
        except Exception:
            pass

        item.addChild(child)
        child = QTreeWidgetItem(["CRC", str(pkt[IP].chksum)])
        item.addChild(child)
        child = QTreeWidgetItem(["Src", str(pkt[IP].src)])
        item.addChild(child)
        child = QTreeWidgetItem(["Dst", str(pkt[IP].dst)])
        item.addChild(child)
        self.ui.packetList.insertTopLevelItem(0, item)

    def get_TCP_packet(self, pkt, time):
        # classyfying packets into TCP Incoming packets
        item = QTreeWidgetItem(["TCP", "", str(time)])
        child = QTreeWidgetItem(["Src",
                                 str(pkt[IP].src) + ":" + str(pkt[TCP].sport)])
        item.addChild(child)
        child = QTreeWidgetItem(["Dst",
                                 str(pkt[IP].dst) + ":" + str(pkt[TCP].dport)])
        item.addChild(child)

        child = QTreeWidgetItem(["Seq", str(pkt[TCP].seq)])
        item.addChild(child)
        child = QTreeWidgetItem(["Ackn", str(pkt[TCP].ack)])
        item.addChild(child)
        child = QTreeWidgetItem(["Offeset", str(pkt[TCP].dataofs)])
        item.addChild(child)
        child = QTreeWidgetItem(["Flags", str(pkt[TCP].flags)])
        item.addChild(child)
        child = QTreeWidgetItem(["Window", str(pkt[TCP].window)])
        item.addChild(child)
        child = QTreeWidgetItem(["CRC", str(pkt[TCP].chksum)])
        item.addChild(child)
        data = " "
        try:
            data = str(pkt.getlayer(Raw).load, "utf-8")
        except Exception:
            if (pkt.getlayer(Raw) and len(data) < 2):
                try:
                    data = str(pkt.getlayer(Raw).load)
                except Exception:
                    pass
        try:
            child = QTreeWidgetItem(["Data", data])
            item.addChild(child)
        except Exception:
            pass
        item.addChild(child)
        self.ui.packetList.insertTopLevelItem(0, item)

    def get_UDP_packet(self, pkt, time):
        # classyfying packets into UDP Incoming packets
        item = QTreeWidgetItem(["UDP", "", str(time)])
        child = QTreeWidgetItem(["Src",
                                 str(pkt[IP].src) + ":" + str(pkt[UDP].sport)])
        item.addChild(child)
        child = QTreeWidgetItem(["Dst",
                                 str(pkt[IP].dst) + ":" + str(pkt[UDP].dport)])
        item.addChild(child)
        child = QTreeWidgetItem(["Tlen", str(pkt[UDP].len)])
        item.addChild(child)
        child = QTreeWidgetItem(["CRC", str(pkt[UDP].chksum)])
        item.addChild(child)
        data = " "

        try:
            data = str(pkt.getlayer(Raw).load, "utf-8")
        except Exception:
            if (pkt.getlayer(Raw) and len(data) < 2):
                try:
                    data = str(pkt.getlayer(Raw).load)
                except Exception:
                    pass
        try:
            child = QTreeWidgetItem(["Data", data])
            item.addChild(child)
        except Exception:
            pass

        self.ui.packetList.insertTopLevelItem(0, item)

    def get_ICMP_packet(self, pkt, time):
        # classyfying packets into ICMP Incoming packets
        item = QTreeWidgetItem(["ICMP", "", str(time)])
        child = QTreeWidgetItem(["Type", str(pkt[ICMP].type)])
        item.addChild(child)
        child = QTreeWidgetItem(["Code", str(pkt[ICMP].code)])
        item.addChild(child)
        child = QTreeWidgetItem(["CRC", str(pkt[ICMP].chksum)])
        item.addChild(child)

        self.ui.packetList.insertTopLevelItem(0, item)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qdarktheme.load_stylesheet())
    widget = Widget()
    widget.setWindowTitle("Sniffer")
    widget.show()
    widget.setFixedSize(1024, 768)
    sys.exit(app.exec_())
