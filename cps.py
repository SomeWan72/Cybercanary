import socket


def complete_port_scanner(detection_queue, comm_cut_queue, s):
    s.listen()

    while comm_cut_queue.empty():
        try:
            s.accept()
            detection_queue.put("Se está detectando un escaneo de puertos.")
        except socket.timeout:
            pass

    s.shutdown(0)
    s.close()
