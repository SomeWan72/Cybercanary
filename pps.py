import socket
import struct
from IPy import IP


def partial_port_scanner(q, ip_list):
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    while True:
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

                    q.put("Paquete TCP enviado desde " + source_address + " al puerto " + str(destination_port))
                    s.close()

                elif ip_protocol == 17:
                    udp_start = ip_length + eth_length
                    udp_char = packet[udp_start:udp_start+8]
                    udp_header = struct.unpack('!HHHH', udp_char)

                    source_port = udp_header[0]
                    destination_port = udp_header[1]
                    length = udp_header[2]
                    checksum = udp_header[3]

                    q.put("Paquete UDP enviado desde " + source_address + " al puerto " + str(destination_port))
                    s.close()

                elif ip_protocol == 1:
                    icmp_start = ip_length + eth_length
                    icmp_char = packet[icmp_start: icmp_start + 4]
                    icmp_header = struct.unpack('!BBH', icmp_char)

                    icmp_type = icmp_header[0]
                    code = icmp_header[0]
                    checksum = icmp_header[0]

                    q.put("Paquete ICMP enviado desde " + source_address)
                    s.close()
