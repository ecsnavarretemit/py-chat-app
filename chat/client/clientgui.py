# clientgui.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.3

import sys
import Tkinter as pygui
import tkMessageBox as msgBox
from ScrolledText import ScrolledText
from chat.helpers.strip_uid import strip_uid
from chat.helpers.is_ipv4 import is_ipv4

class ClientGUI(object):

  def __init__(self, windowTitle="Client GUI"):
    # create new instance of TK
    self.base_gui = pygui.Tk()

    # store the windowTitle in an object attribute
    self.base_window_title = windowTitle

    # Connection Details
    self.connection_host = ''
    self.connection_name = ''
    self.connection_port = 0

    # Client Object
    self.client = None

    # [Connection GUI Initialization] ::start
    self.connection_gui_bootstrapped = False
    self.connection_config_frame = pygui.Frame(self.base_gui)
    self.host_to_use_field = pygui.Entry(self.connection_config_frame)
    self.port_to_use_field = pygui.Entry(self.connection_config_frame)
    self.name_field = pygui.Entry(self.connection_config_frame)
    self.connect_server_btn = pygui.Button(self.connection_config_frame, text="Connect", command=self.connect_to_server)
    # [Connection GUI Initialization] ::end

    # [Main GUI Initialization] ::start
    self.main_gui_bootstrapped = False
    self.chat_room_frame = pygui.Frame(self.base_gui)
    self.activity_log_area = ScrolledText(self.chat_room_frame, height=10, width=50)
    self.message_field = pygui.Entry(self.chat_room_frame)
    self.submit_msg_btn = pygui.Button(self.chat_room_frame, text="Send", command=self.send_msg)

    self.exit_chat_btn = pygui.Button(self.chat_room_frame,
                                      text="Leave Chat Room",
                                      command=lambda: self.switch_context('connection'))
    # [Connection GUI Initialization] ::end

  def bootstrap(self):
    if self.client is None:
      print "Client Object must be specified. Call the set_client() method and set the ClientGUI Object."
      sys.exit(1)

    self.connection_gui()

    # set window title
    self.base_gui.wm_title(self.base_window_title)

    # handle close button
    self.base_gui.protocol("WM_DELETE_WINDOW", self.destroy_gui)

    # Start the GUI
    self.base_gui.mainloop()

  def connection_gui(self):
    # [Config Section] :start
    # assemble the UI and the frame if the attribute does not exist
    if self.connection_gui_bootstrapped is False:
      # Add field for host/hostname to use
      pygui.Label(self.connection_config_frame, text="Host").grid(row=0, column=0)
      self.host_to_use_field.grid(row=0, column=1)

      # Add field for port to use
      pygui.Label(self.connection_config_frame, text="Port").grid(row=1, column=0)
      self.port_to_use_field.grid(row=1, column=1)

      # Add field for chat username/alias
      pygui.Label(self.connection_config_frame, text="Name").grid(row=2, column=0)
      self.name_field.grid(row=2, column=1)

      self.connect_server_btn.grid(row=3, column=1)

      self.connection_gui_bootstrapped = True

    self.connection_config_frame.pack(side=pygui.TOP, padx=10, pady=10)
    # [Config Section] :end

  def main_gui(self):
    # [Chat Room] ::start
    # assemble the UI and the frame if the attribute does not exist
    if self.main_gui_bootstrapped is False:
      self.activity_log_area.grid(row=0)
      self.activity_log_area.edit_modified(0)
      self.activity_log_area.config(highlightbackground="black")
      self.activity_log_area.bind('<<Modified>>', self.scroll_to_end)

      self.message_field.grid(row=1, column=0)
      self.message_field.config(width=30)
      self.message_field.bind("<Return>", self.send_msg)

      self.submit_msg_btn.grid(row=1, column=1)

      self.exit_chat_btn.grid(row=2)

      self.main_gui_bootstrapped = True

    # empty the chat logs
    self.activity_log_area.delete("1.0", pygui.END)

    # show the frame for chat room
    self.chat_room_frame.pack(side=pygui.TOP, padx=10, pady=10)
    # [Chat Room] ::end

  def destroy_gui(self):
    # disconnect from the server
    self.client.disconnect()

    # destroy the window
    self.base_gui.destroy()

  def switch_context(self, context):
    if context == 'main':
      # hide the connection frame/GUI from the window
      if hasattr(self, 'connection_config_frame'):
        self.connection_config_frame.pack_forget()

      self.main_gui()

      title = "%s connected on %s:%s - %s" % (strip_uid(self.connection_name),
                                              self.connection_host,
                                              str(self.connection_port),
                                              self.base_window_title)

      # change the window title to show the connection details
      self.base_gui.wm_title(title)

    else:
      # disconnect from the server
      self.client.disconnect()

      # hide the chat room frame/GUI from the window
      if hasattr(self, 'chat_room_frame'):
        self.chat_room_frame.pack_forget()

      self.connection_gui()

      # set window title
      self.base_gui.wm_title(self.base_window_title)

  def scroll_to_end(self, *_):
    # scroll to the end of text area
    self.activity_log_area.see(pygui.END)
    self.activity_log_area.edit_modified(0)

  def connect_to_server(self):
    hostval = self.host_to_use_field.get()
    portval = self.port_to_use_field.get()
    nameval = self.name_field.get()

    if hostval != '' and portval != '' and nameval != '':
      self.connection_host = str(hostval)
      self.connection_name = str(nameval)

      # check if the host supplied is a valid ip address
      if not is_ipv4(self.connection_host):
        msgBox.showinfo("Client GUI", "Invalid IP Address")
        return

      # check if the input for port number is a valid integer
      try:
        self.connection_port = int(portval)
      except ValueError:
        msgBox.showinfo("Client GUI", "Invalid Port Number")
        return

      # initiate client-server connection
      if self.client.connect(self.connection_host, self.connection_port, self.connection_name) is True:
        # swap UI components/widgets
        self.switch_context('main')

        # log any broadcast message and disconnect on lost connection
        self.client.start_communications(self.log, lambda: self.switch_context('connection'))
      else:
        msgBox.showinfo("Client GUI", "Cant connect to server. Please try again later.")

    else:
      msgBox.showinfo("Client GUI", "Please enter the host, and port to connect to as well as your chat name")

  def set_client(self, client):
    self.client = client

  def send_msg(self, *_):
    message = self.message_field.get()

    # only send messages which are not empty
    if message:
      # show the message on your side
      self.log('[' + strip_uid(self.connection_name) + '] ' + message)

      # send the message to the other side
      self.client.send_msg(str(message))

      # delete the message
      self.message_field.delete(0, pygui.END)

  def log(self, message):
    self.activity_log_area.insert(pygui.END, message + "\n")


