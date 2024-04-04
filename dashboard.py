import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import numpy as np
from scipy.io import wavfile
import plotly.graph_objs as go
import base64

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Button('Загрузить WAV файл'),
    ),
    html.Div(id='output-data'),
])


def process_wav_file(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    with open('temp.wav', 'wb') as f:
        f.write(decoded)

    sample_rate, data = wavfile.read('temp.wav')

    # Вычисление амплитудного спектра
    fft_result = np.fft.fft(data)
    amplitude_spectrum = 2 / len(data) * np.abs(fft_result[:len(data) // 2])

    # Вычисление статистических параметров
    mean_value = np.mean(data)
    median_value = np.median(data)
    min_value = np.min(data)
    max_value = np.max(data)
    std_deviation = np.std(data)

    # Оценка шума в дБ
    noise_estimate = 10 * np.log10(np.mean(data ** 2))

    return mean_value, median_value, min_value, max_value, std_deviation, noise_estimate, amplitude_spectrum


@app.callback(Output('output-data', 'children'),
              Input('upload-data', 'contents'))
def update_output(contents):
    if contents is not None:
        mean_value, median_value, min_value, max_value, std_deviation, noise_estimate, magnitude_spectrum = process_wav_file(
            contents)

        return [
            html.Div(f'Медианное значение: {mean_value}'),
            html.Div(f'Среднее значение: {median_value}'),
            html.Div(f'Минимальное значение: {min_value}'),
            html.Div(f'Максимальное значение: {max_value}'),
            html.Div(f'Стандартное квадратичное отклонение: {std_deviation}'),
            html.Div(f'Шум в дБ: {noise_estimate}'),
            dcc.Graph(
                figure=go.Figure(
                    data=[go.Scatter(y=magnitude_spectrum[:len(magnitude_spectrum)])],
                    layout=go.Layout(title='Amplitude Spectrum', xaxis={'title': 'Frequency'},
                                     yaxis={'title': 'Magnitude'})
                )
            )
        ]


if __name__ == '__main__':
    app.run_server(debug=True)
