#include "udpserver.h"
#include <QDebug>

UdpServer::UdpServer(QWidget* wgt) : QWidget(wgt)
{
    portIn = 90000;

    m_udpInSock = new QUdpSocket(this);
    m_udpOutSock = new QUdpSocket(this);

    bindPortIn(portIn);

    connect(m_udpInSock, &QUdpSocket::readyRead, this, &UdpServer::slotProcessDatagram);
}

void UdpServer::bindPortIn(int port)
{
    portIn = port;
    m_udpInSock->bind(QHostAddress::LocalHost, portIn);
}

void UdpServer::slotProcessDatagram()
{
    QString data;
    QString name;
    QByteArray baDatagram;
    int port;
    do
    {
        baDatagram.resize(m_udpInSock->pendingDatagramSize());
        m_udpInSock->readDatagram(baDatagram.data(), baDatagram.size());
    }
    while(m_udpInSock->hasPendingDatagrams());

    QDateTime dateTime;
    QDataStream in(&baDatagram, QIODevice::ReadOnly);
    in.setVersion(QDataStream::Qt_5_15);

    in >> dateTime >> data >> port >> name;

    QString str = "Received: " + name + " "  + dateTime.toString() + " " + data + " " + QString::number(port);
    portOut.insert(port);
    emit showData(str);
    slotSendDatagram(data, name, port);
}

void UdpServer::slotSendDatagram(QString data, QString name, int portFrom)
{
    QByteArray baDatagram;
    QDataStream out(&baDatagram, QIODevice::WriteOnly);
    out.setVersion(QDataStream::Qt_5_15);
    QDateTime dt = QDateTime::currentDateTime();
    QString str;

    for(int port : qAsConst(portOut))
    {
        if (port != portFrom)
        {
            str = "Send: " + name + " " + dt.toString() + " " + data + " " + QString::number(port);
            out << dt << data << name;
            m_udpOutSock->writeDatagram(baDatagram, QHostAddress::LocalHost, port);
            emit showData(str);
        }
    }
}
