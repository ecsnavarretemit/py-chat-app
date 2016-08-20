#!/usr/bin/env python

# server-gui.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.1

import Tkinter as pygui
from ScrolledText import ScrolledText
import chatserver

class ServerGUI:
  DIALOG = pygui.Tk()
  SERVER_ON = False

  def bootstrap(self, windowTitle="Server GUI"):
    self.setupGUI(windowTitle)

  def setServer(self, server):
    self.server = server

  def setupGUI(self, windowTitle):
    # set window title
    self.DIALOG.wm_title(windowTitle)

    # [Config Section] :start
    self.server_config_frame = pygui.Frame(self.DIALOG)
    self.server_config_frame.pack(side=pygui.TOP, pady=10)

    # Add field for port to use
    pygui.Label(self.server_config_frame, text="Server port to use").grid(row = 0, column=0)

    self.port_to_use_field = pygui.Entry(self.server_config_frame)
    self.port_to_use_field.grid(row=0, column=1)
    self.port_to_use_field.bind("<Return>", self.invokeServer)
    # [Config Section] :end

    # [Controls Section] ::start
    self.server_controls_frame = pygui.Frame(self.DIALOG)
    self.server_controls_frame.pack(side=pygui.RIGHT, fill=pygui.Y)

    # Add Start server button
    self.create_server_btn = pygui.Button(self.server_controls_frame, text="Start Server", command=self.invokeServer)
    self.create_server_btn.grid(row=0, column=1)

    # Stop Server
    self.stop_server_btn = pygui.Button(self.server_controls_frame, text="Stop Server", command=self.stopServer)
    self.stop_server_btn.grid(row=1, column=1)

    # Quit Button
    self.quit_btn = pygui.Button(self.server_controls_frame, text="Quit", command=self.destroyGUI)
    self.quit_btn.grid(row=2, column=1)
    # [Controls Section] ::end

    # [Logs Section] ::start
    self.server_logs_frame = pygui.Frame(self.DIALOG)
    self.server_logs_frame.pack(side=pygui.LEFT, padx=10, pady=10)

    # Create a text area for showing logs.
    pygui.Label(self.server_logs_frame, text="Logs", ).grid(row=0)
    self.activity_log_area = ScrolledText(self.server_logs_frame, height=10, width=50)
    self.activity_log_area.edit_modified(0)
    self.activity_log_area.grid(row=1)
    self.activity_log_area.config(highlightbackground="black")
    self.activity_log_area.bind('<<Modified>>', self.scrollToEnd)
    # [Logs Section] ::end

    # handle close button
    self.DIALOG.protocol("WM_DELETE_WINDOW", self.destroyGUI)

    # Start the GUI
    self.DIALOG.mainloop()

  def scrollToEnd(self, event=None):
    # scroll to the end of text area
    self.activity_log_area.see(pygui.END)
    self.activity_log_area.edit_modified(0)

  def destroyGUI(self):
    self.stopServer()
    self.DIALOG.destroy()

  def stopServer(self, event=None):
    if self.SERVER_ON == True:
      self.server.stop(self.log)

      # set the SERVER_ON flag to false to enable create a new server instance
      self.SERVER_ON = False
    else:
      self.log("Server already stopped.")

  def invokeServer(self, event=None):
    portval = self.port_to_use_field.get()

    if portval != '':
      # start the server if not yet started
      if self.SERVER_ON == False:
        # Prevent starting another instance of server
        self.SERVER_ON = True

        # log the message
        self.server.setPort(int(eval(portval)))
        self.server.invoke(self.log)
      else:
        self.log("Server already started on port: " + str(eval(portval)))
    else:
      self.log("Please provide port number for the server to bind on. Thanks!")

  def log(self, message):
    self.activity_log_area.insert(pygui.END, message + "\n")

app = ServerGUI()
app.setServer(chatserver.ChatServer())
app.bootstrap('Server GUI')


