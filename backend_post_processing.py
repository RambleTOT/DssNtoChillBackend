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
    # Загрузка аудиофайла
    sample_rate, data = wav.read('audiofile.wav')
    sample_rate2, data2 = wav.read('audiofile-3.wav')

    # Анализ амплитудного спектра
    fft_out = np.fft.fft(data)
    amplitude_spectrum = 2 / len(data) * np.abs(fft_out[:len(data) // 2])

    fft_out_2 = np.fft.fft2(data2)
    amplitude_spectrum_2 = 2 / len(data2) * np.abs(fft_out_2[:len(data2) // 2])

    # Вычисление среднего, медианы, минимума и максимума
    mean_value = np.mean(data)
    median_value = np.median(data)
    min_value = np.min(data)
    max_value = np.max(data)

    mean_value_2 = np.mean(data2)
    median_value_2 = np.median(data2)
    min_value_2 = np.min(data2)
    max_value_2 = np.max(data2)

    # Оценка шума в дБ
    noise_db = 10 * np.log10(np.mean(data ** 2))
    noise_db_2 = 10 * np.log10(np.mean(data2 ** 2))

    # Стандартное квадратичное отклонение
    std_deviation = np.std(data)
    std_deviation_2 = np.std(data2)

    # Визуализация амплитудного спектра
    plt.plot(amplitude_spectrum)
    plt.title("Амплитудный спектр")
    plt.xlabel("Частота")
    plt.ylabel("Амплитуда")

    # Сохраняем график в формате изображения
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Преобразуем изображение в строку byte64
    image_byte64 = base64.b64encode(buffer.read()).decode('utf-8')

    # Визуализация амплитудного спектра
    plt.plot(amplitude_spectrum_2)
    plt.title("Амплитудный спектр")
    plt.xlabel("Частота")
    plt.ylabel("Амплитуда")

    # Сохраняем график в формате изображения
    buffer_2 = io.BytesIO()
    plt.savefig(buffer_2, format='png')
    buffer_2.seek(0)

    # Преобразуем изображение в строку byte64
    image_byte64_2 = base64.b64encode(buffer_2.read()).decode('utf-8')

    result = {
        'min': [str(min_value), str(min_value_2)],
        'max': [str(max_value), str(max_value_2)],
        'mean': [str(mean_value), str(mean_value_2)],
        'median': [str(median_value), str(median_value_2)],
        'noise': [str(noise_db), str(noise_db_2)],
        'std': [str(std_deviation), str(std_deviation_2)],
        'graph': [image_byte64, image_byte64_2]
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

