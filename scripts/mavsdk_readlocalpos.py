import asyncio
import time
from mavsdk import System


async def thing1():
    drone = System()
    #await drone.connect(system_address="udp://:14550")
    await drone.connect(system_address="udp://:14550"
                                       "")

    #auto pos = drone.telemetry.position_velocity_ned()

    start1 = time.time()
    start2 = time.time()

    async for posvel in drone.telemetry.position_velocity_ned():
        position = posvel.position
        end = time.time()
        if (end - start1) > 0.1:
            print(f"Position info: {position.north_m: <18} m, {position.east_m: <18} m, {position.down_m: <18} m")
            start1 = time.time()


#
# async for rawgps in drone.telemetry.raw_gps():
# 	end = time.time();
# 	print(end);
# 	if (end-start2) > 0.1:
# 		#print(f"GPS info: {rawgps: <18}")
# 		print(f"{rawgps}")
# 		start2 = time.time();
#
# 	#await asyncio.sleep(0.1)


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(thing1())
