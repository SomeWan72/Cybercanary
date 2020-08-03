import socket


def complete_port_scanner(q, ip, port):
    s = socket.socket()
    s.bind((ip, port))
    s.listen()

    while True:
        (clientSocket, clientAddress) = s.accept()
        q.put("Se está detectando un escaneo de puerto.")
