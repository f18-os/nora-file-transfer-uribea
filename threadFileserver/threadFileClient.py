#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time

import params
from framedSock import FramedStreamSock
from threading import Thread
import time

switchesVarDefaults = (
    (('-s', '--server'), 'server', "localhost:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

class ClientThread(Thread):
    def __init__(self, serverHost, serverPort, debug):
        Thread.__init__(self, daemon=False)
        self.serverHost, self.serverPort, self.debug = serverHost, serverPort, debug
        self.start()
    def run(self):
       s = None
       for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
           af, socktype, proto, canonname, sa = res
           try:
               print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
               s = socket.socket(af, socktype, proto)
           except socket.error as msg:
               print(" error: %s" % msg)
               s = None
               continue
           try:
               print(" attempting to connect to %s" % repr(sa))
               s.connect(sa)
           except socket.error as msg:
               print(" error: %s" % msg)
               s.close()
               s = None
               continue
           break

       if s is None:
           print('could not open socket')
           sys.exit(1)

       fs = FramedStreamSock(s, debug=debug)
       cmd = input('ftp$ ')
       para = cmd.split()
       #para = ('put', 'whygrep')
       if (len(para) == 2 and para[0] == 'put'):#check if put in filename
           try:
               print('atpara1')
               print(para[1])
               file = open(para[1], 'rb')

           except:
               print('file not found')
               exit(0)
           filenam = './' + para[1]  # send filename
           fs.sendmsg(filenam.encode())
           print("received:", fs.receivemsg())
           while True:  # read file

               data = file.read(100)  # .encode()
               print(data)
               if not data:  # end of file
                   fs.sendmsg(b"~")
                   print("received:", fs.receivemsg())
                   return
               fs.sendmsg(data)#.encode())  # send file by 100 byte increments
               print("received:", fs.receivemsg())
       else:
           print('no command or missing parameter')

for i in range(1):
    ClientThread(serverHost, serverPort, debug)

