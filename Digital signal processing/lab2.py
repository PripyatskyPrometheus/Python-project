import numpy as np
import statsmodels.tsa.stattools as smt
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
import pyreaper
from scipy.signal.windows import triang
from scipy.io.wavfile import write
from numba import njit

def read_file(file_name):
    fs, x = wavfile.read(file_name)
    x = np.array(x)
    if len(x.shape) > 1:
        x = np.mean(x, axis=1)
    x = x.astype(np.float32) / max(abs(min(x)), abs(max(x)))
    t = np.linspace(0, (len(x) - 1) / fs, len(x))
    return fs, x, t

def create_graph(title, x, y):
    plt.figure(title)
    plt.title(title)
    plt.plot(x, y)
    plt.savefig(f"{title}.png")

@njit
def my_acf(x, m):
    N = len(x)
    mu_x = np.mean(x)

    sum = 0.0
    for k in range(N - m):
        sum += (x[k] - mu_x) * (x[k + m] - mu_x)
    return sum / ((N - m) * np.var(x))


def my_dtft(x, fs, f):
    N = len(x)

    X = np.zeros_like(f, dtype=float)
    for i, freq in enumerate(f):
        w = 2 * np.pi * freq / fs  
        n = np.arange(N)
        complex_exponential = np.exp(-1j * w * n)
        X[i] = np.abs(np.dot(x, complex_exponential))
    return X

def psola(x, fs, k):
    int16_info = np.iinfo(np.int16)
    x = x * min(int16_info.min, int16_info.max)
    x = x.astype(np.int16)
    pm_times, pm, f_times, f, _ = pyreaper.reaper(x, fs)

    T = round(fs / np.mean(f[f != -1]))
    n = len(x) // T

    result = np.zeros(round(T*(k*(n-1)+2)))

    window_func = triang(2*T)

    for step in range(0, len(x) - 2*T, T):
        src_start = round(step)
        dst_start = round(step * k)
        result[dst_start: dst_start + 2*T] += x[src_start: src_start + 2*T] * window_func

    max_value = max(abs(max(result)), abs(min(result)))
    result /= max_value
    return result

def tone_acf(acf, fs, min_f0=50, max_f0=500):
    min_lag = int(fs / max_f0)
    max_lag = int(fs / min_f0)
    acf_truncated = acf[min_lag:max_lag]

    if len(acf_truncated) > 0:
        peak_index = np.argmax(acf_truncated)
        peak_lag = peak_index + min_lag
        f0 = fs / peak_lag
        return f0
    else:
        return None

def test_acf(fs, x):
    max_period = fs / 50
    res_acf = smt.acf(x, adjusted=True, nlags=int(max_period))
    res_my_acf = np.array([my_acf(x, m) for m in range(int(max_period) + 1)])

    print(f'Результат функции smt.acf: {res_acf[1]}   Результат функции my_acf: {res_my_acf[1]}')
    print(f'Результат функции smt.acf: {res_acf[10]}   Результат функции my_acf: {res_my_acf[10]}')
    print(f'Результат функции smt.acf: {res_acf[100]}   Результат функции my_acf: {res_my_acf[100]}')
    print(f'Результат функции smt.acf: {res_acf[500]}   Результат функции my_acf: {res_my_acf[500]}')

    m_space = np.linspace(0, len(res_acf) - 1, len(res_acf))
    create_graph('АКФ', m_space, res_acf)

    print("Тестирование АКФ")

    F0 = tone_acf(res_acf, fs)
    if F0 != None:
        print(f"Частота основного тона (F0): {F0:.2f} Гц")
    else:
        print("Не удалось выявит частоту основного тона")

def test_dtft(fs, x):
    f_space = np.arange(40, 500, 1)
    sp = my_dtft(x, fs, f_space)

    create_graph('Амплитудный спектр', f_space, sp)

    # Оценка частоты основного тона
    print("Проверка ДВПФ")
    f_space = np.arange(40, 500, 1)  # Диапазон частот
    F0 = f_space[np.argmax(sp)]  # Частота с максимальной амплитудой
    print(f"Частота основного тона (F0): {F0:.2f} Гц")

def test_pyreaper(fs, x, t):
    # Подготовка данных для reaper
    int16_info = np.iinfo(np.int16)
    x = x * min(int16_info.min, int16_info.max)
    x = x.astype(np.int16)
    # Вызов reaper
    pm_times, pm, f_times, f, _ = pyreaper.reaper(x, fs)
    # Отображение позиций пиков
    plt.figure('[Reaper] Пиковые значения')
    plt.plot(t, x)
    plt.scatter(pm_times[pm == 1], x[(pm_times * fs).astype(int)][pm == 1], marker='x', color='red')
    plt.savefig("[Reaper] Пиковые значения")
    # Отображение значений основной частоты
    plt.figure('[Reaper] Частота основного тона')
    plt.plot(f_times, f)
    plt.savefig("[Reaper] Частота основного тона")
    plt.show()

    print("Проверка библиотеки pyreaper")
    # Вычисление средней частоты основного тона
    F0_mean = np.mean(f[f != -1])
    print(f"Частота основного тона (F0):: {F0_mean:.2f} Гц")

def write_file(x, fs, k):
    res = psola(x, fs, k)
    write('new_out(1).wav', fs, res)

def main():
    file_name = "record_out(1).wav"
    fs, x, t,  = read_file(file_name)
    print(f"Параметры сигнала:\nfs={fs}\nx={x}\nt={t}\n")
    print(f'Длинна x = {len(x)}')
    test_acf(fs, x)
    test_dtft(fs, x)
    test_pyreaper(fs, x, t)
    write_file(x, fs, 1.5) 

if __name__ == '__main__':
    main()