from threading import Thread
import zmq
from queue import Queue
import logging

class BasicListener(Thread):
    ''' A convinience class to subscribe to a published data stream.
        datas are retrived by the `get_data()` method once the listener has been started by the
        `start()` method

        Args:
            ip (str):   The ip address where the datas are published (can be local or remote)
            port (int): The port number at which the datas are published
        Kwargs:
            logger:     Optionally provide a logger instance
    '''
    id_counter = 0
    def __init__(self,
                ip:str,
                port:int,
                unpack,
                logger:logging.Logger=None,
                ):
        Thread.__init__(self)
        BasicListener.id_counter += 1
        if(logger == None):
            self.log=logging.getLogger('ssdaq.BasicListener%d'%BasicListener.id_counter)
        else:
            self.log=logger

        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.SUB)
        self.sock.setsockopt(zmq.SUBSCRIBE, b"")
        con_str = "tcp://%s:%s"%(ip,port)
        if('0.0.0.0' == ip):
            self.sock.bind(con_str)
        else:
            self.sock.connect(con_str)
        self.log.info('Connected to : %s'%con_str)
        self.running = False
        self._data_buffer = Queue()

        self.id_counter =BasicListener.id_counter
        self.inproc_sock_name = "SSdataListener%d"%(self.id_counter)
        self.close_sock = self.context.socket(zmq.PAIR)
        self.close_sock.bind("inproc://"+self.inproc_sock_name)
        self.unpack = unpack

    def close(self):
        ''' Closes listener thread and empties the data buffer to unblock the
            the get_data method
        '''

        if(self.running):
            self.log.debug('Sending close message to listener thread')
            self.close_sock.send(b"close")
        self.log.debug('Emptying data buffer')
        #Empty the buffer after closing the recv thread
        while(not self._data_buffer.empty()):
            self._data_buffer.get()
            self._data_buffer.task_done()
        self._data_buffer.join()

    def get_data(self,**kwargs):
        ''' Returns an SSdata instance from the published data stream.
            By default a blocking call. See python Queue docs.

            Kwargs:
                See queue.Queue docs

        '''
        data = self._data_buffer.get(**kwargs)
        self._data_buffer.task_done()
        return data

    def run(self):
        ''' This is the main method of the listener
        '''
        self.log.info('Starting listener')
        recv_close = self.context.socket(zmq.PAIR)
        con_str = "inproc://"+self.inproc_sock_name
        recv_close.connect(con_str)
        self.running = True
        self.log.debug('Connecting close socket to %s'%con_str)
        poller = zmq.Poller()
        poller.register(self.sock,zmq.POLLIN)
        poller.register(recv_close,zmq.POLLIN)

        while(self.running):

            socks= dict(poller.poll())

            if(self.sock in socks):
                data = self.sock.recv()

                self._data_buffer.put(self.unpack(data))
            else:
                self.log.info('Stopping')
                self._data_buffer.put(None)
                break
        self.running = False