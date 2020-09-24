import socket
import struct
import subprocess
import time
from IPy import IP


def get_flags(packet):
    URG_F = {0: "", 1: "URG"}
    ACK_F = {0: "", 1: "ACK"}
    PSH_F = {0: "", 1: "PSH"}
    RST_F = {0: "", 1: "RST"}
    SYN_F = {0: "", 1: "SYN"}
    FIN_F = {0: "", 1: "FIN"}

    URG = packet & 0x020
    URG >>= 5
    ACK = packet & 0x010
    ACK >>= 4
    PSH = packet & 0x008
    PSH >>= 3
    RST = packet & 0x004
    RST >>= 2
    SYN = packet & 0x002
    SYN >>= 1
    FIN = packet & 0x001
    FIN >>= 0

    flags = [URG_F[URG], ACK_F[ACK], PSH_F[PSH], RST_F[RST], SYN_F[SYN], FIN_F[FIN]]
    return flags


def detectors(detection_queue, comm_cut_queue, reset_iptables_queue, s, ip_list):
    suspects = dict()
    suspects_time = dict()
    while comm_cut_queue.empty():
        try:
            packet = s.recvfrom(65565)
            packet = packet[0]

            eth_length = 14
            eth_char = packet[:eth_length]
            eth_header = struct.unpack('!6s6sH', eth_char)
            eth_protocol = socket.ntohs(eth_header[2])

            if eth_protocol == 8:
                ip_char = packet[eth_length:eth_length + 20]
                ip_header = struct.unpack('!BBHHHBBH4s4s', ip_char)

                ihl = ip_header[0] & 0xF

                ip_length = ihl * 4
                ip_protocol = ip_header[6]
                source_address = socket.inet_ntoa(ip_header[8])

                if IP(source_address) not in ip_list:
                    if ip_protocol == 6:
                        tcp_start = ip_length + eth_length
                        tcp_char = packet[tcp_start:tcp_start + 20]
                        tcp_header = struct.unpack('!HHLLBBHHH', tcp_char)

                        destination_port = tcp_header[1]
                        flags = get_flags(tcp_header[5])

                        if IP(source_address).iptype() != 'PRIVATE':
                            detection_queue.put(
                                "Paquete TCP enviado desde " + source_address + " al puerto " + str(destination_port))

                        else:
                            if flags[4] == "SYN":
                                if source_address not in suspects:
                                    suspects[source_address] = 0
                                    suspects_time[source_address] = time.time()

                                suspects[source_address] += 1

                                if suspects[source_address] == 50:
                                    detection_queue.put("Escaneo de puertos detectado desde " + source_address)
                                elif suspects_time[source_address] + 5 < time.time():
                                    del suspects[source_address]
                                    del suspects_time[source_address]

                    elif IP(source_address).iptype() != 'PRIVATE' and ip_protocol == 17:
                        udp_start = ip_length + eth_length
                        udp_char = packet[udp_start:udp_start + 8]
                        udp_header = struct.unpack('!HHHH', udp_char)

                        destination_port = udp_header[1]

                        detection_queue.put(
                            "Paquete UDP enviado desde " + source_address + " al puerto " + str(destination_port))

                    elif IP(source_address).iptype() != 'PRIVATE' and ip_protocol == 1:
                        detection_queue.put("Paquete ICMP enviado desde " + source_address)

        except socket.timeout:
            pass

    subprocess.run("iptables -A INPUT -j DROP", shell=True)
    reset_iptables_queue.put("RESET")
    s.close()
