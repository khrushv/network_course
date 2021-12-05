#ifndef UDPSERVER_H
#define UDPSERVER_H

#include <QTextEdit>
#include <QUdpSocket>
#include <QTimer>
#include <QDateTime>
#include <QSet>

class UdpServer : public QWidget
{
Q_OBJECT

private:
    QUdpSocket* m_udpInSock;
    QUdpSocket* m_udpOutSock;
    int portIn;
    QSet<int> portOut;

public:
    UdpServer(QWidget* wgt = 0);
    void bindPortIn(int port);

signals:
    void showData(QString );

private slots:
    void slotProcessDatagram();
    void slotSendDatagram(QString data, QString name, int portFrom);

};

#endif // UDPSERVER_H
