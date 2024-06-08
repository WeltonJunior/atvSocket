import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024)
            if message:
                print(message.decode('utf-8'))
            else:
                break
        except:
            break

def client(host='localhost', port=8082):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"Conectado ao servidor {host}:{port}")

    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == 'sair':
            sock.close()
            break
        sock.send(message.encode('utf-8'))

client()
