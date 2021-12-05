#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    udpServer = new UdpServer(this);
    connect(udpServer, &UdpServer::showData, this, &MainWindow::showData);
}

void MainWindow::showData(QString data)
{
    ui->textEdit->append(data);
}

MainWindow::~MainWindow()
{
    delete ui;
}
