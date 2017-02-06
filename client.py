#!/usr/bin/python

import socket;
import os;
s = socket.socket();
s.connect((os.environ["IP"],8081))
print s.recv(1024)
print 'Received some data';
s.send('This is client 1');
s.close()
