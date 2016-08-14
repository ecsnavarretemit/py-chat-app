# chat-client.py
#
# Courtesy of http://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
# Modified by Exequiel Ceasar Navarrete <esnavarrete@up.edu.ph>

import sys
import socket
import select
import re
 
def chat_client():
    if(len(sys.argv) < 3) :
        print 'Usage : python chat_client.py hostname port [chat_alias]'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    # if there are more than 4 arguments in chat-client.py invocation,
    # save them in chat_alias variable else prompt the user to enter a chat alias
    if(len(sys.argv) > 3):
        chat_alias = sys.argv[3]
    else:
        sys.stdout.write('Enter your chat name: ')
        chat_alias = sys.stdin.readline().rstrip()
        sys.stdout.flush()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. You can start sending messages'
    sys.stdout.write('[' + chat_alias + '] ')
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)

                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    # extract name and message <name>:<message>
                    chat_parts = re.search('(\[.+\]) (.+):(.+)', data)

                    if chat_parts:
                        ch_alias = chat_parts.group(2)
                        ch_msg   = chat_parts.group(3)
                        sys.stdout.write('\r[' + ch_alias + ' says] ' + ch_msg + "\n")
                        sys.stdout.write('[' + chat_alias + '] ')
                    else:
                        sys.stdout.write(data)

                    # sys.stdout.write('[' + chat_alias + '] ')
                    sys.stdout.flush()

            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send(chat_alias + ':' + msg)
                sys.stdout.flush()

                sys.stdout.write('[' + chat_alias + '] ')
                sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(chat_client())


