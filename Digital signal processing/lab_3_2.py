import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.signal import sawtooth, square

def tone(f, t, waveform='harmonic', fs=44100):
    time = np.linspace(0, t, int(fs * t), endpoint=False)  # Создаем массив времени

    if waveform == 'harmonic': # Гармонический сигнал
        signal = np.sin(2 * np.pi * f * time)
    elif waveform == 'square': #  Mеандр со скважностью
        signal = square(2 * np.pi * f * time)
    elif waveform == 'triangle': # # Треугольная форма сигнала
        signal = sawtooth(2 * np.pi * f * time, width=0.5)
    elif waveform == 'sawtooth': # Пила
        signal = sawtooth(2 * np.pi * f * time)
    else:
        raise ValueError("Неопределённая форма сигнала")

    return signal

def musical_tone(f, t, waveform='harmonic', fs=44100, db=-20):

    time = np.linspace(0, t, int(fs * t), endpoint=False)

    harmonics = int(20000 / f)  # Максимальное количество гармоник

    # Определение амплитуд гармоник
    amplitudes = [1]  # Первая гармоника (основная)
    for i in range(2, harmonics + 1):
        amplitudes.append(1 / i)  # Амплитуды уменьшаются с ростом номера гармоники

    harmonic_signals = []
    for i in range(1, harmonics + 1):
        harmonic_signals.append(tone(i * f, t, waveform, fs) * amplitudes[i-1])

    # Сложение гармоник
    composite_signal = np.sum(harmonic_signals, axis=0, dtype=np.float64)

    # Нормализация сигнала
    max_amplitude = np.max(np.abs(composite_signal))
    print(f"Максимальная амплитуда до нормализации: {max_amplitude}") 
    composite_signal = composite_signal / max_amplitude
    print(f"Максимальная амплитуда после нормализации: {np.max(np.abs(composite_signal))}")

    # Затухание сигнала
    if db != 0:
        if db > 0:
            print("db положительный - сигнал будет усилен")
        alpha = -np.log(10**(db / 20)) / t
        decay = np.exp(-alpha * time)
        composite_signal = composite_signal * decay

    return composite_signal

# Пример использования:
frequency = 440
duration = 5
sampling_rate = 44100
decay_db = -20  # Уровень затухания (дБ)

# Генерируем музыкальный тон
audio = musical_tone(frequency, duration, waveform='triangle', fs=sampling_rate, db=decay_db)

write('musical_tone_triangle.wav', sampling_rate, audio)

# Отображение сигнала
plt.figure(figsize=(10, 4))
plt.title('Затухающий составной тон')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.xlim(0, 0.01)  # Первые 10 мс
plt.stem(np.linspace(0, duration, len(audio)), audio, use_line_collection=True)
plt.show()