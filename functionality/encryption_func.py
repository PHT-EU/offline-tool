from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, ec
# EC used?
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import os


def create_rsa_keys():
    """
    Generates a rsa private public key pair and returns their byte representation
    :return:
    """
    print("Test create")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # TODO maybe use a password for storing the private key -> more user security
    private_key_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                format=serialization.PrivateFormat.PKCS8,
                                                encryption_algorithm=serialization.NoEncryption()
                                                )
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                             format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return private_key_pem, public_key_pem


def store_keys(path, rsa_private_key_pem, name):
    """
    Stores the given keys at the specified path
    :param path:
    :param rsa_private_key_pem:
    :param name:
    :return:
    """
    print("Test store")
    with open(os.path.join(path, name), "wb") as sk:
        sk.write(rsa_private_key_pem)
        print("Wrote " + name + " to " + path)


def load_private_key(path):
    """
    Loads a private key from the given path
    :param path:
    :return:
    """
    print(path)
    with open(path, "rb") as key:
        private_key = serialization.load_pem_private_key(key.read(),
                                                         password=None,
                                                         backend=default_backend())
    print("Key successfully loaded")
    return private_key


def sign_hash(private_key, hash_value):
    """
    Creates an ecc signature using the provided private key and hash
    :param private_key: rsa private key
    :param hash_value: hash as byte object
    :return: DER encoded byte object representing the signature
    """
    signature = private_key.sign(hash_value,
                                 padding.PSS(
                                     mgf=padding.MGF1(hashes.SHA512()),
                                     salt_length=padding.PSS.MAX_LENGTH
                                 ),
                                 utils.Prehashed(hashes.SHA512()))
    return signature


def decrypt_symmetric_key(encrypted_sym_key, private_key):
    """
    Decrypts a given symmetric key using the private key of the user
    :param encrypted_sym_key: rsa encrypted symmetric key
    :param private_key:
    :return:
    """
    decrypted_key = private_key.decrypt(
        encrypted_sym_key,
        padding=padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    )
    return decrypted_key


def decrypt_models(models, sym_key):
    """
    Decrypts the given models using the provided symmetric key
    :param models: list of encrypted models
    :param sym_key: symmetric key
    :return: list of decrypted models
    """
    decr_models = []
    fer = Fernet(sym_key)
    for model in models:
        with open(model, "rb") as mf:
            decr_models.append(fer.decrypt(mf.read()))
    return decr_models


def hash_string(string):
    hash_str = hashes.Hash(hashes.SHA512(), default_backend())
    hash_str.update(string.encode())
    return hash_str.finalize()


