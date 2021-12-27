# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QWidget, QTableWidgetItem, QLineEdit
from PySide2.QtCore import QFile, QRegExp
from PySide2.QtUiTools import QUiLoader
import qdarktheme

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import poplib
import email

my_email = ""
my_password = ""


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "mainwidget.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        global my_email
        global my_password
        print(my_email)
        print(my_password)
        self.ui.errorLabel.setVisible(False)
        self.ui.sendButton.clicked.connect(
                               lambda: self.send_button_clicked())
        self.ui.reloadButton.clicked.connect(
                               lambda: self.reload_button_clicked())
        ui_file.close()

    def send_button_clicked(self):
        global my_email
        global my_password
        rx = QRegExp("[A-Za-z0-9._%+-]+[@][A-Za-z0-9.-]+[.][A-Za-z]{2,4}")
        if not rx.exactMatch(self.ui.sendToLineEdit.text()):
            self.ui.errorLabel.setVisible(True)
            return
        self.ui.errorLabel.setVisible(False)
        msg = MIMEMultipart()
        msg['From'] = my_email
        msg['To'] = self.ui.sendToLineEdit.text()
        msg['Subject'] = self.ui.subjectLineEdit.text()

        body = self.ui.textBrowser.toPlainText()
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(my_email, my_password)
        text = msg.as_string()
        server.sendmail(my_email, self.ui.sendToLineEdit.text(), text)
        server.quit()
        print("send_button_clicked")

    def reload_button_clicked(self):
        user = my_email
        Mailbox = poplib.POP3_SSL('pop.gmail.com', '995')
        Mailbox.user(user)
        Mailbox.pass_('sroo3be5DB')
        numMessages = len(Mailbox.list()[1])
        str_from = ""
        str_to = ""
        str_date = ""
        str_subject = ""
        oldRowCount = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount() + numMessages)
        for i in range(numMessages):
            for data in Mailbox.retr(i+1)[1]:
                msg = email.message_from_bytes(data)
                if msg.get("From") is not None:
                    str_from = msg.get("From")
                if msg.get("To") is not None:
                    str_to = msg.get("To")
                if msg.get("Date") is not None:
                    str_date = msg.get("Date")
                if msg.get("Subject") is not None:
                    str_subject = msg.get("Subject")
                self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(str_date))
                self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(str_from))
                self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(str_to))
                self.ui.tableWidget.setItem(i, 3, QTableWidgetItem(str_subject))
                oldRowCount += 1
        Mailbox.quit()
        print("reload_button_clicked")


class LoginWidget(QWidget):
    def __init__(self):
        super(LoginWidget, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "login.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        self.ui.errorLabel.setVisible(False)
        self.ui.lineEdit_2.setEchoMode(QLineEdit.Password);
        self.ui.pushButton.clicked.connect(
                               lambda: self.push_button_clicked())
        ui_file.close()

    def push_button_clicked(self):
        global my_email
        global my_password
        my_email = self.ui.lineEdit.text()
        my_password = self.ui.lineEdit_2.text()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        try:
            server.login(my_email, my_password)
        except:
            self.ui.errorLabel.setVisible(True)
            return
        self.ui.errorLabel.setVisible(False)
        server.quit()

        self.w = MainWidget()
        self.w.setWindowTitle("Email Client")
        self.w.setFixedSize(1024, 768)
        self.w.show()
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(qdarktheme.load_stylesheet())
    widget = LoginWidget()
    widget.setWindowTitle("Login Email Client")
    widget.setFixedSize(400, 250)
    widget.show()
    sys.exit(app.exec_())
