# pylint: disable=invalid-name,missing-docstring,too-few-public-methods

import unittest
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft
from scipy.signal import stft

def dft(x: np.ndarray) -> np.ndarray:
    N = len(x)
    X = np.zeros(N, dtype=complex)

    for k in range(N):
        for n in range(N):
            X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
    return X


def real_stft(x: np.ndarray, segment: int, overlap: int) -> np.ndarray:
    n = x.shape[0]
    assert len(x.shape) == 1
    assert segment < n
    assert overlap < segment

    hop_size = segment - overlap
    num_segments = (n - overlap) // hop_size

    stft_result = np.zeros((segment, num_segments), dtype=complex)

    for i in range(num_segments):
        start = i * hop_size
        end = start + segment
        segment_data = x[start:end]
        stft_result[:, i] = dft(segment_data)
    
    stft_result = stft_result[:segment // 2 + 1, :] # только положительные частоты

    return stft_result


class Test(unittest.TestCase):
    class Params:
        def __init__(self, n: int, segment: int, overlap: int) -> None:
            self.n = n
            self.segment = segment
            self.overlap = overlap

        def __str__(self) -> str:
            return f"n={self.n} segment={self.segment} overlap={self.overlap}"
    #@unittest.skip
    def test_dft(self) -> None:
        for n in (10, 11, 12, 13, 14, 15, 16):
            with self.subTest(n=n):
                np.random.seed(0)
                x = np.random.rand(n) + 1j * np.random.rand(n)
                actual = dft(x)
                expected = fft(x)
                self.assertTrue(np.allclose(actual, expected))

    #@unittest.skip
    def test_stft(self) -> None:
        params_list = (
            Test.Params(50, 10, 5),
            Test.Params(50, 10, 6),
            Test.Params(50, 10, 7),
            Test.Params(50, 10, 8),
            Test.Params(50, 10, 9),
            Test.Params(101, 15, 7),
            Test.Params(101, 15, 8),
        )

        for params in params_list:
            with self.subTest(params=str(params)):
                np.random.seed(0)
                x = np.random.rand(params.n)
                actual = real_stft(x, params.segment, params.overlap)
                _, _, expected = stft(
                    x,
                    boundary=None,
                    nperseg=params.segment,
                    noverlap=params.overlap,
                    padded=False,
                    window="boxcar",
                )
                assert isinstance(expected, np.ndarray)
                self.assertTrue(np.allclose(actual, params.segment * expected))


def main() -> None:
    
    sample_rate, audio_data = wavfile.read("6412-17.wav")
        
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)

    segment_length = 4096
    overlap = segment_length // 2

    f, t, spectrum = stft(audio_data, fs=sample_rate, nperseg=segment_length, noverlap=overlap)

    plt.figure(figsize=(14, 6))
    plt.pcolormesh(t, f, np.abs(spectrum)**2)
    plt.ylim(0, 1200)
    plt.ylabel('Частота (Гц)')
    plt.xlabel('Время (с)')
    plt.title('Спектрограмма')
    plt.savefig('Спектрограмма.png')
    plt.show()

    unittest.main()

if __name__ == "__main__":
    main()
