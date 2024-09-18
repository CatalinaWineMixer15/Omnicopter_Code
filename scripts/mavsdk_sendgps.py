
import asyncio

import time

import mavsdk
from mavsdk import System

async def thing1():
	drone = System()
	await drone.connect(system_address="udp://:14550")

	status_text_task = asyncio.ensure_future(print_status_text(drone))

	print("Waiting for drone to connect...")
	async for state in drone.core.connection_state():
		if state.is_connected:
			print(f"-- Connected to drone!")
			break

	start1 = time.time();
	start2 = time.time();
	

	while True:
		end = time.time();
		if (end-start2) > 0.1:
			print(f"Sending GPS data")

			rawgps = GetRawGps(start1);
			
			print(f"{rawgps}")

			await drone.telemetry_server.publish_raw_gps(rawgps, GetGpsInfo(drone))
			start2 = time.time();
		
		


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return




def GetRawGps(starttime):

	lat = 47.397746399999996
	lat = 47.3978
	#lon = 8.545612
	lon = 8.545
	alt = 488.1100158691406
	cog_deg = 164.55999755859375
	cog_deg = 0

	#telem = Telemetry();

	currenttime = time.time();

	gpstime = (currenttime - starttime)*1000000;

	return mavsdk.telemetry.RawGps(int(gpstime), lat, lon, alt, 0.0, 0.0, 0.0, cog_deg, alt, 1.0, 1.0, 0.25, 0.0, 0.0);

	# RawGps(time.time(), latitude_deg, longitude_deg, absolute_altitude_m, hdop, vdop, velocity_m_s, cog_deg, altitude_ellipsoid_m, horizontal_uncertainty_m, vertical_uncertainty_m, velocity_uncertainty_m_s, heading_uncertainty_deg, yaw_deg)



def GetGpsInfo(drone):

	num_satellites = 7;

	fixtypeenum = 3;
	#fixtypeenum = 0;

	fix_type = mavsdk.telemetry_server.FixType(fixtypeenum);

	return mavsdk.telemetry_server.GpsInfo(num_satellites, fix_type);





if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(thing1())
