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


def enu2lla(enu, home):
    return pymap3d.enu2geodetic(enu[0], enu[1], enu[2], home[0], home[1], home[2])


async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    # Get home position (LLA)
    async for home in drone.telemetry.position():
        print("home: ", home)
        home_lla = [home.latitude_deg, home.longitude_deg, home.absolute_altitude_m]
        #defaultUp = home.relative_altitude_m
        break

    defaultEast = 0.0
    defaultNorth = 0.0
    defaultUp = 0.0

    # Define optional input altitude
    parser = argparse.ArgumentParser()
    parser.add_argument("enu_east",  nargs='?', type=float, default=defaultEast)
    parser.add_argument("enu_north", nargs='?', type=float, default=defaultNorth)
    parser.add_argument("enu_up",    nargs='?', type=float, default=defaultUp)
    args = parser.parse_args()

    print("Inputs: East: ", args.enu_east, ", North: ", args.enu_north, ", Up: ", args.enu_up)

    """
    if args.enu_east < 0:
        args.enu_east = defaultEast
    if args.enu_north < 0:
        args.enu_north = defaultNorth
    if args.enu_up < 0:
        args.enu_up = defaultUp
    """

    #latitude_deg = 47.39769
    #longitude_deg = 8.54465
    #absolute_altitude_m = 492
    yaw_deg = 0

    # Convert home position to ENU
    #home_enu = lla2enu(home_lla)
    home_enu = [0, 0, 0]

    # Create new ENU position using inputs relative to home position
    newpos_enu = [home_enu[0] + args.enu_east, home_enu[1] + args.enu_north, home_enu[2] + args.enu_up]

    # Convert new position to LLA
    newpos_lla = enu2lla(newpos_enu, home_lla)

    print(newpos_lla)

    # Sending command to drone
    print("-- Going to new position")
    #await drone.action.goto_location(newpos_lla[0], newpos_lla[1], newpos_lla[2], yaw_deg)

    #pprint.pp(dir(mavsdk))

    alttype = mavsdk.offboard.PositionGlobalYaw.AltitudeType(2)

    posglobal = mavsdk.offboard.PositionGlobalYaw(newpos_lla[0], newpos_lla[1], newpos_lla[2], yaw_deg, alttype)

    pprint.pp(posglobal)

    await drone.offboard.set_position_global(posglobal)

    await asyncio.sleep(10)

    status_text_task.cancel()


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
