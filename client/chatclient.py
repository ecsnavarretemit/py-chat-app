# chatserver.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.3

import socket
import select
import threading
import re

class ChatClient:
  SOCKET_LIST = []
  RECV_BUFFER = 4096

  def connect(self, host, port, name):
    is_success = True

    self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connection_socket.settimeout(2)

    # connect to remote host
    try:
      self.connection_socket.connect((host, port))

      # send the fist message as the chat user identifier in the format of `ch_alias:<alias>`
      self.connection_socket.send('ch_alias:' + name)
    except:
      is_success = False

    return is_success

  def disconnect(self):
    # check if the instance has connection socket
    # if it has shutdown and close the socket
    if hasattr(self, 'connection_socket'):
      try:
        self.connection_socket.shutdown(socket.SHUT_RDWR)
        self.connection_socket.close()
      except:
        pass

    # stop the thread
    if hasattr(self, 'stop_thread_evt'):
      self.stop_thread_evt.set()

  def startCommunications(self, logCallback=None, disconnectionCallback=None):
    self.stop_thread_evt = threading.Event()

    threading.Thread(name="py-chat-client-thread", target=self.run, args=(self.stop_thread_evt, logCallback, disconnectionCallback,)).start()

  def sendMsg(self, message):
    self.connection_socket.send(message)

  def run(self, stop_event, logCallback=None, disconnectionCallback=None):
    while(not stop_event.is_set()):
      SOCKET_LIST = [self.connection_socket]

      try:
        # Get the list sockets which are readable
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [])

        for sock in ready_to_read:
          if sock == self.connection_socket:
            # incoming message from remote server, s
            data = sock.recv(self.RECV_BUFFER)

            if not data:
              if disconnectionCallback != None:
                disconnectionCallback()
            else:
              if logCallback != None:
                logCallback(data)

      except:
        stop_event.set()


