#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    udpClient = new UdpClient(this);
    connect(udpClient, &UdpClient::showData, this, &MainWindow::showData);
}

void MainWindow::showData(QString data)
{
    ui->textEdit->append(data);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_sendButton_clicked()
{
    udpClient->slotSendDatagram(ui->lineEdit->text());
    ui->lineEdit->setText("");
}

void MainWindow::on_connectButton_clicked()
{
    if(ui->nameLineEdit->text() != "")
    {
        udpClient->setName(ui->nameLineEdit->text());
    }
    else
    {
        ui->errorLabel->setText("Не введено имя");
        return;
    }
    if(ui->nameLineEdit->text() != "")
    {
        try
        {
            QRegExp re("\\d*");
            if (re.exactMatch(ui->portLineEdit->text()))
            {
                udpClient->bindPortIn(ui->portLineEdit->text().toInt());
            }
            else
            {
                ui->errorLabel->setText("Порт содержит нечисленные значения");
                return;
            }
        }  catch (...)
        {
            ui->errorLabel->setText("Ошибка порта");
        }

    }
    else
    {
        ui->errorLabel->setText("Не введен порт");
        return;
    }
    ui->errorLabel->setText("");
    ui->sendButton->setEnabled(true);
    udpClient->sendHelloServer();
    ui->connectButton->setEnabled(false);
    ui->portLineEdit->setEnabled(false);
    ui->nameLineEdit->setEnabled(false);
    ui->disconnectButton->setEnabled(true);
    ui->sendButton->setEnabled(true);
}


void MainWindow::on_disconnectButton_clicked()
{
    ui->connectButton->setEnabled(true);
    ui->portLineEdit->setEnabled(true);
    ui->nameLineEdit->setEnabled(true);
    ui->sendButton->setEnabled(false);
    udpClient->disconnectPort();
}

