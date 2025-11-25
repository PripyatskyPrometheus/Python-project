import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.signal import sawtooth, square

def tone(f, t, waveform='harmonic', fs=44100):
    time = np.linspace(0, duration, int(fs * t), endpoint=False)

    if waveform == 'harmonic':
        signal = np.sin(2 * np.pi * f * time)
    elif waveform == 'square':
        signal = square(2 * np.pi * f * time)
    elif waveform == 'triangle':
        signal = sawtooth(2 * np.pi * f * time, width=0.5)
    elif waveform == 'sawtooth':
        signal = sawtooth(2 * np.pi * f * time)
    else:
        raise ValueError("Неопределённая форма сигнала")

    return signal

def musical_tone(f, t, waveform='harmonic', fs=44100, db=-20):
    time = np.linspace(0, t, int(fs * t), endpoint=False)

    harmonics = int(20000 / f)  # Максимальное количество гармоник

    amplitudes = [1]  # Первая гармоника (основная)
    for i in range(2, harmonics + 1):
        amplitudes.append(1 / i)  # Амплитуды уменьшаются с ростом номера гармоники

    harmonic_signals = []
    for i in range(1, harmonics + 1):
        harmonic_signals.append(tone(i * f, t, waveform, fs) * amplitudes[i-1])

    composite_signal = np.sum(harmonic_signals, axis=0)

    max_amplitude = np.max(np.abs(composite_signal))
    print(f"Максимальная амплитуда до нормализации: {max_amplitude}") 
    composite_signal = composite_signal / max_amplitude
    print(f"Максимальная амплитуда после нормализации: {np.max(np.abs(composite_signal))}")

    if db != 0:
        if db > 0:
            print("db положительный - сигнал будет усилен")
        alpha = -np.log(10**(db/20)) / duration
        decay = np.exp(-alpha * time)
        composite_signal = composite_signal * decay

    return composite_signal

# Параметры
sampling_rate = 44100
waveform = 'harmonic'
decay_db = -10

# Happy (Pharrell Williams)
note_names = [
    'A3', 'C4', 'D4', 'C4', 'E4', 'D4', 'C4', 'A3', 'D4', 'C4',
    'A3', 'C4', 'A3', 'C4', 'D4', 'C4', 'E4', 'E3', 'E3', 'G3',
    'A3', 'A3', 'A3', 'G3', 'A3', 'A3', 'A3', 'A3', 'G3', 'A3',
    'A3', 'A3', 'G3', 'A3'
]

notes = [
    {'frequency': 220.00, 'duration': 1},
    {'frequency': 261.6256, 'duration': 1},
    {'frequency': 293.6648, 'duration': 1},
    {'frequency': 261.6256, 'duration': 1},
    {'frequency': 329.6276, 'duration': 1},
    {'frequency': 293.6648, 'duration': 1},
    {'frequency': 261.6256, 'duration': 0.5},
    {'frequency': 220.00, 'duration': 0.5},
    {'frequency': 293.6648, 'duration': 1},
    {'frequency': 261.6256, 'duration': 1},
    {'frequency': 220.00, 'duration': 0.5},
    {'frequency': 261.6256, 'duration': 0.5},
    {'frequency': 220.00, 'duration': 1},
    {'frequency': 261.6256, 'duration': 1},
    {'frequency': 293.6648, 'duration': 1},
    {'frequency': 261.6256, 'duration': 0.5},
    {'frequency': 329.6276, 'duration': 0.5},
    {'frequency': 164.8138, 'duration': 0.5},
    {'frequency': 164.8138, 'duration': 0.5},
    {'frequency': 195.9977, 'duration': 0.5},
    {'frequency': 220.00, 'duration': 0.5},
    {'frequency': 220.00, 'duration': 0.5},
    {'frequency': 220.00, 'duration': 0.5},
    {'frequency': 195.9977, 'duration': 0.5},
    {'frequency': 220.00, 'duration': 0.5},
    {'frequency': 220.00, 'duration': 1},
    {'frequency': 220.00, 'duration': 1},
    {'frequency': 220.00, 'duration': 0.5},
    {'frequency': 195.9977, 'duration': 0.5},
    {'frequency': 220.00, 'duration': 0.5},
    {'frequency': 220.00, 'duration': 1},
    {'frequency': 220.00, 'duration': 1},
    {'frequency': 195.9977, 'duration': 0.5},
    {'frequency': 220.00, 'duration': 0.5}
]

# Создаем музыкальные фрагменты
music = []
for i, note_data in enumerate(notes):
    note_name = note_names[i]
    frequency = note_data['frequency']
    duration = note_data['duration']
    note_signal = musical_tone(frequency, duration, waveform=waveform, fs=sampling_rate, db=decay_db)
    music.append(note_signal)
    print(f"Обработка ноты {note_name}")

combined_music = np.concatenate(music)

combined_music = combined_music / np.max(np.abs(combined_music))

write('my_music.wav', sampling_rate, combined_music)