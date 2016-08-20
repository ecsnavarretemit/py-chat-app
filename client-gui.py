#!/usr/bin/env python

# client-gui.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT

import Tkinter as pygui
import tkMessageBox as msgBox
import chatclient

# TODO: erase on send
# TODO: scroll on the bottom
# TODO: scrollbar for the messages
class ClientGUI:
  DIALOG = pygui.Tk()

  def bootstrap(self, windowTitle="Client GUI"):
    self.connectionGUI()

    # set window title
    self.DIALOG.wm_title(windowTitle)

    # Start the GUI
    self.DIALOG.mainloop()

  def connectionGUI(self):
    # [Config Section] :start
    # assemble the UI and the frame if the attribute does not exist
    if not hasattr(self, 'connection_config_frame'):
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
    else:
      self.connection_config_frame.pack(side=pygui.TOP, padx=10, pady=10)
    # [Config Section] :end

  def mainGUI(self):
    # [Chat Room] ::start
    # assemble the UI and the frame if the attribute does not exist
    if not hasattr(self, 'chat_room_frame'):
      self.chat_room_frame = pygui.Frame(self.DIALOG)
      self.chat_room_frame.pack(side=pygui.TOP, padx=10, pady=10)

      self.activity_log_area = pygui.Text(self.chat_room_frame, height=10, width=50)
      self.activity_log_area.grid(row=0)
      self.activity_log_area.config(highlightbackground="black")

      self.message_field = pygui.Entry(self.chat_room_frame)
      self.message_field.grid(row=1, column=0)
      self.message_field.config(width=30)
      self.message_field.bind("<Return>", self.sendMsg)

      self.submit_msg_btn = pygui.Button(self.chat_room_frame, text="Send", command=self.sendMsg)
      self.submit_msg_btn.grid(row=1, column=1)

      self.exit_chat_btn = pygui.Button(self.chat_room_frame, text="Leave Chat Room", command=lambda: self.switchContext('connection'))
      self.exit_chat_btn.grid(row=2)
    else:
      self.chat_room_frame.pack(side=pygui.TOP, padx=10, pady=10)
    # [Chat Room] ::end

  def switchContext(self, context):
    if context == 'main':
      # hide the connection frame/GUI from the window
      if hasattr(self, 'connection_config_frame'):
        self.connection_config_frame.pack_forget()

      self.mainGUI()

    else:
      # disconnect from the server
      self.client.disconnect()

      # hide the chat room frame/GUI from the window
      if hasattr(self, 'chat_room_frame'):
        self.chat_room_frame.pack_forget()

      self.connectionGUI()

  def connectToServer(self):
    hostval = self.host_to_use_field.get()
    portval = self.port_to_use_field.get()
    nameval = self.name_field.get()

    if hostval != '' and portval != '' and nameval != '':
      self.connection_host = str(hostval)
      self.connection_port = int(eval(portval))
      self.connection_name = str(nameval)

      # initiate client-server connection
      self.client.connect(self.connection_host, self.connection_port, self.connection_name)

      # swap UI components/widgets
      self.switchContext('main')

      # log any broadcast message
      self.client.startCommunications(self.log)
    else:
      msgBox.showinfo("Client GUI", "Please enter the host, and port to connect to as well as your chat name")

  def setClient(self, client):
    self.client = client

  def sendMsg(self, event=None):
    message = self.message_field.get()

    # show the message on your side
    self.log('[' + self.connection_name + '] ' + message)

    # send the message to the other side
    self.client.sendMsg(str(message))

  def log(self, message):
    self.activity_log_area.insert(pygui.END, message + "\n")

app = ClientGUI()
app.setClient(chatclient.ChatClient())
app.bootstrap('Client GUI')


