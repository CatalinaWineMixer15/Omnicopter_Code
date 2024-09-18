"""
Example of how to connect to the autopilot by using mavproxy's
--udpin:0.0.0.0:9000 endpoint from the companion computer itself
"""

# Disable "Bare exception" warning
# pylint: disable=W0702

import time
# Import mavutil
from pymavlink import mavutil

def wait_conn():
    """
    Sends a ping to stabilish the UDP communication and awaits for a response
    """
    msg = None
    while not msg:
        #master.mav.ping_send(
        #    int(time.time() * 1e6), # Unix time in microseconds
        #    0, # Ping number
        #    0, # Request ping of all systems
        #    0 # Request ping of all components
        #)
        
        master.mav.param_set_send(
            master.target_system, master.target_component,
            b'GPS_TYPE',
            14,
            mavutil.mavlink.MAV_PARAM_TYPE_REAL32
        )

        master.mav.gps_input_send(
            0,  # Timestamp (micros since boot or Unix epoch)
            0,  # ID of the GPS for multiple GPS inputs
            # Flags indicating which fields to ignore (see GPS_INPUT_IGNORE_FLAGS enum).
            # All other fields must be provided.
            (mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VEL_HORIZ |
             mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_VEL_VERT |
             mavutil.mavlink.GPS_INPUT_IGNORE_FLAG_SPEED_ACCURACY),
            0,  # GPS time (milliseconds from start of GPS week)
            0,  # GPS week number
            3,  # 0-1: no fix, 2: 2D fix, 3: 3D fix. 4: 3D with DGPS. 5: 3D with RTK
            0,  # Latitude (WGS84), in degrees * 1E7
            0,  # Longitude (WGS84), in degrees * 1E7
            0,  # Altitude (AMSL, not WGS84), in m (positive for up)
            1,  # GPS HDOP horizontal dilution of position in m
            1,  # GPS VDOP vertical dilution of position in m
            0,  # GPS velocity in m/s in NORTH direction in earth-fixed NED frame
            0,  # GPS velocity in m/s in EAST direction in earth-fixed NED frame
            0,  # GPS velocity in m/s in DOWN direction in earth-fixed NED frame
            0,  # GPS speed accuracy in m/s
            0,  # GPS horizontal accuracy in m
            0,  # GPS vertical accuracy in m
            7   # Number of satellites visible.
        )

        msg = master.recv_match()
        time.sleep(0.5)

# Create the connection
#  Companion is already configured to allow script connections under the port 9000
# Note: The connection is done with 'udpout' and not 'udpin'.
#  You can check in http:192.168.1.2:2770/mavproxy that the communication made for 9000
#  uses a 'udp' (server) and not 'udpout' (client).
master = mavutil.mavlink_connection('udpout:0.0.0.0:14540')

# Send a ping to start connection and wait for any reply.
#  This function is necessary when using 'udpout',
#  as described before, 'udpout' connects to 'udpin',
#  and needs to send something to allow 'udpin' to start
#  sending data.
wait_conn()

# Get some information !
while True:
    try:
        print(master.recv_match().to_dict())
    except:
        pass
    time.sleep(0.1)

# Output:
# {'mavpackettype': 'AHRS2', 'roll': -0.11364290863275528, 'pitch': -0.02841472253203392, 'yaw': 2.0993032455444336, 'altitude': 0.0, 'lat': 0, 'lng': 0}
# {'mavpackettype': 'AHRS3', 'roll': 0.025831475853919983, 'pitch': 0.006112074479460716, 'yaw': 2.1514968872070312, 'altitude': 0.0, 'lat': 0, 'lng': 0, 'v1': 0.0, 'v2': 0.0, 'v3': 0.0, 'v4': 0.0}
# {'mavpackettype': 'VFR_HUD', 'airspeed': 0.0, 'groundspeed': 0.0, 'heading': 123, 'throttle': 0, 'alt': 3.129999876022339, 'climb': 3.2699999809265137}
# {'mavpackettype': 'AHRS', 'omegaIx': 0.0014122836291790009, 'omegaIy': -0.022567369043827057, 'omegaIz': 0.02394154854118824, 'accel_weight': 0.0, 'renorm_val': 0.0, 'error_rp': 0.08894175291061401, 'error_yaw': 0.0990816056728363}
