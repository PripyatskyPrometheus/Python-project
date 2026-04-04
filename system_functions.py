import logging
import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

logger = logging.getLogger()
logger.setLevel('INFO')


def load_settings(settings_file: str) -> dict:
    settings = None
    try:
        with open(settings_file) as json_file:
            settings = json.load(json_file)
        logging.info(f"Settings file successfully loaded from file {settings_file}")
    except OSError as err:
        logging.warning(f"Settings file was not loaded from file {settings_file}\n{err}")
    return settings


def byte_read_text(file_name: str) -> bytes:
    """
    The function reads text in byte form from txt file.
    :param file_name: name of txt file.
    :return: text in byte form.
    """
    try:
        with open(file_name, mode='rb') as text_file:
            text = text_file.read()
        logging.info(f' Text was successfully read from file {file_name}')
    except OSError as err:
        logging.warning(f' Text was not read from file {file_name}\n{err}')
    return text


def byte_write_text(text: bytes, file_name: str) -> None:
    """
    The function writes text in byte form to txt file.
    :param text: text for writing
    :param file_name: name of txt file.
    :return: None
    """
    try:
        with open(file_name, mode='wb') as text_file:
            text_file.write(text)
        logging.info(f' Text was successfully written to file {file_name}')
    except OSError as err:
        logging.warning(f' Text was not written to file {file_name}\n{err}')


def save_symmetric_key(key: bytes, file_name: str) -> None:
    """
    The function saves a symmetric key to txt file.
    :param key: symmetric key for symmetric encryption algorithm.
    :param file_name: name of txt file.
    :return: None.
    """
    try:
        with open(file_name, 'wb') as key_file:
            key_file.write(key)
        logging.info(f' Symmetric key successfully saved to {file_name}')
    except OSError as err:
        logging.warning(f' Symmetric key was not saved to file {file_name}\n{err}')


def save_asymmetric_keys(private_key, public_key, private_pem: str, public_pem: str) -> None:
    """
    The function saves a private key and a public key to pem files.
    param private_key: private key for asymmetric encoding algorithm.
    param public_key: public key for asymmetric encoding algorithm.
    param private_pem: pem file for private key.
    param public_pem: pem file for public key.
    return: None
    """
    try:
        with open(private_pem, 'wb') as private_out:
            private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                        encryption_algorithm=serialization.NoEncryption()))
        logging.info(f' Private key successfully saved to {private_pem}')
    except OSError as err:
        logging.warning(f' Private key was not saved to file {private_pem}\n{err}')
    try:
        with open(public_pem, 'wb') as public_out:
            public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                     format=serialization.PublicFormat.SubjectPublicKeyInfo))
        logging.info(f' Public key successfully saved to {public_pem}')
    except OSError as err:
        logging.warning(f' Public key was not saved to file {public_pem}\n{err}')


def load_symmetric_key(file_name: str) -> bytes:
    """
    The function loads  a symmetric key from txt file.
    :param file_name: name of txt file.
    :return: symmetric key for symmetric encoding algorithm.
    """
    try:
        with open(file_name, mode='rb') as key_file:
            key = key_file.read()
        logging.info(f' Symmetric key successfully loaded from {file_name}')
    except OSError as err:
        logging.warning(f' Symmetric key was not loaded from file {file_name}\n{err}')
    return key


def load_private_key(private_pem: str):
    """
    The function loads a private key from pem file.
    :param private_pem: name of pem file.
    :return: private key for asymmetric encoding algorithm.
    """
    private_key = None
    try:
        with open(private_pem, 'rb') as pem_in:
            private_bytes = pem_in.read()
        private_key = load_pem_private_key(private_bytes, password=None)
        logging.info(f' Private key successfully loaded from {private_pem}')
    except OSError as err:
        logging.warning(f' Private key was not loaded from file {private_pem}\n{err}')
    return private_key


def load_public_key(public_pem: str):
    """
    The function loads a public key from pem file.
    :param public_pem: name of pem file.
    :return: public key for asymmetric encoding algorithm.
    """
    public_key = None
    try:
        with open(public_pem, 'rb') as pem_in:
            public_bytes = pem_in.read()
        public_key = load_pem_public_key(public_bytes)
        logging.info(f' Public key successfully loaded from {public_pem}')
    except OSError as err:
        logging.warning(f' Public key was not loaded from file {public_pem}\n{err}')
    return public_key
    