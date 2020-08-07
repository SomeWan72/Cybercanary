import time


def complete_port_scanner(detection_queue, com_cut_queue, s, ip, port):
    s.bind((ip, port))
    s.listen()

    while True:
        if not com_cut_queue.empty():
            s.close()
        elif s.accept():
            detection_queue.put("Se está detectando un escaneo de puertos.")
            time.sleep(1)
