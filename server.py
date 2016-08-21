#!/usr/bin/env python

# server.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.2

import os
import sys
sys.path.insert(0, os.path.abspath('./server'))

from chatserver import ChatServer
from servergui import ServerGUI

try:
  app = ServerGUI()
  app.setServer(ChatServer())
  app.bootstrap('Server GUI')
except KeyboardInterrupt:
  print "\nCleaning Used Resources."

  # destroy GUI along with its used resources
  app.destroyGUI()

  print "Bye!"
  sys.exit(0)


