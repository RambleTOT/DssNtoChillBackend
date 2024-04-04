import socket

localIP = "192.168.43.36"
localPort = 3333
bufferSize = 1 << 15

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
counter = 0

# Listen for incoming datagrams
while (True):

    message, address = UDPServerSocket.recvfrom(bufferSize)
    list_raw_data = list(message)
    # print(f"Message from Client:{message}")
    # print(f"Client IP Address:{address}")

    data = []
    for i in range(0, len(list_raw_data), 2):
        num = (list_raw_data[i+1] << 12 | list_raw_data[i] << 4) & 0xFFFF
        print(hex(num))
        data.append(num)
