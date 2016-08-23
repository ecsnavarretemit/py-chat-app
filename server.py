#!/usr/bin/env python

# server.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.3

import sys
from chat.server.chatserver import ChatServer
from chat.server.servergui import ServerGUI

try:
  app = ServerGUI('Server GUI')
  app.set_server(ChatServer())
  app.bootstrap()
except KeyboardInterrupt:
  print "\nCleaning Used Resources."

  # destroy GUI along with its used resources
  app.destroy_gui()

  print "Bye!"
  sys.exit(0)


