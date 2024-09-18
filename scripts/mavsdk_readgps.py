
import asyncio
import time
from mavsdk import System

async def thing1():
	drone = System()
	#await drone.connect(system_address="udp://:14550")
	await drone.connect(system_address="udp://:3000")

	#auto pos = drone.telemetry.position_velocity_ned()

	start1 = time.time();
	start2 = time.time();

#	async for position in drone.telemetry.position():
#		end = time.time();
#		if (end-start1) > 0.1:
#			print(f"Position info: {position.absolute_altitude_m: <18} m")
#			start1 = time.time();


	async for rawgps in drone.telemetry.raw_gps():
		end = time.time();
		print(end);
		if (end-start2) > 0.1:
			#print(f"GPS info: {rawgps: <18}")
			print(f"{rawgps}")
			start2 = time.time();

		#await asyncio.sleep(0.1)

def thing2():

	lat = 47.397746399999996;
	lon = 8.545612;
	alt = 488.1100158691406;
	cog_deg = 164.55999755859375;

	return RawGps(time.time(), lat, lon, alt, 0.0, 0.0, 0.0, cog_deg, alt, 1.0, 1.0, 0.25, 0.0, 0.0);

	# RawGps(time.time(), latitude_deg, longitude_deg, absolute_altitude_m, hdop, vdop, velocity_m_s, cog_deg, altitude_ellipsoid_m, horizontal_uncertainty_m, vertical_uncertainty_m, velocity_uncertainty_m_s, heading_uncertainty_deg, yaw_deg)



if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(thing1())
