import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

ORIGIN_FILE = "origin.wav"
ENCODED_FILE = "output.wav"

y, sr = librosa.load(ORIGIN_FILE)
S = librosa.stft(y)
spectrogram = librosa.amplitude_to_db(abs(S))

y, sr = librosa.load(ENCODED_FILE)
S = librosa.stft(y)
spectrogram2 = librosa.amplitude_to_db(abs(S))

for i in range(S.shape[0]):
    for j in range(S.shape[1]):
        spectrogram2[i, j] = spectrogram2[i, j] - spectrogram[i, j]

# 可视化频谱图
librosa.display.specshow(spectrogram2, sr=sr, x_axis='time', y_axis='linear')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.show()
