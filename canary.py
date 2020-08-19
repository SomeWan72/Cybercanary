from multiprocessing import Process, Queue
import subprocess
import socket
from cps import complete_port_scanner
from pps import partial_port_scanner
from observer import observer
from IPy import IP


if __name__ == '__main__':
    ip = "192.168.1.66"
    port_cps = 11944

    subprocess.run("iptables -t nat -A PREROUTING -d " + ip + "/32 -p tcp -m tcp --dport 22 -j ACCEPT", shell=True)
    subprocess.run("iptables -t nat -A PREROUTING -d " + ip +
                   "/32 -p tcp -m tcp --dport 1:65535 -j DNAT --to-destination " + ip + ":" + str(port_cps), shell=True)

    cps_socket = socket.socket()
    cps_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    cps_socket.bind((ip, port_cps))
    pps_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    f = open("ip.txt", "r")
    ip_list = list()

    for line in f:
        ip_list.append(IP(line))

    f.close()

    detection_queue = Queue()
    comm_cut_queue = Queue()

    cps_process = Process(target=complete_port_scanner, args=(detection_queue, comm_cut_queue, cps_socket))
    pps_process = Process(target=partial_port_scanner, args=(detection_queue, comm_cut_queue, pps_socket, ip_list))
    obs_process = Process(target=observer, args=(detection_queue, comm_cut_queue))

    cps_process.start()
    pps_process.start()
    obs_process.start()

    cps_process.join()
    pps_process.join()
    obs_process.join()

    cps_process.close()
    pps_process.close()
    obs_process.close()
