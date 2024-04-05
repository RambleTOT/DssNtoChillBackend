import base64
import io
import socket
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_RATE = 40000  # Гц
DURATION = 5  # Секунды

START_FREQ = 100
END_FREQ = 18000

localIP = "192.168.239.178"
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
    if counter <= 30:
        message, address = UDPServerSocket.recvfrom(bufferSize)
        list_raw_data = list(message)
    else:
        t = np.arange(0, len(data) / SAMPLE_RATE, 1 / SAMPLE_RATE)
        signal = np.array(data, dtype=np.float64)
        signal = signal / 4095 * 2 - 1
        mean_value = np.mean(data)
        median_value = np.median(data)
        min_value = np.min(data)
        max_value = np.max(data)
        #noise_db = 10 * np.log10(np.mean(data ** 2))
        std_deviation = np.std(data)

        fft_result = 2 * np.abs(np.fft.rfft(signal)) / len(signal)
        freq = np.fft.rfftfreq(len(signal), d=1 / SAMPLE_RATE)

        start_index = np.argmax(freq >= START_FREQ)
        end_index = np.argmax(freq >= END_FREQ)

        # Отображение спектра в заданном диапазоне частот
        plt.figure(figsize=(10, 6))
        plt.plot(freq[start_index:end_index], fft_result[start_index:end_index])
        plt.title('Spectrum from 100 Hz to 18000 Hz')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.grid(True)

        # Сохраняем график в формате изображения
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Преобразуем изображение в строку byte64
        image_byte64_ = base64.b64encode(buffer.read()).decode('utf-8')

        print(max_value)

        data = []
        counter = 0
    # print(f"Message from Client:{message}")
    # print(f"Client IP Address:{address}")
    counter += 1
    for i in range(0, len(list_raw_data), 2):
        num = (list_raw_data[i+1] << 8 | list_raw_data[i]) & 0xFFF
        data.append(num)
