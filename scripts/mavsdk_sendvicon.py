#!/usr/bin/env python3

import asyncio
import time
import mavsdk
from mavsdk import System
import numpy

import argparse

def createViconData(counter):

    #enu = [0, 0, 5]



    defaultEast = 0.0
    defaultNorth = 0.0
    defaultUp = 0.0

    # Define optional input altitude
    parser = argparse.ArgumentParser()
    parser.add_argument("enu_east",  nargs='?', type=float, default=defaultEast)
    parser.add_argument("enu_north", nargs='?', type=float, default=defaultNorth)
    parser.add_argument("enu_up",    nargs='?', type=float, default=defaultUp)
    args = parser.parse_args()

    enu = [args.enu_east, args.enu_north, args.enu_up]

    # Wait 10 seconds, then takeoff to altitude in 5 seconds
    if 400 < counter < 600:
        enu[2] = enu[2] * (counter-400) / 200
    elif counter >= 600:
        enu[2] = enu[2]
    else:
        enu[2] = defaultUp


    n =  enu[1]
    e =  enu[0]
    d = -enu[2]

    tvecs = numpy.array([n, e, d]) * 1000

    pose_covar = mavsdk.mocap.Covariance([float(0.1 ** 2), float(0), float(0), float(0), float(0), float(0),
                                          float(0.1 ** 2), float(0), float(0), float(0), float(0),
                                          float(0.1 ** 2), float(0), float(0), float(0),
                                          float(100), float(0), float(0),
                                          float(100), float(0),
                                          float(100)])

    position_body = mavsdk.mocap.PositionBody(float(tvecs[0]) / 1000.0, float(tvecs[1]) / 1000.0,
                                              float(tvecs[2]) / 1000.0)

    angle_body = mavsdk.mocap.AngleBody(float(0), float(0), float(0))

    vision_pos_estimate = mavsdk.mocap.VisionPositionEstimate(0, position_body, angle_body, pose_covar)

    return vision_pos_estimate


async def sendViconData():

    # Message frequency (Hz)
    freq = 40
    printfreq = 10

    drone = System()
    #await drone.connect(system_address="udp://:14540")
    await drone.connect(system_address="udp://:14560")

    #status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    start = time.time()
    start2 = start

    # viconData = createViconData()

    counter = 0

    while True:
        end = time.time()
        if (end - start) > (1/freq):

            start = time.time()

            counter = counter + 1

            print(f"COUNTER: {counter}")

            viconData = createViconData(counter)

            try:
                await drone.mocap.set_vision_position_estimate(viconData)
            except:
                print("ERROR SENDING VICON")
                continue

            if (end - start2) > (1/printfreq):
                start2 = time.time()
                print(f"{viconData}")


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(sendViconData())
