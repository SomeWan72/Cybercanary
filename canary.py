#!/usr/bin/python

from multiprocessing import Process, Queue
import subprocess
import socket
from cps import complete_port_scanner
from pps import partial_port_scanner
from observer import observer
from decoy import decoy
from IPy import IP


if __name__ == '__main__':
    ip = subprocess.run("hostname -I", shell=True, capture_output=True, text=True).stdout.strip()
<<<<<<< HEAD
    socket.setdefaulttimeout(1)
=======
    port_cps = 11944

    # subprocess.run("iptables -t nat -A PREROUTING -d " + ip + "/32 -p tcp -m tcp --dport 22 -j ACCEPT", shell=True)
    # subprocess.run("iptables -t nat -A PREROUTING -d " + ip +
    #               "/32 -p tcp -m tcp --dport 1:65535 -j DNAT --to-destination " + ip + ":" + str(port_cps), shell=True)

    socket.setdefaulttimeout(1)

    # cps_socket = socket.socket()
    # cps_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # cps_socket.bind((ip, port_cps))
>>>>>>> 70f60a12067e16e973c375ab2fb5f93a98e33b5e
    pps_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    with open("ip.txt", "r") as f:
        ip_list = list()
        ip_list.append(IP(ip))

        for line in f:
            ip_list.append(IP(line))

    detection_queue = Queue()
    comm_cut_queue = Queue()

<<<<<<< HEAD
=======
    # cps_process = Process(target=complete_port_scanner, args=(detection_queue, comm_cut_queue, cps_socket))
>>>>>>> 70f60a12067e16e973c375ab2fb5f93a98e33b5e
    pps_process = Process(target=partial_port_scanner, args=(detection_queue, comm_cut_queue, pps_socket, ip_list))
    obs_process = Process(target=observer, args=(detection_queue, comm_cut_queue, ip_list))
    dec_process = Process(target=decoy)

<<<<<<< HEAD
=======
    # cps_process.start()
>>>>>>> 70f60a12067e16e973c375ab2fb5f93a98e33b5e
    pps_process.start()
    obs_process.start()
    dec_process.start()

<<<<<<< HEAD
=======
    # cps_process.join()
>>>>>>> 70f60a12067e16e973c375ab2fb5f93a98e33b5e
    pps_process.join()
    obs_process.join()
    dec_process.join()

<<<<<<< HEAD
=======
    # cps_process.close()
>>>>>>> 70f60a12067e16e973c375ab2fb5f93a98e33b5e
    pps_process.close()
    obs_process.close()
    dec_process.close()
