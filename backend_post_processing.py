import base64
import io
from flask import Flask, jsonify
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

app = Flask(__name__)


@app.route('/')
def get_statistics():
    # Загрузка аудиофайла
    sample_rate, data = wav.read('audiofile.wav')

    # Первый микрофон

    # Анализ амплитудного спектра
    fft_out = np.fft.fft(data)
    amplitude_spectrum = 2 / len(data) * np.abs(fft_out[:len(data) // 2])

    # Вычисление среднего, медианы, минимума и максимума
    mean_value = np.mean(data)
    median_value = np.median(data)
    min_value = np.min(data)
    max_value = np.max(data)

    # Оценка шума в дБ
    noise_db = 10 * np.log10(np.mean(data ** 2))

    # Стандартное квадратичное отклонение
    std_deviation = np.std(data)

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

    result = {
        'min': [str(min_value)],
        'max': [str(max_value)],
        'mean': [str(mean_value)],
        'median': [str(median_value)],
        'noise': [str(noise_db)],
        'std': [str(std_deviation)],
        'graph': [image_byte64]
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

