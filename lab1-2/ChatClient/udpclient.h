#ifndef UDPCLIENT_H
#define UDPCLIENT_H

#include <QWidget>
#include <QUdpSocket>
#include <QDateTime>

class UdpClient : public QWidget
{
Q_OBJECT

private:
    QUdpSocket* m_udpInSock;
    QUdpSocket* m_udpOutSock;

    int portIn;
    int portOut;

    QString name;

public:
    UdpClient(QWidget* wgt = 0);
    void bindPortIn(int port);
    void sendHelloServer();
    void setName(QString name);
    void disconnectPort();
signals:
    void showData(QString);

public slots:
    void slotProcessDatagram();
    void slotSendDatagram(QString str);
};

#endif // UDPCLIENT_H
