# chatserver.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.1.3

import socket
import select
import threading
import re
from chat.helpers.strip_uid import strip_uid

# TODO: callbacks should be implemented as event listener
class ChatServer(object):
  port = 9000
  host = ''
  socket_dict = {}
  recv_buffer = 4096

  def __init__(self):
    # Initialize Blank Socket
    self.server_socket = None

    # create thread event for stopping the thread execution
    self.stop_thread_evt = threading.Event()

  def set_port(self, port):
    self.port = port

  def set_host(self, host):
    self.host = host

  def invoke(self, callback=None):
    is_success = True

    try:
      self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.server_socket.bind((self.host, self.port))
      self.server_socket.listen(10)

      # add server socket object to the list of readable connections
      self.socket_dict['cs_main_sckt'] = self.server_socket

      if callback != None:
        # invoke a callback supplied
        callback("Starting Server on port: " + str(self.port))

      # reset the thread event to blank state
      if self.stop_thread_evt.is_set() is True:
        self.stop_thread_evt.clear()

      # invoke the run method
      threading.Thread(name="py-chat-server-thread", target=self.run, args=(self.stop_thread_evt, callback,)).start()
    except socket.error:
      is_success = False

    return is_success

  # TODO: refactor this function so that it will lessen the indentation level
  #       of this section. Can be broken into separate functions that can be reused
  #       in other parts of this application.
  def run(self, stop_event, callback=None):
    sock_local_copy = self.socket_dict.copy()

    while not stop_event.is_set():
      try:
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        #
        # (read, write, error) = Sockets
        # we are only interested in the read socket
        ready_to_read, _, _ = select.select(sock_local_copy.values(), [], [], 0)

        for sock in ready_to_read:
          # a new connection request recieved
          if sock == self.server_socket:
            # accept returns the socket and the address but we are only interested in the socket
            sockfd, _ = self.server_socket.accept()

            sock_local_copy['tmp'] = sockfd

          # a message from a client, not a new connection
          else:
            # process data recieved from client,
            try:
              # receiving data from the socket.
              data = sock.recv(self.recv_buffer)

              if data:
                # there is something in the socket
                # check if its an alias or not
                re_alias = re.search('ch_alias:(.+)', data)

                if re_alias:
                  chat_alias = re_alias.group(1)

                  # store the temporary socket back to the dictionary with the correct key
                  sock_local_copy[chat_alias] = sock_local_copy['tmp']

                  # remove the temporary socket
                  sock_local_copy.pop('tmp')

                  # get the peername
                  peername = sock_local_copy[chat_alias].getpeername()

                  if callback != None:
                    callback(strip_uid(chat_alias) + " on IP address " + peername[0] + " has connected to the server.")

                  self.broadcast(self.server_socket, sock,
                                 "[Server] %s on IP address %s has connected in the chat room" %
                                 (strip_uid(chat_alias), peername[0]))

                else:
                  for name, item_socket in sock_local_copy.iteritems():
                    # broadcast the message
                    if item_socket == sock:
                      self.broadcast(self.server_socket, sock, '[' + strip_uid(name) + '] ' + data)

              else:
                deep_sock_local_copy = sock_local_copy.copy()
                for_removal = []

                # to prevent a runtime exception we store the name of the sockets in a list
                # then iterate it later for removal. since looping the dictionary and removing items at the same time
                # throws a RuntimeError
                for name, item_socket in deep_sock_local_copy.iteritems():
                  # remove the socket that's broken
                  if item_socket == sock:
                    for_removal.append(name)

                # remove items that are subject for removal
                for item in for_removal:
                  socket_to_remove = deep_sock_local_copy.get(item)
                  peername = socket_to_remove.getpeername()

                  deep_sock_local_copy.pop(item)

                  if callback != None:
                    callback(strip_uid(item) + " on IP address " + peername[0] + " has disconnected from the server.")

                  self.broadcast(self.server_socket, socket_to_remove,
                                 "[Server] %s on IP address %s has left the chat room." %
                                 (strip_uid(item), peername[0]))

                sock_local_copy = deep_sock_local_copy

            # exception
            except socket.error:
              if callback != None:
                callback(strip_uid(name) + " has disconnected from the server.")

              self.broadcast(self.server_socket, sock, "%s has gone offline" % strip_uid(name))
              continue

        self.socket_dict = sock_local_copy

      except (socket.error, select.error):
        stop_event.set()

  def broadcast(self, server_socket, sock, message):
    for name, item_socket in self.socket_dict.iteritems():
      # send the message only to peer
      if item_socket != server_socket and item_socket != sock:
        try:
          item_socket.send(message)
        except socket.error:
          # broken socket connection
          item_socket.close()

          # broken socket, remove it
          if item_socket in self.socket_dict:
            self.socket_dict.pop(name)

  def stop(self, callback=None):
    # prevent from throwing errors by checking if the server_socket attribute exists.
    if hasattr(self, 'server_socket'):
      # stop the thread
      if hasattr(self, 'stop_thread_evt'):
        self.stop_thread_evt.set()

      # close all sockets
      for itemsocket in self.socket_dict.values():
        itemsocket.close()

      # empty out the socket dictionary
      self.socket_dict.clear()

      del self.server_socket

      if callback != None:
        # invoke a callback supplied
        callback("Stopping server listening on port: " + str(self.port))


