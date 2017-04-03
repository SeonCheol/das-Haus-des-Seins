from socket import *
from select import *
import sys
from time import ctime
import wave
import pyaudio

import grungermonet as gm

HOST = ''
PORT = 5810
BUF_SIZE = 1024
ADDR = (HOST, PORT)
NUM = 2
FORMAT = pyaudio.paInt16
RECORD_SECONDS = 10

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(ADDR)
serverSock.listen(10)
connection_list = [serverSock]
print "start. wait connecting to %s port" %str(PORT)
frames = []
p = pyaudio.PyAudio()

## start flag
start = False

num_client = 0

while connection_list:
    try:
        print('wait...')

        # requested with select , and unblock every 10 seconds
        read_sock, write_sock, err_sock = select(connection_list, [], [], 10)
        print read_sock, write_sock, err_sock


        for sock in read_sock:
            ## new connection ##
            if sock == serverSock:
                clientSock, addr_info = serverSock.accept()
                connection_list.append(clientSock)
                print(connection_list)
                num_client += 1
                if num_client == 2:
                    for tmp_sock in connection_list[1:]:
                        tmp_sock.send('s')
                    # clientSock.sendall('s')

                print("[%s] client(%s) is connecting" %(ctime(), addr_info[0]))
                ## reply to client ##
                for socket_in_list in connection_list:
                    if socket_in_list != serverSock and socket_in_list != sock:
                        try:

                            print("new connection")
                        except Exception as e:
                            socket_in_list.close()
                            connection_list.remove(socket_in_list)
                            num_client -= 1

            ## client who are connecting send new data
            else:
                # print "??"
                # # ## start the commute
                # if start == True:
                #     sent = sock.send('s')
                #     if sent == 0:
                #         raise RuntimeError("Socket connection broken")
                # else:
                #     if raw_input() == 's':
                #         start != start
                #     continue

                if num_client == 2:
                    data = sock.recv(BUF_SIZE)
                else:
                    data= None

                if data:
                    print("[%s]data is given %s" % (ctime(), data))
                    frames.append(data)
                    for socket_in_list in connection_list:
                        if socket_in_list != serverSock and socket_in_list != sock:
                            try:
                                print(data)

                            except Exception as e:
                                print(e.message)
                                socket_in_list.close()
                                connection_list.remove(socket_in_list)
                                num_client -= 1
                                continue
                else:
                    connection_list.remove(sock)
                    num_client -= 1

                    wf = wave.open('ki.wav', 'wb')
                    wf.setnchannels(1)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(44100)
                    wf.writeframes(b''.join(frames))
                    wf.close()
                    sock.close()
                    print("the connection is closed")
    except KeyboardInterrupt:
        serverSock.close()
        sys.exit()