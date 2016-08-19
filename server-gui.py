#!/usr/bin/env python

# server-gui.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT

import Tkinter as pygui

class ServerGUI:
  DIALOG = pygui.Tk()
  SERVER_ON = False

  def bootstrap(self, windowTitle="Server GUI"):
    self.setupGUI(windowTitle)

  def setupGUI(self, windowTitle):
    # set window title
    self.DIALOG.wm_title(windowTitle)

    # Add field for port to use
    pygui.Label(self.DIALOG, text="Server port to use").grid(row = 0)

    self.port_to_use_field = pygui.Entry(self.DIALOG)
    self.port_to_use_field.grid(row=0, column=1)
    self.port_to_use_field.bind("<Return>", self.invokeServer)

    # Add Start server button
    self.create_server_btn = pygui.Button(self.DIALOG, text="Start Server", command=self.invokeServer)
    self.create_server_btn.grid(row=1)

    # Stop Server
    self.stop_server_btn = pygui.Button(self.DIALOG, text="Stop Server", command=self.stopServer)
    self.stop_server_btn.grid(row="2")

    # Quit Button
    self.quit_btn = pygui.Button(self.DIALOG, text="Quit", command=self.DIALOG.destroy)
    self.quit_btn.grid(row=3)

    # Create a text area for showing logs.
    self.activity_log_area = pygui.Text(self.DIALOG, height=10, width=90)
    self.activity_log_area.grid(row=4)

    # Start the GUI
    self.DIALOG.mainloop()

  def stopServer(self, event=None):
    self.log("Stopping Server")

  def invokeServer(self, event=None):
    portval = self.port_to_use_field.get()

    if portval != '':
      # start the server if not yet started
      if self.SERVER_ON == False:
        # Prevent starting another instance of server
        self.SERVER_ON = True

        self.log("Starting Server on port: " + str(eval(portval)))
      else:
        self.log("Server already started on port: " + str(eval(portval)))
    else:
      self.log("Please provide port number for the server to bind on. Thanks!")

  def log(self, message):
    self.activity_log_area.insert(pygui.END, message + "\n")

app = ServerGUI()
app.bootstrap('Server GUI')


