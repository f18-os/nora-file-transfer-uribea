#! /usr/bin/env python3
import sys, os, socket, params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    from framedSock import FramedStreamSock
    sock, addr = lsock.accept()
    fsock = FramedStreamSock(sock, debug)

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = fsock.receivemsg()
            if debug: print("rec'd: ", payload)
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)


            payload += b"!"             # make emphatic!
            fsock.sendmsg(payload)
