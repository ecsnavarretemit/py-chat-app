# servergui.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.3

import sys
import Tkinter as pygui
import tkMessageBox as msgBox
from ScrolledText import ScrolledText

class ServerGUI(object):
  server_on = False

  def __init__(self, window_title="Server GUI"):
    self.base_gui = pygui.Tk()

    self.window_title = window_title
    self.server_port = 0
    self.server = None

    # [GUI Initialization] ::start
    self.server_config_frame = pygui.Frame(self.base_gui)
    self.port_to_use_field = pygui.Entry(self.server_config_frame)
    self.server_controls_frame = pygui.Frame(self.base_gui)
    self.create_server_btn = pygui.Button(self.server_controls_frame, text="Start Server", command=self.invoke_server)
    self.stop_server_btn = pygui.Button(self.server_controls_frame, text="Stop Server", command=self.stop_server)
    self.quit_btn = pygui.Button(self.server_controls_frame, text="Quit", command=self.destroy_gui)
    # [GUI Initialization] ::end

    self.server_logs_frame = pygui.Frame(self.base_gui)
    self.activity_log_area = ScrolledText(self.server_logs_frame, height=10, width=50)

  def bootstrap(self):
    if self.server is None:
      print "Server Object must be specified. Call the set_server() method and set the ServerGUI Object."
      sys.exit(1)

    # set window title
    self.base_gui.wm_title(self.window_title)

    # [Config Section] :start
    self.server_config_frame.pack(side=pygui.TOP, pady=10)

    # Add field for port to use
    pygui.Label(self.server_config_frame, text="Server port to use").grid(row=0, column=0)

    self.port_to_use_field.grid(row=0, column=1)
    self.port_to_use_field.bind("<Return>", self.invoke_server)
    # [Config Section] :end

    # [Controls Section] ::start
    self.server_controls_frame.pack(side=pygui.RIGHT, fill=pygui.Y)

    # Add Start server button
    self.create_server_btn.grid(row=0, column=1)

    # Stop Server
    self.stop_server_btn.grid(row=1, column=1)

    # Quit Button
    self.quit_btn.grid(row=2, column=1)
    # [Controls Section] ::end

    # [Logs Section] ::start
    self.server_logs_frame.pack(side=pygui.LEFT, padx=10, pady=10)

    # Create a text area for showing logs.
    pygui.Label(self.server_logs_frame, text="Logs").grid(row=0)

    self.activity_log_area.edit_modified(0)
    self.activity_log_area.grid(row=1)
    self.activity_log_area.config(highlightbackground="black")
    self.activity_log_area.bind('<<Modified>>', self.scroll_to_end)
    # [Logs Section] ::end

    # handle close button
    self.base_gui.protocol("WM_DELETE_WINDOW", self.destroy_gui)

    # Start the GUI
    self.base_gui.mainloop()

  def set_server(self, server):
    self.server = server

  def scroll_to_end(self, *_):
    # scroll to the end of text area
    self.activity_log_area.see(pygui.END)
    self.activity_log_area.edit_modified(0)

  def destroy_gui(self):
    self.stop_server()
    self.base_gui.destroy()

  def stop_server(self, *_):
    if self.server_on is True:
      self.server.stop(self.log)

      # set the SERVER_ON flag to false to enable create a new server instance
      self.server_on = False
    else:
      self.log("Server already stopped.")

  def invoke_server(self, *_):
    portval = self.port_to_use_field.get()

    if portval != '':
      # check if the input for port number is a valid integer
      try:
        self.server_port = int(portval)
      except ValueError:
        msgBox.showinfo("Client GUI", "Invalid Port Number")
        return

      # start the server if not yet started
      if self.server_on is False:
        # log the message
        self.server.set_port(self.server_port)

        if not self.server.invoke(self.log):
          msgBox.showinfo("Client GUI", "Cannot bind to port: %s. Please select another port to bind on." %
                          str(self.server_port))

          return

        # Prevent starting another instance of server
        self.server_on = True
      else:
        self.log("Server already started on port: " + str(self.server_port))
    else:
      self.log("Please provide port number for the server to bind on. Thanks!")

  def log(self, message):
    self.activity_log_area.insert(pygui.END, message + "\n")


