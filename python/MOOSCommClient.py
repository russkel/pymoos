import ctypes
import socket
from time import sleep, time
from threading import Thread, RLock

from pymoos.XPCTcpSocket import *
from pymoos.CMOOSMsg import *
from pymoos.CMOOSCommObject import *
from pymoos.CMOOSCommPkt import *


def MOOSTime():
    # MOOSLocalTime is not available in pyMOOS (yet)
    # but it exists inside CMOOSMsg !
    # msg = MOOSMsg()
    # return msg.GetTime()
    return time()


class MOOSCommClient(Thread):
    def __init__(self):
        super(Thread, self).__init__()
        Thread.__init__(self)

        # Define the wire protocol
        self.protocol = "ELKS CAN'T DANCE 2/8/10".encode("utf-8")

        self.bConnected = False
        self.m_bQuit = False
        self.host = "localhost"
        self.port = 9000
        self.m_sMyName = "pythonApp"

        self.m_Outbox = []
        self.m_Inbox = []

        self.onConnectCallBack = None
        self.onMailCallBack = None

        self.sock = XPCTcpSocket(self.port)
        self.comms = MOOSCommObject()

        self.m_Outbox_Lock = RLock()
        self.m_Inbox_Lock = RLock()

    def Close(self):
        "Notify thread about closing connection"
        self.m_bQuit = True
        self.join()

    def Notify(self, variable, value, time=-1):
        "Add a message to the outbox"

        Msg = MOOSMsg("N", variable, value, time)

        if self.__Post(Msg):
            return True
        else:
            return False

    def Register(self, variable, interval=0):
        """
        Register with the DB for some variable
        interval is the minimum time between notifications
        """
        if not variable:
            return False

        time = -1
        MsgR = MOOSMsg("R", variable, interval, time)

        if self.__Post(MsgR):
            return True
        else:
            return False

    def UnRegister(self, variable):
        "De-Register with the DB for some variable"
        print("UnRegister")

    def IsConnected(self):
        return self.bConnected

    def SetCommsTick(self, nCommTick):
        self.mFundamentalFrequency = min(nCommTick, MAX_TICK)
        return

    def Fetch(self):
        "Called by client to retrieve non-null MOOS Messages"
        with self.m_Inbox_Lock:
            data = self.m_Inbox
            self.m_Inbox = []
        return data

    def FetchRecentMail(self):
        """
        Filter messages in the inbox to remove old messages.
        Uses the MOOSMsg.IsSkewed method to detect old messages
        """
        messages = self.Fetch()

        current_time = MOOSTime()
        # print "current_time", current_time

        filtered_messages = [
            m for m in messages if m.IsSkewed(current_time, None) == False
        ]

        return filtered_messages

    def Run(self, host, port, myName, fundamentalFreq=5):
        """
        Entry point for the MOOS exchange
        fundamentalFreq is in [Hz]
        """
        self.host = host
        self.port = port
        self.sock = XPCTcpSocket(self.port)
        self.m_sMyName = myName
        self.mFundamentalFrequency = fundamentalFreq
        self.daemon = True
        self.start()

        return True

    def SetOnConnectCallBack(self, fn):
        self.onConnectCallBack = fn
        return True

    def SetOnDisconnectCallBack(self, fn):
        self.onDisconnectCallBack = fn
        return True

    def SetOnMailCallBack(self, fn):
        self.onMailCallBack = fn
        return True

    def PeekMail(self, MOOSMSG_LIST, Key, erase=False, findYoungest=False):

        for message in self.m_Inbox:
            if message.m_sKey == Key:
                return message

        return None

    def ServerRequest(self, sWhat, timout=-1, bClear=False):
        raise NotImplementedError

    def Peek(self, MOOSMSG_LIST, Key, erase=True):
        raise NotImplementedError

    def GetLocalIPAddress(self):
        # ip = socket.gethostbyaddr( socket.gethostname() )
        # return ip[2] # returns '::1' on rodrigob's machine
        return socket.gethostname()

    def run(self):
        """
        Threading entry point.
        This method is launched when Thread.start() is called
        """
        self.__ClientLoop()
        return True

    def __ClientLoop(self):

        while not self.m_bQuit:

            if self.__ConnectToServer():
                self.bConnected = True

                while not self.m_bQuit:
                    sleep(1.0 / self.mFundamentalFrequency)

                    if not self.__DoClientWork():
                        # something went wrong, we have lost the connection
                        self.bConnected = False
                        break

            else:
                print("Unable to connect to %s" % self.host)
                sleep(1)
        return

    def __ConnectToServer(self):
        if self.IsConnected():
            print("Already connected")
            return True

        self.sock.vConnect(self.host)

        if self.__HandShake():
            return True

    def __DoClientWork(self):
        "Main I/O loop"

        PktTx = CMOOSCommPkt()
        PktRx = CMOOSCommPkt()

        with self.m_Outbox_Lock:
            if not self.m_Outbox:
                "Send a message to tick things over"
                msg = MOOSMsg()
                msg.m_sSrc = self.m_sMyName
                self.m_Outbox.append(msg)

            try:
                PktTx.Serialize(self.m_Outbox, True, True, None)
            except:
                return False
            # Clear the outbox
            self.m_Outbox = []
        # release self.m_Outbox_Lock

        # Get the local time
        # dfLocalPktTxTime = MOOSLocalTime()

        sent_value = None
        try:
            sent_value = self.comms.SendPkt(self.sock, PktTx)
        except RuntimeError as e:
            print("SendPkt raised a RuntimeError", e)

        if not sent_value:
            print("Send error")
            return False

        read_value = None
        try:
            read_value = self.comms.ReadPkt(self.sock, PktRx, -1)
        except RuntimeError as e:
            print("ReadPkt raised a RuntimeError", e)

        if not read_value:
            print("Receive error")
            return False

        # dfLocalPktRxTime = MOOSLocalTime()
        # PktRx.Serialize( m_Inbox, false, true, dfServerPktTxTime )
        with self.m_Inbox_Lock:
            PktRx.Serialize(self.m_Inbox, False, True, None)

            if self.onMailCallBack and self.m_Inbox:
                try:
                    self.onMailCallBack()
                except:
                    print("Unable to evaluate user-specified onMailCallBack")
                    raise

        # release self.m_Inbox_Lock

        return True

    def __HandShake(self):
        # Send the wire protocol
        c = ctypes.c_char_p(self.protocol)
        v = ctypes.cast(c, ctypes.c_void_p)

        self.sock.SendMessage(v.value, 32)

        Msg = MOOSMsg("D", "", self.m_sMyName, 1.0)
        self.comms.SendMsg(self.sock, Msg)

        WelcomeMsg = MOOSMsg()
        self.comms.ReadMsg(self.sock, WelcomeMsg)

        if WelcomeMsg.IsType("K"):
            print("Client was poisioned")
            return False

        self.skew = WelcomeMsg.m_dfVal

        # Invoke onconnect callback
        if self.onConnectCallBack:
            try:
                self.onConnectCallBack()
            except:
                print("Unable to evaluate user-specified onConnectCallBack")

        return True

    def Post(self, message):
        return self.__Post(message)

    def __Post(self, message):
        "Called by client to send a message to the MOOS DB"

        try:
            message.m_sSrc = self.m_sMyName

            with self.m_Outbox_Lock:
                self.m_Outbox.append(message)

            return True
        except:
            return False
