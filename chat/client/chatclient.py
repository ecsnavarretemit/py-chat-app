# chatserver.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.3

import socket
import select
import threading
from chat.helpers.rand_uid import rand_uid

class ChatClient(object):
  recv_buffer = 4096

  def __init__(self):
    # Initialize Blank Socket
    self.connection_socket = None

    # create thread event for stopping the thread execution
    self.stop_thread_evt = threading.Event()

  def connect(self, host, port, name):
    is_success = True

    # connect to remote host
    try:
      self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.connection_socket.settimeout(2)
      self.connection_socket.connect((host, port))

      # send the first message as the chat user identifier in the format of
      # `ch_alias:<alias>:uid-xxxxxxxxxx`
      self.connection_socket.send('ch_alias:' + name + ':uid-' + rand_uid(10))
    except socket.error:
      is_success = False

    return is_success

  def disconnect(self):
    # check if the instance has connection socket
    # if it has shutdown and close the socket
    if hasattr(self, 'connection_socket') and self.connection_socket != None:
      try:
        self.connection_socket.shutdown(socket.SHUT_RDWR)
        self.connection_socket.close()
      except socket.error:
        pass

    # stop the thread
    if hasattr(self, 'stop_thread_evt'):
      self.stop_thread_evt.set()

  def start_communications(self, log_callback=None, disconnection_callback=None):
    # reset the thread event to blank state
    if self.stop_thread_evt.is_set():
      self.stop_thread_evt.clear()

    threading.Thread(
      name="py-chat-client-thread",
      target=self.run,
      args=(self.stop_thread_evt, log_callback, disconnection_callback,)
    ).start()

  def send_msg(self, message):
    self.connection_socket.send(message)

  def run(self, stop_event, log_callback=None, disconnection_callback=None):
    while not stop_event.is_set():
      socket_list = [self.connection_socket]

      try:
        # Get the list sockets which are readable
        # (read, write, error) = Sockets
        # we are only interested in the read socket
        ready_to_read, _, _ = select.select(socket_list, [], [])

        for sock in ready_to_read:
          if sock == self.connection_socket:
            # incoming message from remote server, s
            data = sock.recv(self.recv_buffer)

            if not data:
              if disconnection_callback != None:
                disconnection_callback()
            else:
              if log_callback != None:
                log_callback(data)

      except (socket.error, select.error):
        stop_event.set()


