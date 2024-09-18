#!/usr/bin/python3


from multiprocessing import Process
import subprocess


# Forms IP:port or path:baud strings
def pathstr(part1, part2):
    return part1 + ":" + str(part2)


# Runs mavlink-router to form the connections
def runmavrouter():

    GCS_IP = "192.168.137.1"
    GCS_port1 = 14550
    GCS_port2 = 14560
    GCS_port3 = 14570

    FC_path = "/dev/ttyUSB0"
    FC_baud = 921600

    GCS_str1 = pathstr(GCS_IP, GCS_port1)
    GCS_str2 = pathstr(GCS_IP, GCS_port2)
    GCS_str3 = pathstr(GCS_IP, GCS_port3)
    FC_str = pathstr(FC_path, FC_baud)

    print("GCS_str1: ", GCS_str1)
    print("GCS_str2: ", GCS_str2)
    print("GCS_str3: ", GCS_str3)
    print("FC_str: ", FC_str)

    subprocess.run(["mavlink-routerd", "-e", GCS_str1, "-e", GCS_str2, "-e", GCS_str3, FC_str])


# Main program
if __name__ == '__main__':

    process1 = Process(target=runmavrouter)
    process1.start()

