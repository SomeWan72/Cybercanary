import socket
import struct
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


def partial_port_scanner(detection_queue, comm_cut_queue, s, ip_list):
    suspects = dict()
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

                version = ip_header[0] >> 4
                ihl = ip_header[0] & 0xF

                ip_length = ihl * 4
                ip_protocol = ip_header[6]
                source_address = socket.inet_ntoa(ip_header[8])
                destination_address = socket.inet_ntoa(ip_header[9])

                if IP(source_address).iptype() != 'PRIVATE' and IP(source_address) not in ip_list:
                    if ip_protocol == 6:
                        tcp_start = ip_length + eth_length
                        tcp_char = packet[tcp_start:tcp_start + 20]
                        tcp_header = struct.unpack('!HHLLBBHHH', tcp_char)

                        source_port = tcp_header[0]
                        destination_port = tcp_header[1]
                        sequence = tcp_header[2]
                        ack = tcp_header[3]
                        flags = get_flags(tcp_header[5])

                        if flags[4] == "SYN":
                            if source_address not in suspects:
                                suspects[source_address] = 0

                            suspects[source_address] += 1

                            if suspects[source_address] > 20:
                                detection_queue.put("Escaneo de puertos detectado desde " + source_address)

                        else:
                            detection_queue.put(
                                "Paquete TCP enviado desde " + source_address + " al puerto " + str(destination_port))

                    elif ip_protocol == 17:
                        udp_start = ip_length + eth_length
                        udp_char = packet[udp_start:udp_start + 8]
                        udp_header = struct.unpack('!HHHH', udp_char)

                        source_port = udp_header[0]
                        destination_port = udp_header[1]
                        length = udp_header[2]
                        checksum = udp_header[3]

                        detection_queue.put(
                            "Paquete UDP enviado desde " + source_address + " al puerto " + str(destination_port))

                    elif ip_protocol == 1:
                        icmp_start = ip_length + eth_length
                        icmp_char = packet[icmp_start: icmp_start + 4]
                        icmp_header = struct.unpack('!BBH', icmp_char)

                        icmp_type = icmp_header[0]
                        code = icmp_header[0]
                        checksum = icmp_header[0]

                        detection_queue.put("Paquete ICMP enviado desde " + source_address)

        except socket.timeout:
            pass

    s.close()
