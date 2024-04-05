import base64
import io
from flask import Flask, jsonify
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import socket


app = Flask(__name__)

@app.route('/')
def get_statistics():

    SAMPLE_RATE = 40000  # Гц
    DURATION = 5  # Секунды

    START_FREQ = 100
    END_FREQ = 18000

    localIP = "192.168.239.178"
    localPort1 = 3333
    localPort2 = 3334
    bufferSize = 1 << 15

    UDPServerSocket1 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket2 = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    UDPServerSocket1.bind((localIP, localPort1))
    UDPServerSocket2.bind((localIP, localPort2))

    print("UDP servers up and listening")

    counter1 = 0
    counter2 = 0
    data1 = []
    data2 = []

    while True:
        if counter1 <= 20 and counter2 <= 20:
            message, address = UDPServerSocket1.recvfrom(bufferSize)
            list_raw_data = list(message)
            for i in range(0, len(list_raw_data), 2):
                num = (list_raw_data[i + 1] << 8 | list_raw_data[i]) & 0xFFF
                data1.append(num)
            counter1 += 1

            message, address = UDPServerSocket2.recvfrom(bufferSize)
            list_raw_data = list(message)
            for i in range(0, len(list_raw_data), 2):
                num = (list_raw_data[i + 1] << 8 | list_raw_data[i]) & 0xFFF
                data2.append(num)
            counter2 += 1

        else:
            signal1 = np.array(data1, dtype=np.float64)
            signal2 = np.array(data2, dtype=np.float64)

            t1 = np.arange(0, len(data1) / SAMPLE_RATE, 1 / SAMPLE_RATE)
            t2 = np.arange(0, len(data2) / SAMPLE_RATE, 1 / SAMPLE_RATE)

            fft_result1 = 2 * np.abs(np.fft.rfft(signal1)) / len(signal1)
            fft_result2 = 2 * np.abs(np.fft.rfft(signal2)) / len(signal2)

            freq1 = np.fft.rfftfreq(len(signal1), d=1 / SAMPLE_RATE)
            freq2 = np.fft.rfftfreq(len(signal2), d=1 / SAMPLE_RATE)

            start_index1 = np.argmax(freq1 >= START_FREQ)
            end_index1 = np.argmax(freq1 >= END_FREQ)

            start_index2 = np.argmax(freq2 >= START_FREQ)
            end_index2 = np.argmax(freq2 >= END_FREQ)

            # Plot spectrum for signal 1
            plt.figure(figsize=(10, 6))
            plt.plot(freq1[start_index1:end_index1], fft_result1[start_index1:end_index1])
            plt.title('Spectrum from 100 Hz to 18000 Hz - Signal 1')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Magnitude')
            plt.grid(True)
            buffer1 = io.BytesIO()
            plt.savefig(buffer1, format='png')
            buffer1.seek(0)
            image_byte64_1 = base64.b64encode(buffer1.read()).decode('utf-8')

            # Plot spectrum for signal 2
            plt.figure(figsize=(10, 6))
            plt.plot(freq2[start_index2:end_index2], fft_result2[start_index2:end_index2])
            plt.title('Spectrum from 100 Hz to 18000 Hz - Signal 2')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Magnitude')
            plt.grid(True)
            buffer2 = io.BytesIO()
            plt.savefig(buffer2, format='png')
            buffer2.seek(0)
            image_byte64_2 = base64.b64encode(buffer2.read()).decode('utf-8')

            result = {
                'graph1': image_byte64_1,
                'graph2': image_byte64_2
            }

            data1 = []
            data2 = []
            counter1 = 0
            counter2 = 0
            return jsonify(result)