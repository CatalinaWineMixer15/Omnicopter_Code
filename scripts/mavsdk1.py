
import asyncio

from mavsdk import System

async def thing1():
	drone = System()
	await drone.connect(system_address="udp://:14540")



if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(thing1())
