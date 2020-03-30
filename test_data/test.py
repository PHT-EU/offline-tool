import numpy as np
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import pickle
from functionality import encryption_func


def generate_sym_key():
    return Fernet.generate_key()


def create_hash(length):
    return np.random.bytes(length)


def create_encrypted_models(fernet_key):
    encrypted_models = []
    fernet = Fernet(fernet_key)
    for _ in range(3):
        model = np.ones((20, 20))
        model = pickle.dumps(model)
        encrypted_models.append(fernet.encrypt(model))
    return encrypted_models


def create_encrypted_sym_key(rsa_public_key, fernet_key):
    encrypted_key = rsa_public_key.encrypt(fernet_key,
                                           padding.OAEP(
                                               mgf=padding.MGF1(algorithm=hashes.SHA512()),
                                               algorithm=hashes.SHA512(),
                                               label=None
                                           )
                                           )
    return encrypted_key


if __name__ == '__main__':
    sym_key = generate_sym_key()
    with open("sym_key", "wb") as sk_f:
        sk_f.write(sym_key)

    with open("sym_key", "rb") as sk_f:
        key = sk_f.read()

    with open("encr_sym_key", "wb") as enc_sym_key:
        with open("/home/felix/PycharmProjects/pht-offline-tool/test_data/rsa_public_key", "rb") as rsa_key:
            rsa_pub_key = serialization.load_pem_public_key(rsa_key.read(), default_backend())
        encr_key = create_encrypted_sym_key(rsa_pub_key, key)
        enc_sym_key.write(encr_key)
    models = create_encrypted_models(key)
    for i in range(len(models)):
        with open(f"model{i}", "wb") as f:
            f.write(models[i])

