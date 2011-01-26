#!/usr/bin/env python
"""
Connection Test

First test to make sure all adapters can connect and disconnect properly
"""

import nose
import pika
import pika.adapters as adapters

from pika.adapters.tornado_connection import TornadoConnection

connected = False  # Global connected flag, resets in each test

HOST = 'localhost'
PORT = 5672

@nose.tools.timed(2)
def test_asyncore_connection():
    connection = connect(adapters.AsyncoreConnection)
    connection.ioloop.start()
    if not connected:
        assert False
    else:
        pass

@nose.tools.timed(2)
def test_select_epoll_connection():
    set_select_poller('epoll')
    connection = connect(adapters.SelectConnection)
    connection.ioloop.start()
    if connection.ioloop.get_poller_type() != 'EpollPoller':
        assert False
    if not is_connected():
        assert False
    pass


@nose.tools.timed(2)
def test_select_poll_connection():
    set_select_poller('poll')
    connection = connect(adapters.SelectConnection)
    connection.ioloop.start()
    if connection.ioloop.get_poller_type() != 'PollPoller':
        assert False
    if not is_connected():
        assert False
    pass


@nose.tools.timed(2)
def test_select_select_connection():
    set_select_poller('select')
    connection = connect(adapters.SelectConnection)
    connection.ioloop.start()
    if connection.ioloop.get_poller_type() != 'SelectPoller':
        assert False
    if not is_connected():
        assert False
    pass

@nose.tools.timed(2)
def test_select_kqueue_connection():
    global connected
    set_select_poller('kqueue')
    connection = connect(adapters.SelectConnection)
    connection.ioloop.start()
    if connection.ioloop.get_poller_type() != 'KQueuePoller':
        assert False
    if not is_connected():
        assert False
    pass

@nose.tools.timed(2)
def test_select_tornado_connection():
    connection = connect(TornadoConnection)
    connection.ioloop.start()
    if not is_connected():
        assert False
    else:
        pass

@nose.tools.nottest
def connect(connection_type):
    global connected
    connected = False
    parameters = pika.ConnectionParameters(HOST, PORT)
    return connection_type(parameters, on_connected)

@nose.tools.nottest
def set_select_poller(type):
    adapters.select_connection.SELECT_TYPE = type

@nose.tools.nottest
def is_connected():
    global connected
    return connected

@nose.tools.nottest
def on_connected(connection):
    global connected
    connected = connection.is_open()
    connection.ioloop.stop()

if __name__ == '__main__':

    test_select_kqueue_connection()
