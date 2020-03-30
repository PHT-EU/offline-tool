from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtGui, QtWidgets
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


def store_keys(path, rsa_private_key_pem,rsa_public_key_pem, name, name2):
    """
    Stores the given keys at the specified path
    :param path:
    :param rsa_private_key_pem:
    :param rsa_public_key_pem:
    :return:
    """
    print("Test store")
    with open(os.path.join(path, name + "_sk.pem"), "wb") as sk:
        sk.write(rsa_private_key_pem)
        print("Wrote " + name + " to " +  path)
    with open(os.path.join(path, name2 + "_pk.pem"), "wb") as pk:
        pk.write(rsa_public_key_pem)
        print("Wrote " + name2 + " to " +  path)



def load_private_key(path):
    """
    Loads a private key from the given path
    :param path:
    :return:
    """
    print(path)
    with open(path, "rb") as key:
        try:
            private_key = serialization.load_pem_private_key(key.read(),
                                                             password=None,
                                                             backend=default_backend())
        except:
            private_key = "unvalid"
            return private_key
        else:
            print("Key successfully loaded")
            return private_key


def sign_hash(private_key, hash):
    """
    Creates an ecc signature using the provided private key and hash
    :param rsa: rsa private key
    :param hash: hash as byte object
    :return: DER encoded byte object representing the signature
    """
    signature = private_key.sign(hash,
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
    fernet = Fernet(sym_key)
    for model in models:
        with open(model, "rb") as mf:
            token = mf.read()
            fernet_decrypt = fernet.decrypt(token)
            decr_models.append(fernet_decrypt)
    return decr_models


def hash_string(string):
    hasher = hashes.Hash(hashes.SHA512(), default_backend())
    hasher.update(string.encode())
    return hasher.finalize()


