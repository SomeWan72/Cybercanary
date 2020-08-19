def complete_port_scanner(detection_queue, comm_cut_queue, s):
    s.listen()

    while comm_cut_queue.empty():
        s.accept()
        detection_queue.put("Se está detectando un escaneo de puertos.")

    s.close()
