import time
import socket


def complete_port_scanner(detection_queue, s, ip, port):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen()

    while True:
        s.accept()
        detection_queue.put("Se está detectando un escaneo de puertos.")
