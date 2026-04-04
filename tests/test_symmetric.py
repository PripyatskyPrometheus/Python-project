import unittest
import os
import logging

from symmetric import generate_symmetric_key, symmetric_encrypt, symmetric_decrypt


class TestSymmetric(unittest.TestCase):
    def test_generate_symmetric_key_length(self):
        for length in (4, 8, 16, 24, 32):
            key = generate_symmetric_key(length)
            self.assertIsInstance(key, bytes)
            self.assertEqual(len(key), length)

    def test_encrypt_decrypt_roundtrip(self):
        key = generate_symmetric_key(16)
        plaintexts = [
            b"",
            b"short",
            os.urandom(1),
            os.urandom(7),
            os.urandom(8),  # block size boundary after padding
            os.urandom(31),
            b"The quick brown fox jumps over the lazy dog",
        ]
        for pt in plaintexts:
            ct = symmetric_encrypt(key, pt)
            self.assertIsInstance(ct, bytes)
            # Blowfish CBC with 8-byte IV prepended
            self.assertGreaterEqual(len(ct), 8)
            self.assertEqual(len(ct) % 8, 0)
            recovered = symmetric_decrypt(key, ct)
            self.assertEqual(recovered, pt)

    def test_ciphertext_has_random_iv(self):
        key = generate_symmetric_key(16)
        pt = b"data"
        ct1 = symmetric_encrypt(key, pt)
        ct2 = symmetric_encrypt(key, pt)
        # First 8 bytes are IV and should differ with high probability
        self.assertNotEqual(ct1[:8], ct2[:8])
        # Entire ciphertext should differ due to different IVs
        self.assertNotEqual(ct1, ct2)

    def test_wrong_key_fails_to_decrypt(self):
        key = generate_symmetric_key(16)
        wrong_key = generate_symmetric_key(16)
        pt = b"secret message"
        ct = symmetric_encrypt(key, pt)
        with self.assertRaises(Exception):
            # This may fail either during decrypt or during unpadding
            symmetric_decrypt(wrong_key, ct)

    def test_logging_messages(self):
        key = generate_symmetric_key(16)
        pt = b"hello"
        with self.assertLogs(level="INFO") as cm:
            gen_key = generate_symmetric_key(8)
            _ = symmetric_encrypt(key, pt)
            _ = symmetric_decrypt(key, _)
        logs = "\n".join(cm.output)
        self.assertIn("Symmetric key successfully generated", logs)
        self.assertIn("Symmetric encryption was successful", logs)
        self.assertIn("Symmetric decryption was successful", logs)


if __name__ == "__main__":
    unittest.main()
