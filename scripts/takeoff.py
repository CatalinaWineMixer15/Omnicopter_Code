#!/usr/bin/env python3

import asyncio
from mavsdk import System
import argparse


async def run():

    defaultAlt = 10

    # Define optional input altitude
    parser = argparse.ArgumentParser()
    parser.add_argument("alt", nargs='?', type=float, default=defaultAlt)
    args = parser.parse_args()

    if args.alt < 0:
        args.alt = defaultAlt



    drone = System()
    await drone.connect(system_address="udp://:14570")
    # # await drone.connect(system_address="udp://:4000")
    # await drone.connect(system_address="udp://:14540")

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        break
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print(f"-- Taking off for altitude: {args.alt} m")
    await drone.action.set_takeoff_altitude(args.alt)
    await drone.action.takeoff()

    await asyncio.sleep(5)

    await drone.action.land()

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
