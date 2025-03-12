import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

FLAG = "BUAACTF{1nFO_H1DD3N_1n_fr3KW3NcY_dom41N}"
IMG_WIDTH = 1920
IMG_HEIGHT = 800
FONT_FILE = "SourceHanSansSC-Bold.otf"
MUSCI_FILE = "autumn_leaves.wav"
ORIGIN_FILENAME = "origin.wav"
OUTPUT_FILENAME = "output.wav"
N_FFT = 4096


def spec2wav(amp, ang, filename, sr):
    """
    :param amp: the amplitude of spec array
    :param ang: the angle of spec array
    :param filename: output wav filename
    :param sr: sample rate
    :return:
    """
    D = amp * np.exp(1j * ang)
    y_inv = librosa.istft(D)
    sf.write(filename, y_inv, sr)


# 生成原始音频
y, sr = librosa.load(MUSCI_FILE)
S = librosa.stft(y, n_fft=N_FFT)
spectrogram = librosa.amplitude_to_db(abs(S))
spec2wav(librosa.db_to_amplitude(spectrogram), np.angle(S), ORIGIN_FILENAME, sr)

# 将flag转换为图片
img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), (255, 255, 255))
draw = ImageDraw.Draw(img)
font_size = int(IMG_WIDTH / len(FLAG) * 1.5)
font = ImageFont.truetype(FONT_FILE, font_size)
draw.text((font_size, IMG_HEIGHT // 2 - font_size), FLAG, (0, 0, 0), font)
img = img.resize((S.shape[1], S.shape[0]))

# 添加噪声
for i in range(img.height):
    for j in range(img.width):
        spectrogram[-i, j] += img.getpixel((j, i))[0] / 128

# 可视化频谱图
librosa.display.specshow(spectrogram, sr=sr, x_axis='time', y_axis='linear')
spec2wav(librosa.db_to_amplitude(spectrogram), np.angle(S), OUTPUT_FILENAME, sr)
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.show()
