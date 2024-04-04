# Модуль socket для сетевого программирования
from socket import *
import numpy as np

import math
import wave

# данные сервера
host = '10.42.0.1'
port = 3333
addr = (host, port)

# socket - функция создания сокета
# первый параметр socket_family может быть AF_INET или AF_UNIX
# второй параметр socket_type может быть SOCK_STREAM(для TCP) или SOCK_DGRAM(для UDP)
udp_socket = socket(AF_INET, SOCK_DGRAM)
# bind - связывает адрес и порт с сокетом
udp_socket.bind(addr)

data = []
try:
    # Бесконечный цикл работы программы
    while True:
        data_bytes = []
        # print('wait data...')

        # recvfrom - получает UDP сообщения
        conn, addr = udp_socket.recvfrom(1 << 15)
        # print(f'addr:{addr} len:{len(conn)} data:{conn}')
        data_bytes = list(conn)
        # print(data_bytes)
        for i in range(0, len(data_bytes), 2):
            num = (data_bytes[i + 1] << 8) | (data_bytes[i] & 0xF)
            print(num)
            data.append(num)
        # sendto - передача сообщения UDP
        # udp_socket.sendto(b'message received by the server', addr)
finally:
    with wave.open("file.wav", 'wb') as file:
        file.setnchannels(1)
        # 2 bytes per sample.
        file.setsampwidth(2)
        file.setframerate(20_000)
        file.writeframes(data.tobytes())
    udp_socket.close()
