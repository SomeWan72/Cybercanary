#!/usr/bin/python

from multiprocessing import Process, Queue
import subprocess
import socket
from detectors import detectors
from observer import observer
from decoy import decoy
from IPy import IP


if __name__ == '__main__':
    ip = subprocess.run("hostname -I", shell=True, capture_output=True, text=True).stdout.strip()
    socket.setdefaulttimeout(1)
    socket.setdefaulttimeout(1)
    detector_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    with open("ip.txt", "r") as f:
        ip_list = list()
        ip_list.append(IP(ip))

        for line in f:
            ip_list.append(IP(line))

    detection_queue = Queue()
    comm_cut_queue = Queue()

    det_process = Process(target=detectors, args=(detection_queue, comm_cut_queue, detector_socket, ip_list))
    obs_process = Process(target=observer, args=(detection_queue, comm_cut_queue, ip_list))
    dec_process = Process(target=decoy)

    det_process.start()
    obs_process.start()
    dec_process.start()

    det_process.join()
    obs_process.join()
    dec_process.join()

    det_process.close()
    obs_process.close()
    dec_process.close()
