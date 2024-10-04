import socket
import threading
import time

server = input('H: ')
port = int(input('P: '))

def receive(client_socket):
    while True:
        recv = client_socket.recv(1024).decode()
        if not recv:
            break
        print(f'>',end=' ')
        for char in recv:
            print(char,end='',flush=True)
            time.sleep(0.03)
        print('\n')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server, port))
print('Connection Established with server!')
thread1 = threading.Thread(target=receive, args=(client_socket,))
thread1.start()

#Send
while True:
    send = input()
    client_socket.sendall(send.encode())
