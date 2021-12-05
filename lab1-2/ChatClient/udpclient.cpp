#include "udpclient.h"
#include <QDebug>

UdpClient::UdpClient(QWidget* wgt) : QWidget(wgt)
{
    portIn = 55;
    portOut = 90000;
    m_udpInSock = new QUdpSocket(this);
    m_udpOutSock = new QUdpSocket(this);

    connect(m_udpInSock, &QUdpSocket::readyRead, this, &UdpClient::slotProcessDatagram);
}

void UdpClient::bindPortIn(int port)
{
    portIn = port;
    m_udpInSock->bind(QHostAddress::LocalHost, portIn);
}

void UdpClient::sendHelloServer()
{
    slotSendDatagram("Hello server");
}

void UdpClient::setName(QString name)
{
    this->name = name;
}

void UdpClient::slotProcessDatagram()
{
    QString data;
    QString senderName;
    QByteArray baDatagram;

    do
    {
        baDatagram.resize(m_udpInSock->pendingDatagramSize());
        m_udpInSock->readDatagram(baDatagram.data(), baDatagram.size());
    }
    while(m_udpInSock->hasPendingDatagrams());

    QDateTime dateTime;
    QDataStream in(&baDatagram, QIODevice::ReadOnly);
    in.setVersion(QDataStream::Qt_5_15);
    in >> dateTime >> data >> senderName;
    QString str = senderName + " " + dateTime.toString() + " " + data;
    emit showData(str);
}

void UdpClient::slotSendDatagram(QString data)
{
    QByteArray baDatagram;
    QDataStream out(&baDatagram, QIODevice::WriteOnly);
    out.setVersion(QDataStream::Qt_5_15);
    QDateTime dt = QDateTime::currentDateTime();
    out << dt << data << portIn << this->name;
    QString str = this->name + " " + dt.toString()  + " " + data + " ";
    m_udpOutSock->writeDatagram(baDatagram, QHostAddress::LocalHost, portOut);


    emit showData(str);
}

void UdpClient::disconnectPort()
{
    m_udpInSock->disconnectFromHost();
    m_udpOutSock->disconnectFromHost();
}
