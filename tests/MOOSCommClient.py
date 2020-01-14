import sys
from time import time
from threading import Thread, RLock

import unittest

from pymoos import MOOSCommClient


class MOOSApp( MOOSCommClient ):
    "Test class for the MOOSCommClient class"

    def __init__(self):
        MOOSCommClient.__init__(self)

    def DoRegistrations( self ):
        self.Register( "counter", 0.0 )

    def MailCallback( self ):
        print("Received mail")
    

class ClientOne( MOOSCommClient ):
    "Test class for the TestMessagesExchanges test case"

    def __init__(self):
        MOOSCommClient.__init__(self)
        self.SetOnConnectCallBack( self.do_registrations )
        self.SetOnMailCallBack( self.mail_callback )
        self.number_of_received_messages = 0
        
        fundamental_frequency = 10 # [Hz]
        self.Run("localhost", 9000, self.__class__.__name__, fundamental_frequency)

        return

    def do_registrations(self):
        self.Register( "message_to_client_one")
        return
        
       
    def mail_callback(self):
        #print  self.__class__.__name__, " received mail"
        
        current_time = MOOSTime()        
        messages = self.FetchRecentMail()
        
        self.number_of_received_messages += len(messages)    

        #print_messages = True
        print_messages = False
        if print_messages:
            print(self.__class__.__name__, "received:")
            for message in messages:
                print(message.GetKey(), \
                    ":", message.GetString(), \
                    "\ndelta_time", current_time - message.GetTime(), \
                    "skewed", message.IsSkewed(current_time, None))
        
        return
        
    def wait_to_receive_message(self, timeout = 5):
        """
        timeout is in [seconds]
        """

        initial_time = time()
        
        while (time() - initial_time) < timeout:
            sleep(0.1)
            if self.number_of_received_messages > 0:
                print(self.__class__.__name__, \
                        "received %i messages" % self.number_of_received_messages)
                return True
            else:
                continue

        return False
        
class ClientTwo( ClientOne ):
    "Test class for the TestMessagesExchanges test case"

    def __init__(self):
        ClientOne.__init__(self)
        return

    def do_registrations(self):
        self.Register( "message_to_client_two")
        return
 
  
class TestMessagesExchanges(unittest.TestCase):
    
    def setUp(self):
        self.client_one = ClientOne()
        self.client_two = ClientTwo()
        
        self._wait_until_clients_are_connected()
        return

    def _wait_until_clients_are_connected(self):
        
        timeout_in_seconds = 5
        initial_time = time()
        print("\nConnecting the clients",)
        while (time() - initial_time) < timeout_in_seconds:
            sleep(0.1)
            print(".",); sys.stdout.flush()
            
            if self.client_one.IsConnected() and self.client_two.IsConnected():
                print("Connected")
                return True
            else:
                continue
        
        print("MOOS clients connection failed. Is MOOSDB running ?")
        raise Exception("Timeout waiting for clients one and two to connect")
        return
    
    def test_messages_exchanges(self):
        
        self._test_sending_and_not_receiving_messages()
        print("_test_sending_and_not_receiving_messages DONE")
        
        # we reset the counters
        self.client_one.number_of_received_messages = 0
        self.client_two.number_of_received_messages = 0

        self._test_sending_and_receiving_messages()
        print("_test_sending_and_receiving_messages DONE")
                
        return
    
    def _test_sending_and_receiving_messages(self):
        
        # client1 send messages
        self.client_one.Notify("message_to_client_two", "Hello client two !")
        
         # client2 should receive them
        received = self.client_two.wait_to_receive_message()
        self.assertTrue(received)
        
        # client2 send messages    
        self.client_two.Notify("message_to_client_one", "Hello client one !")
                
        # client1 should receive them
        received = self.client_one.wait_to_receive_message()
        self.assertTrue(received)

       
        return

    def _test_sending_and_not_receiving_messages(self):
        
        # client1 send messages
        self.client_one.Notify("message_to_client_two", "Hello client two !")
        
         # client2 should receive them
        received = self.client_two.wait_to_receive_message()
        self.assertTrue(received)
      
        # client1 should not have received any message
        timeout = 2 # [seconds]
        received = self.client_one.wait_to_receive_message(timeout)
        self.assertFalse(received)

        return


def mini_test():
    
    m = MOOSApp()
    m.SetOnConnectCallBack( m.DoRegistrations )
    m.SetOnMailCallBack( m.MailCallback )
    
    print("%s" % m.GetLocalIPAddress())

    fundamental_frequency = 10 # [Hz]
    m.Run( "127.0.0.1", 9000, "test_me", fundamental_frequency) 

    counter = 0

    while True:
        sleep(.01)
        messages = m.Fetch()

        m.Notify( "counter", counter )
        counter += 1

        for message in messages:
            print("Message trace:", message.Trace())
            print("Message key:", message.GetKey())
            print("Message time:", message.GetTime())
            
    return

if __name__ == "__main__":

    suite = unittest.TestLoader().loadTestsFromTestCase(TestMessagesExchanges)
    unittest.TextTestRunner(verbosity=3).run(suite)

    #mini_test()
