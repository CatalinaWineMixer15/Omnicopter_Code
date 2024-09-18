import socket

import schedule
import time


from multiprocessing import Process
from time import sleep


# Inputs
sendsec = 1
currentstrfile = "currentstrfile.txt"

# UDP connection info
IP = ''
PORT = 12000

PORT2 = 13000





addr = ("127.0.0.1", PORT2)




def SET_CURRENT_STR(currentstr):
    global currentstrfile
    f = open(currentstrfile, "w")
    f.write(currentstr)
    f.close()

def GET_CURRENT_STR():
    global currentstrfile
    f = open(currentstrfile, "r")
    return f.read()






# Connect to UDP address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((IP, PORT))



#while True:
#
#    schedule.run_pending()
#
#    message, address = server_socket.recvfrom(1024)
#
#    currentstr = message.decode('utf-8')
#
#    print(currentstr)



def waitForPos():
    #global currentstr
    while True:

        message, address = server_socket.recvfrom(1024)


        currentstr = message.decode('utf-8')

        print(currentstr)

        SET_CURRENT_STR(currentstr)


def send_currentstr():

    # Initial start time
    starttime = time.monotonic()

    #print("SEND CURRENTSTR")

    a = 0

    while True:

        start = time.time()

        #global currentstr

        currentstr = GET_CURRENT_STR()

        print(currentstr + " - SENT")

        message = currentstr.encode('utf-8')

        #a = a + 1

        #teststr = f'TEST {a}'

        #print(teststr)
        #message = teststr.encode('utf-8')

        server_socket.sendto(message, addr)

        # Delay
        time.sleep(sendsec - ((time.monotonic() - starttime) % sendsec))


# Schedule the task to run every day at 7:00 AM
#schedule.every(sendsec).seconds.do(send_currentstr)


def sendPos():
    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == '__main__':

    proc1 = Process(target=waitForPos)
    proc1.start()

    proc2 = Process(target=send_currentstr)
    proc2.start()
