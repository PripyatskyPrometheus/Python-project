import numpy as np
from scipy.interpolate import interp1d
from scipy.io.wavfile import read, write
from matplotlib import pyplot as plt


def read_file(filename):

    fs, x = read(filename)
    x = np.array(x)
    if len(x.shape) > 1:
        x = np.mean(x, axis=1)
    x = x.astype(float) / max(abs(min(x)), abs(max(x)))
    t = np.linspace(0, (len(x) - 1) / fs, len(x))
    return x, t, fs

def plot_signal(t, signal, title):

    plt.figure(figsize=(12, 4))
    plt.plot(t, signal)
    plt.title(title)
    plt.xlabel('Время (с)')
    plt.ylabel('Амплитуда')
    plt.grid()
    plt.savefig(f"{title}.png")
    plt.show()

def shift(x, fs, dt, at, f):

    t = np.linspace(0, (len(x) - 1) / fs, len(x))
    new_t = np.zeros(len(t))
    for i in range(len(new_t)):
        new_t[i] = t[i] + dt + at * np.sin(2 * np.pi * f * t[i])

    f_interp = interp1d(new_t, x, bounds_error=False, fill_value=0)
  
    result = f_interp(t)
    
    
    return np.nan_to_num(result)


def effect_chorus(input_signal, fs, n_copy=5):
    copy = np.zeros((n_copy, len(input_signal)))
    for i in range(n_copy):
        copy[i] = shift(input_signal, fs, dt=0.02*i, at=0.01*i, f=0.5*i)
        copy[i] /= copy[i].max()

    result = np.sum(copy, axis=0)
    result /= max(abs(result.min()), abs(result.max()))
    return result


def main():
    input_file = "record_out(1).wav"
    output_file = "chorus.wav"
    
    signal, t, fs = read_file(input_file)
    plot_signal(t, signal, "Исходный сигнал")
    
    processed = effect_chorus(signal, fs, n_copy=5)
    plot_signal(t, processed, "Сигнал после применения хоруса")
    
    write(output_file, fs, processed)

if __name__ == "__main__":
    main()