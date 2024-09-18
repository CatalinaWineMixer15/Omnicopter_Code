
from multiprocessing import Process
import subprocess

# Forms IP:port strings
def ipportstr(IP, port):
    return IP + ":" + str(port)


# Runs mavlink-router to form the connections
def runmavrouter():

    GCS_IP = "192.168.137.1"
    GCS_port1 = 14550
    GCS_port2 = 14560
    GCS_port3 = 14570

    PX4_IP = "/dev/ttyUSB0"
    PX4_port = 921600

    GCS_str1 = ipportstr(GCS_IP, GCS_port1)
    GCS_str2 = ipportstr(GCS_IP, GCS_port2)
    GCS_str3 = ipportstr(GCS_IP, GCS_port3)
    PX4_str = ipportstr(PX4_IP, PX4_port)

    print("GCS_str1: ", GCS_str1)
    print("GCS_str2: ", GCS_str2)
    print("GCS_str3: ", GCS_str3)
    print("PX4_str: ", PX4_str)

    subprocess.run(["mavlink-routerd", "-e", GCS_str1, "-e", GCS_str2, "-e", GCS_str3, PX4_str])


if __name__ == '__main__':

    process1 = Process(target=runmavrouter)
    process1.start()

