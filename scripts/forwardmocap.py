#!/usr/bin/env python3

import asyncio
import time
import mavsdk
from mavsdk import System
import numpy
import socket
import struct

from scipy.spatial.transform import Rotation

homeZ = 0
setHomeFlag = True


# Settings for ODROID connection
address_ODROID = "udp://:14560"

# Settings for Mocap connection
localIP     = "127.0.0.1"
localPort   = 12690
bufferSize  = 1024

NetMsgMat4_ID = 2807643820


# Create connection to Mocap network
async def createMocapUDPconnection():

    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))

    print("UDP server up and listening")

    return UDPServerSocket


# Create connection to PX4 through ODROID
async def createODROIDconnection():

    drone = System()
    await drone.connect(system_address=address_ODROID)

    #status_text_task = asyncio.ensure_future(print_status_text(drone))

    # Wait for drone connection
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    return drone


# Listen for incoming data from Mocap connection
def listenForIncomingData(UDPServerSocket, printtoggle):

    # Listen for message from socket
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    # Extract message and address
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    # clientMsg = "Message from Client:{}".format(message)
    # clientIP  = "Client IP Address:{}".format(address)
    # print(clientMsg)
    # print(clientIP)

    # Decode the message based on MsgName (int), payload (int), data
    netMsgID = int.from_bytes(message[0:4], 'big')
    payloadBytes = int.from_bytes(message[4:8], 'big')

    if (printtoggle):
        print("NetMsgID is ", netMsgID)

    return message, address, netMsgID, payloadBytes


# Parse NetMsgMat4 object
def parse_NetMsgMat4(message, printtoggle):

    if (printtoggle):
        print( "NetMsgMat4 arrived... Let's look inside" )

    mat4 = numpy.empty([4,4])
    unpack = struct.Struct(">d") #> means big endian
    i = 0
    for r, c in numpy.ndindex( mat4.shape ):
        f = unpack.unpack( bytes( message[8 + i*8 : 8+i*8 + 8] ) )
        # print( "f is", f[0] )
        mat4[c][r] = f[0]
        i = i + 1

    if (printtoggle):
        print(mat4)

    return mat4


# Convert Mat4 array to desired array of mocap values
#   Assumes mat4 format of:
#     [a00, a01, a02,   x;
#      a10, a11, a12,   y;
#      a20, a21, a22,   z;
#        0,   0,   0,   0];
def convertMat4toMocap(mat4):

    # Extract rotation matrix
    rotmat = Rotation.from_matrix(mat4[numpy.ix_([0, 1, 2], [0, 1, 2])])

    #print("Rotation matrix: ", rotmat)

    # Convert rotation matrix to Euler angles (rad)
    yaw, pitch, roll = rotmat.as_euler("ZYX", degrees=False)

    #print("Euler angles (rad): ", roll, ", ", pitch, ", ", yaw)

    global homeZ, setHomeFlag

    # if setHomeFlag:
    #     homeZ = mat4[2, 3]
    #     setHomeFlag = False

    # Return [x, y, z, roll, pitch, yaw]
    return numpy.array([mat4[0, 3], mat4[1, 3], mat4[2, 3] - homeZ, roll, pitch, yaw])


# Form MAVSDK Mocap Object from Mocap Data
def createMAVmocapObject(mocapData):

    # mocapData ENU to NED
    # TODO: CHANGE THIS TO FIT ACTUAL MOCAP FRAME
    n  =  mocapData[1]
    e  =  mocapData[0]
    d  = -mocapData[2]
    nr =  mocapData[4]
    ep =  mocapData[3]
    dy = -mocapData[5]  # + 3.14159

    # NED position vector
    posvec = numpy.array([n, e, d])

    # Attitude vector
    attvec = numpy.array([nr, ep, dy])

    # Default covariance matrix
    pose_covar = mavsdk.mocap.Covariance([float(0.1 ** 2), float(0), float(0), float(0), float(0), float(0),
                                          float(0.1 ** 2), float(0), float(0), float(0), float(0),
                                          float(0.1 ** 2), float(0), float(0), float(0),
                                          float(100), float(0), float(0),
                                          float(100), float(0),
                                          float(100)])

    # Position (m)
    position_body = mavsdk.mocap.PositionBody(float(posvec[0]), float(posvec[1]), float(posvec[2]))

    # Attitude (rad)
    angle_body = mavsdk.mocap.AngleBody(float(attvec[0]), float(attvec[1]), float(attvec[2]))

    # Return MAVSDK Mocap object
    return mavsdk.mocap.VisionPositionEstimate(0, position_body, angle_body, pose_covar)


# Send mocap data to ODROID
async def sendMocapData(drone, mocapData):

    # Create MAVSDK Mocap object from mocapData
    mocapObj = createMAVmocapObject(mocapData)

    # Send Mocap object to drone
    await drone.mocap.set_vision_position_estimate(mocapObj)


# Main script
async def main():

    # Print-to-screen frequency (Hz)
    printfreq = 10

    # Create a datagram socket
    UDPServerSocket = await createMocapUDPconnection()

    # Connect to ODROID
    drone = await createODROIDconnection()

    # Start time variables
    starttime_msg = time.time()
    starttime_print = starttime_msg

    # Continue to listen for incoming messages to forward to ODROID
    while True:

        endtime = time.time()

        # Listen for incoming messages
        message, address, netMsgID, payloadBytes = (
            listenForIncomingData(UDPServerSocket, False))

        # Message is NetMsgMat4
        if netMsgID == NetMsgMat4_ID:

            # Parse message into mat4 format
            mat4 = parse_NetMsgMat4(message, False)

            # Convert mat4 into mocap data array
            mocapData = convertMat4toMocap(mat4)


            # Send mocap data to ODROID
            try:
                await sendMocapData(drone, mocapData)
            except:
                print("ERROR SENDING MOCAP")
                continue


            # Print mocapData to console at set frequency
            if (endtime - starttime_print) > (1/printfreq):
                starttime_print = time.time()
                print(mocapData)


# (UNUSED) Print status updates from ODROID
async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


# Run main script
if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(main())
