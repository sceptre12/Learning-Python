#!/usr/bin/python

import socket;
import os;
s = socket.socket();
import process;
s.connect((os.environ["IP"],os.environ["PORT"]))
print s.recv(1024)
print 'Received some data';
s.send('This is client 1');
s.close()
