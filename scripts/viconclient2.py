import socket

# UDP connection info
IP = ''
PORT = 13000


# Connect to UDP address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((IP, PORT))


while True:

    message, address = server_socket.recvfrom(1024)

    print(message.decode('utf-8'))
