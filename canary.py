from multiprocessing import Process, Queue
import socket
from cps import complete_port_scanner
from pps import partial_port_scanner
from observer import observer
from IPy import IP


if __name__ == '__main__':
    ip = "192.168.1.66"
    port_cps = 11944

    cps_socket = socket.socket()
    pps_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    f = open("ip.txt", "r")
    ip_list = list()

    for line in f:
        ip_list.append(IP(line))

    f.close()

    detection_queue = Queue()
    com_cut_queue = Queue()

    cps_process = Process(target=complete_port_scanner, args=(detection_queue, com_cut_queue, cps_socket, ip, port_cps))
    pps_process = Process(target=partial_port_scanner, args=(detection_queue, com_cut_queue, pps_socket, ip_list))
    vig_process = Process(target=observer, args=(detection_queue, com_cut_queue))

    cps_process.start()
    pps_process.start()
    vig_process.start()
    cps_process.join()
    pps_process.join()
    vig_process.join()
