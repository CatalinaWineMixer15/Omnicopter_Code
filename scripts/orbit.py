#!/usr/bin/env python3

import asyncio
import mavsdk
from mavsdk import System
import argparse
import math


async def run():

    defaultAlt = 10

    # Define optional input altitude
    parser = argparse.ArgumentParser()
    parser.add_argument("alt", nargs='?', type=float, default=defaultAlt)
    args = parser.parse_args()

    if args.alt < 0:
        args.alt = defaultAlt;


    drone = System()
    await drone.connect(system_address="udp://:14540")

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    # Orbit parameters
    radius_m = 3
    velocity_ms = 1
    yaw_behavior = mavsdk.action.OrbitYawBehavior(mavsdk.action.OrbitYawBehavior.HOLD_FRONT_TO_CIRCLE_CENTER)
    latitude_deg = math.nan
    longitude_deg = math.nan
    absolute_altitude_m = math.nan

    print("-- Orbiting")
    await drone.action.do_orbit(radius_m, velocity_ms, yaw_behavior, latitude_deg, longitude_deg, absolute_altitude_m)

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
