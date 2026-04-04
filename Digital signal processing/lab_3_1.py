import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.signal import sawtooth, square

def tone(f, t, waveform='harmonic', fs=44100):
    time = np.linspace(0, t, int(fs * t), endpoint=False)  # Создаем массив времени

    if waveform == 'harmonic': # Гармонический сигнал
        signal = np.sin(2 * np.pi * f * time)
    elif waveform == 'square': #  Mеандр (квадратная волна)
        signal = square(2 * np.pi * f * time)
    elif waveform == 'triangle': # Треугольная форма сигнала
        signal = sawtooth(2 * np.pi * f * time, width=0.5)
    elif waveform == 'sawtooth': # Пила
        signal = sawtooth(2 * np.pi * f * time)
    else:
        raise ValueError("Неопределённая форма сигнала")

    return signal


frequency = 440 
duration = 10  
sampling_rate = 44100

# Генерируем синусоидальный сигнал
audio = tone(frequency, duration, waveform='sawtooth', fs=sampling_rate)

# Сохраняем сигнал в WAV-файл
write('tone_sawtooth.wav', sampling_rate, audio)

# Отображаем часть сигнала
plt.figure(figsize=(10, 4))
plt.title('Cигнал')
plt.xlabel('Время, мс')
plt.ylabel('Амплитуда')
plt.xlim(0, 0.01)  # Отображаем первые 10 мс
plt.stem(np.linspace(0, duration, len(audio)), audio, use_line_collection=True)
plt.show()