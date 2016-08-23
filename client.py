#!/usr/bin/env python

# client.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.3

import sys
from chat.client.clientgui import ClientGUI
from chat.client.chatclient import ChatClient

try:
  app = ClientGUI('Client GUI')
  app.set_client(ChatClient())
  app.bootstrap()
except KeyboardInterrupt:
  print "\nCleaning Used Resources."

  # destroy GUI along with its used resources
  app.destroy_gui()

  print "Bye!"
  sys.exit(0)


