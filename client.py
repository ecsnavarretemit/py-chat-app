#!/usr/bin/env python

# client.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.3

import os
import sys
sys.path.insert(0, os.path.abspath('./client'))

from clientgui import ClientGUI
from chatclient import ChatClient

try:
  app = ClientGUI()
  app.setClient(ChatClient())
  app.bootstrap('Client GUI')
except KeyboardInterrupt:
  print "\nCleaning Used Resources."

  # destroy GUI along with its used resources
  app.destroyGUI()

  print "Bye!"
  sys.exit(0)


