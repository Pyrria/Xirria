#! /usr/bin/env python
import socket

class Proto():
    def __init__(self, address):
        self.buffer = ''
        self.cmds = {
            '\x03': self.on_x03,
            '\x25': self.on_x25,
            '\x0f': self.on_x0f
        }
        
        print(' * Connecting to %s' % address)
        self.stream = socket.socket()
        self.stream.connect((address, 7777))
        self.on_connect()
        self.loop()
        
    def loop(self):
        while True:
            self.buffer += self.stream.recv(1024)
            self.parse_buffer()
            
    def parse_buffer(self):
        '''Parse self.buffer'''
        self.output(self.buffer, 'parsing: ')
        while self.buffer:
            packet = self.buffer[0:ord(self.buffer[0])+4]
            self.buffer = self.buffer[ord(self.buffer[0])+4:]
            self.output(packet, 'p: ')
    
            cmd = packet[4]
            packet = packet[5:]
            
            if cmd in self.cmds:
                self.cmds[cmd](packet)
                
    def output(self, data, pre=''):
        string = ''
        for char in data:
            string += hex(ord(char)) + ':'
        print(pre + string)

    
    def on_connect(self):
        print(' * Connected, sending 0x01')
        self.stream.send('\x0a\x00\x00\x00\x01\x54\x65\x72\x72\x61\x72\x69\x61\x34')
    
    def on_x03(self, data):
        '''Connection Accepted'''
        print(' * Connection accepted')
        print('     Sending player style')
        self.stream.send('\x1b\x00\x00\0x00\x04\x00\x00\xd7\x5a\x37\xff\x7d\x5a\x69\x5a\x4b\xaf\xa5\x8c\xa0\xb4\xd7\xff\xe6\xaf\xa0\x69\x3c\x79\x6c\x65')
        
        print('    Sending Health Data')
        self.stream.send('\x06\x00\x00\x00\x10\x00\x00\x00\x64\x00') # health data
        self.stream.send('\x06\x00\x00\x00\x2a\x00\x00\x00\x00\x00') # mana
        self.stream.send('\x12\x00\x00\x00\x05\x00\x00\x01\x43\x6f\x70\x70\x65\x72\x20\x50\x69\x63\x6b\x61\x78\x65') #inventory
        self.stream.send('\x0c\x00\x00\x00\x05\x00\x02\x02\x4d\x75\x73\x68\x72\x6f\x6f\x6d')
        self.stream.send('\x09\x00\x00\x00\x05\x00\x04\x0e\x41\x63\x6f\x72\x6e')
        self.stream.send('\x01\x00\x00\x00\x06')
        
    def on_x0f(self, data):
        print(' * Got unknown packet')
    
    def on_x25(self, data):
        print(' * Sending password')
        self.stream.send('\x09\x00\x00\x00\x26deepshit')
            
p = Proto('terra.sllabs.com')