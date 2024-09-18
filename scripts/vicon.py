import socket
import time
import json
import numpy
from numpy import random


# Inputs
delaysec = 1.0      # Delay (seconds)
scale = 10;         # Position scaler
scale2 = 1;         # Velocity scaler
timeoutsec = 5.0    # Timeout (seconds)
delayscale = 2;

# UDP connection info
IP = ''
PORT = 12000



# Create address
addr = ("127.0.0.1", PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(timeoutsec)


def sendXYZV():

    # Generate random position data
    pos = scale * random.rand(3)
    vel = scale2 * random.rand(3)

    #xyzstr = f'X: {x}, Y: {y}, Z: {z}, Vx: {vx}, Vy: {vy}, Vz: {vz}'

    ## Send data
    #print(xyzstr)

    #message = b'X: {x}, Y: {y}, Z: {z}'

    #message = xyzstr.encode('utf-8')

    data = json.dumps({"X": pos[0], "Y": pos[1], "Z": pos[2], "Vx": vel[0], "Vy": vel[1], "Vz": vel[2]})

    fullarray = numpy.concatenate((pos,vel))

    print(fullarray)

    #posstr = numpy.array2string(pos)
    #velstr = numpy.array2string(vel)

    #data = json.dumps({"pos": posstr, "vel": velstr})

    message = data.encode()

    client_socket.sendto(message, addr)



# Initial start time
starttime = time.monotonic()


while True:

    start = time.time()

    delaysec = random.random() * delayscale

    sendXYZV()

    # Delay
    time.sleep(delaysec - ((time.monotonic() - starttime) % delaysec))
