import random
import socket
import time


# Inputs
delaysec = 1.0      # Delay (seconds)
scale = 10;         # Position scaler
timeoutsec = 5.0    # Timeout (seconds)
delayscale = 2;

# UDP connection info
IP = ''
PORT = 12000



# Create address
addr = ("127.0.0.1", PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(timeoutsec)

# Initial start time
starttime = time.monotonic()


while True:

    start = time.time()

    delaysec = random.random() * delayscale

    # Generate random position data
    x = scale * random.random()
    y = scale * random.random()
    z = scale * random.random()

    xyzstr = f'X: {x}, Y: {y}, Z: {z}'

    # Send data
    print(xyzstr)

    #message = b'X: {x}, Y: {y}, Z: {z}'

    message = xyzstr.encode('utf-8')

    client_socket.sendto(message, addr)

    # Delay
    time.sleep(delaysec - ((time.monotonic() - starttime) % delaysec))
