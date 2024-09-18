#!/usr/bin/env python3

import asyncio
from mavsdk import System
from datetime import datetime

async def run():

    drone = System()
    #await drone.connect(system_address="udp://:14550")
    #await drone.connect(system_address="udp:192.168.137.1:4550")
    await drone.connect(system_address="udp://:14550")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        print(state)
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    async for status_text in drone.telemetry.status_text():
        current = datetime.now();
        str1 = f"[{status_text.type}]";
        print(f"{current}: {str1: <12} {status_text.text}")


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
