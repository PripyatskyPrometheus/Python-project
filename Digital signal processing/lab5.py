# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

import unittest

import numpy as np
from scipy.signal import stft, istft
from scipy.fft import ifft
import scipy.io.wavfile


def idft(x: np.ndarray) -> np.ndarray:
    N = len(x)
    n = np.arange(N)
    m = n.reshape((N, 1))
    e = np.exp(2j * np.pi *m * n / N)
    X = np.dot(e, x) / N
    return X


def real_istft(spectrum: np.ndarray, segment: int, overlap: int) -> np.ndarray:
    assert len(spectrum.shape) == 2
    assert spectrum.shape[0] == segment // 2 + 1

    window = np.ones(segment)
    hop = segment - overlap
    res_len = hop * spectrum.shape[1] + overlap
    x = np.zeros(res_len)
    w = np.zeros(res_len)

    for i in range(spectrum.shape[1]):
        #        |
        # Yt[n] \|/
        y = np.real(idft(np.concatenate((spectrum[:, i], np.flip(np.conj(spectrum[:, i][1:spectrum.shape[0] - 1 + segment % 2]))))))
        x = np.concatenate((x[:i * hop], x[i * hop:i * hop + segment] + y, x[i * hop + segment:]))
        w = np.concatenate((w[:i * hop], w[i * hop: i * hop + segment] + window, w[i * hop + segment:]))

    X = x / w

    return X


class Test(unittest.TestCase):
    class Params:
        def __init__(self, n: int, segment: int, overlap: int) -> None:
            self.n = n
            self.segment = segment
            self.overlap = overlap

        def __str__(self) -> str:
            return f"n={self.n} segment={self.segment} overlap={self.overlap}"

    def test_idft(self) -> None:
        for n in (10, 11, 12, 13, 14, 15, 16):
            with self.subTest(n=n):
                np.random.seed(0)
                x = np.random.rand(n) + 1j * np.random.rand(n)
                actual = idft(x)
                expected = ifft(x)
                self.assertTrue(np.allclose(actual, expected))

    #@unittest.skip
    def test_istft_unmodified(self) -> None:
        self._test_istft(False)

    #@unittest.skip
    def test_istft_modified(self) -> None:
        self._test_istft(True)

    def _test_istft(self, modify: bool) -> None:
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

                _, _, s = stft(
                    x,
                    boundary=None,
                    nperseg=params.segment,
                    noverlap=params.overlap,
                    padded=False,
                    window="boxcar",
                )

                assert isinstance(s, np.ndarray)

                if modify:
                    low_pass_filter = np.concatenate(
                        (
                            np.ones(s.shape[0] // 2),
                            np.zeros(s.shape[0] - s.shape[0] // 2),
                        )
                    )
                    for column in np.arange(s.shape[1]):
                        s[:, column] = s[:, column] * low_pass_filter

                _, expected = istft(
                    s,
                    boundary=None,
                    nperseg=params.segment,
                    noverlap=params.overlap,
                    window="boxcar",
                )

                assert isinstance(expected, np.ndarray)

                actual = real_istft(s * params.segment, params.segment, params.overlap)

                self.assertTrue(np.allclose(actual, expected))


def main() -> None:
    unittest.main()
    fs, data = scipy.io.wavfile.read("6412-17.wav")
    x = np.array(data)
    
    if len(x.shape) > 1:
        x = np.mean(x, axis=1)
    
    nperseg = int(0.02 * fs)
    noverlap = nperseg // 2
    window = "hann"

    _, _, Zxx = stft(x, fs=fs, window=window, nperseg=nperseg, noverlap=noverlap)
    
    Zxx_robot = np.abs(Zxx) * np.exp(0j)
    
    _, x_robot = istft(Zxx_robot, fs=fs, window=window, nperseg=nperseg, noverlap=noverlap)
    
    x_robot = x_robot / np.max(np.abs(x_robot))
    scipy.io.wavfile.write("new_robot_effect.wav", fs, x_robot)

if __name__ == "__main__":
    main()