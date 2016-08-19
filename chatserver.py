# chat-server.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT

import sys
import socket
import select
import threading

class ChatServer:
  PORT = 9000
  HOST = ''
  SOCKET_LIST = []
  RECV_BUFFER = 4096

  def setPort(self, port):
    self.PORT = port

  def setHost(self, host):
    self.HOST = host

  def invoke(self, callback=None):
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind((self.HOST, self.PORT))
    self.server_socket.listen(10)

    # add server socket object to the list of readable connections
    self.SOCKET_LIST.append(self.server_socket)

    if callback != None:
      # invoke a callback supplied
      callback("Starting Server on port: " + str(self.PORT))

    # invoke the run method
    threading.Thread(target=self.run).start()

  def run(self):
    while True:
      # get the list sockets which are ready to be read through select
      # 4th arg, time_out  = 0 : poll and never block
      ready_to_read,ready_to_write,in_error = select.select(self.SOCKET_LIST, [], [], 0)

      for sock in ready_to_read:
        # a new connection request recieved
        if sock == self.server_socket:
          sockfd, addr = self.server_socket.accept()
          self.SOCKET_LIST.append(sockfd)
          print "Client (%s, %s) connected" % addr

          self.broadcast(self.server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

        # a message from a client, not a new connection
        else:
          # process data recieved from client,
          try:
            # receiving data from the socket.
            data = sock.recv(self.RECV_BUFFER)

            if data:
              # there is something in the socket
              self.broadcast(self.server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
            else:
              # remove the socket that's broken
              if sock in self.SOCKET_LIST:
                self.SOCKET_LIST.remove(sock)

                # at this stage, no data means probably the connection has been broken
                self.broadcast(self.server_socket, sock, "Client (%s, %s) is offline\n" % addr)

          # exception
          except:
            self.broadcast(self.server_socket, sock, "Client (%s, %s) is offline\n" % addr)
            continue

  def broadcast(self, server_socket, sock, message):
    for socket in self.SOCKET_LIST:
      # send the message only to peer
      if socket != server_socket and socket != sock :
        try:
          socket.send(message)
        except:
          # broken socket connection
          socket.close()

          # broken socket, remove it
          if socket in self.SOCKET_LIST:
            self.SOCKET_LIST.remove(socket)

  def stop(self, callback=None):
    # prevent from throwing errors by checking if the server_socket attribute exists.
    if hasattr(self, 'server_socket'):
      self.server_socket.close()

      if callback != None:
        # invoke a callback supplied
        callback("Stopping server listening on port: " + str(self.PORT))


