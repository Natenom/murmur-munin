#!/usr/bin/env python
# -*- coding: utf-8
#
# munin-murmur.py - "murmur stats (User/Bans/Uptime/Channels)" script for munin.
# Copyright (c) 2010, Natenom / Natenom@natenom.name
# Version: 0.0.4
# 2010-09-03


#Path to Murmur.ice
iceslice='/usr/share/slice/Murmur.ice'

#Murmur-Port (not needed to work, only for display purposes)
serverport=64738

#Port where ice listen
iceport=6502


import Ice, sys
Ice.loadSlice("--all -I/usr/share/slice %s" % iceslice)

ice = Ice.initialize()
import Murmur

if (sys.argv[1:]):
  if (sys.argv[1] == "config"):
    print 'graph_title Murmur (Port %s)' % (serverport)
    print 'graph_vlabel Count'
    print 'users.label Users (All)'
    print 'usersnotauth.label Users (Not authenticated)'
    print 'uptime.label Uptime in days'
    print 'chancount.label Channelcount/10'
    print 'bancount.label Bans on server'
    sys.exit(0)


meta = Murmur.MetaPrx.checkedCast(ice.stringToProxy("Meta:tcp -h 127.0.0.1 -p %s" % (iceport)))
server=meta.getServer(1)

#count users
usersnotauth=0
users=server.getUsers()
for key in users.keys():
  if (users[key].userid == -1):
    usersnotauth+=1

print "users.value %i" % (len(users))
print "uptime.value %.2f" % (float(meta.getUptime())/60/60/24)
print "chancount.value %.1f" % (len(server.getChannels())/10)
print "bancount.value %i" % (len(server.getBans()))
print "usersnotauth.value %i" % (usersnotauth)
  
ice.shutdown()
