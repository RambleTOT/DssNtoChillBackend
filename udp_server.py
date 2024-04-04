import socket

localIP = "10.42.0.1"
localPort = 3333
bufferSize = 1 << 15

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
counter = 0
data = []
# Listen for incoming datagrams
while (True):
    if counter <= 5:
        message, address = UDPServerSocket.recvfrom(bufferSize)
        list_raw_data = list(message)
        print(len(data))
    else:
        # print(f'{len(data)}_else')
        print(data)
        data = []
        counter = 0

    counter += 1
    # print(len(list_raw_data))
    for i in range(0, len(list_raw_data), 2):
        num = (list_raw_data[i + 1] << 8 | list_raw_data[i]) & 0xFFF
        # print(num)
        data.append(num)

