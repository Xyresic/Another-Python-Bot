#!/usr/bin/python3
import sys
import re
import socket
import http.client
import urllib.parse
import math
import traceback

from time import sleep

## This is the class that will communicate with the IRC server ##
#################################################################
class irc:
    
    # info is a dictionary containing connection information
    def __init__(self, info):
        
        self.HOST = info["HOST"]
        self.PORT = int(info["PORT"])
        self.CHANNELS = info["CHANNELS"]
        self.NICK = info["NICK"]
        self.IDENT = info["IDENT"]
        self.REALNAME = info["REALNAME"]
        self.EXTRA = info["EXTRA"]

    def connect(self, info):
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))
        self.s.send("NICK {}\r\n".format(self.NICK).encode("utf-8"))
        self.s.send("USER {} 0 * :{}\r\n"
                    .format(self.IDENT, self.REALNAME).encode("utf-8"))

    # Send a command to IRC
    def sendcmd(self, cmd, msg):
        self.s.send("{} :{}\r\n"
                    .format(cmd, msg).encode("utf-8", errors="ignore"))

    # Send a message to IRC
    def sendmsg(self, channel, msg):
        self.s.send("PRIVMSG {} :{}\r\n"
                    .format(channel, msg).encode("utf-8"))

    def run(self):
        print(self.s.recv(512).decode("utf-8"))
                    

## MAIN PROGRAM ##
##################

# First thing we need to do is check for the info file
try:
    f = open("info", "r")
except IOError:
    print("File Not Found: \"info\"")
    sys.exit(1)

# Get settings from file
info = {}
for l in f:
    (key, val) = l.strip("\n").split("=")
    info[key.upper()] = val

# Create a new irc object
try:
    s = irc(info)
except KeyError:
    print("Error in info file")
    sys.exit(1)

s.connect(info)
s.sendcmd("JOIN", "#Patchouli")
while 1:
    s.run()