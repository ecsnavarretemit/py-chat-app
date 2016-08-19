#!/usr/bin/env python

# client-gui.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT

import Tkinter as pygui
import tkMessageBox as msgBox

class ClientGUI:
  DIALOG = pygui.Tk()

  def bootstrap(self, windowTitle="Client GUI"):
    self.connectionGUI(windowTitle)

  def connectionGUI(self, windowTitle):
    # set window title
    self.DIALOG.wm_title(windowTitle)

    # [Config Section] :start
    self.connection_config_frame = pygui.Frame(self.DIALOG)
    self.connection_config_frame.pack(side=pygui.TOP, padx=10, pady=10)

    # Add field for host/hostname to use
    pygui.Label(self.connection_config_frame, text="Host").grid(row = 0, column=0)
    self.host_to_use_field = pygui.Entry(self.connection_config_frame)
    self.host_to_use_field.grid(row=0, column=1)

    # Add field for port to use
    pygui.Label(self.connection_config_frame, text="Port").grid(row = 1, column=0)
    self.port_to_use_field = pygui.Entry(self.connection_config_frame)
    self.port_to_use_field.grid(row=1, column=1)

    # Add field for chat username/alias
    pygui.Label(self.connection_config_frame, text="Name").grid(row = 2, column=0)
    self.name_field = pygui.Entry(self.connection_config_frame)
    self.name_field.grid(row=2, column=1)

    self.connect_server_btn = pygui.Button(self.connection_config_frame, text="Connect", command=self.connectToServer)
    self.connect_server_btn.grid(row=3, column=1)
    # [Config Section] :end

    # Start the GUI
    self.DIALOG.mainloop()

  def connectToServer(self):
    hostval = self.host_to_use_field.get()
    portval = self.port_to_use_field.get()
    nameval = self.name_field.get()

    if hostval != '' and portval != '' and nameval != '':
      print "Connect"
    else:
      msgBox.showinfo("Client GUI", "Please enter the host, and port to connect to as well as your chat name")

app = ClientGUI()
app.bootstrap('Client GUI')


