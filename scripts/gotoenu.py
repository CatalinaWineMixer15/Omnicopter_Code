#!/usr/bin/env python3

import asyncio
import mavsdk
from mavsdk import System
import argparse
import math

import pymap3d

import pprint


def lla2enu(lla):
    return pymap3d.geodetic2enu(lla[0], lla[1], lla[2])


def enu2ned(enu):
    n  =  enu[1]
    e  =  enu[0]
    d  = -enu[2]
    return n, e, d


async def run():

    drone = System()
    await drone.connect(system_address="udp://:14570")
    # await drone.connect(system_address="udp://:14540")

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    defaultEast = 0.0
    defaultNorth = 0.0
    defaultUp = 0.0
    defaultYaw = 0.0  # deg

    # Define optional input altitude
    parser = argparse.ArgumentParser()
    parser.add_argument("enu_east",  nargs='?', type=float, default=defaultEast)
    parser.add_argument("enu_north", nargs='?', type=float, default=defaultNorth)
    parser.add_argument("enu_up",    nargs='?', type=float, default=defaultUp)
    parser.add_argument("enu_yaw",   nargs='?', type=float, default=defaultYaw)
    args = parser.parse_args()

    print("Inputs: East: ", args.enu_east, ", North: ", args.enu_north, ", Up: ", args.enu_up, ", Yaw: ", args.enu_yaw)

    """
    if args.enu_east < 0:
        args.enu_east = defaultEast
    if args.enu_north < 0:
        args.enu_north = defaultNorth
    if args.enu_up < 0:
        args.enu_up = defaultUp
    """

    # Convert home position to ENU
    #home_enu = lla2enu(home_lla)
    home_enu = [0, 0, 0]

    # Create new ENU position using inputs relative to home position
    newpos_enu = [home_enu[0] + args.enu_east, home_enu[1] + args.enu_north, home_enu[2] + args.enu_up]

    # Convert new position to NED
    [north_m, east_m, down_m] = enu2ned(newpos_enu)

    print(north_m, ", ", east_m, ", ", down_m)

    print("-- Arming")
    await drone.action.arm()

    # Sending command to drone
    print("-- Going to new position")
    #await drone.action.goto_location(newpos_lla[0], newpos_lla[1], newpos_lla[2], yaw_deg)

    #pprint.pp(dir(mavsdk))

    posnedy = mavsdk.offboard.PositionNedYaw(north_m, east_m, down_m, args.enu_yaw)

    pprint.pp(posnedy)

    await drone.offboard.set_position_ned(posnedy)

    await drone.offboard.start()

    await asyncio.sleep(5)

    #await drone.offboard.stop()


    [n, e, d] = enu2ned(home_enu)
    homenedy = mavsdk.offboard.PositionNedYaw(n, e, d, 0)

    #await drone.offboard.set_position_ned(homenedy)

    await asyncio.sleep(5)

    # status_text_task.cancel()


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
