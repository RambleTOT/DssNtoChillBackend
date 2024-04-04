import base64
import io
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-audio',
        children=html.Button('Upload Audio File'),
        multiple=False
    ),
    html.Div(id='output-graph')
])


def plot_spectrum(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    with open('temp.wav', 'wb') as f:
        f.write(decoded)

    rate, data = wavfile.read('temp.wav')
    fft_data = np.fft.fft(data)
    magnitude = np.abs(fft_data)

    plt.figure(figsize=(10, 5))
    plt.plot(magnitude)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(img.read()).decode()))


@app.callback(Output('output-graph', 'children'),
              Input('upload-audio', 'contents'))
def update_output(contents):
    if contents is not None:
        return plot_spectrum(contents)
    else:
        return html.Div()


if __name__ == '__main__':
    app.run_server(debug=True)
