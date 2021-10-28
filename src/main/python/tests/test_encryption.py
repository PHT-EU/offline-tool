import unittest
from functionality import encryption_func
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding, utils
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import json


class MyTestCase(unittest.TestCase):
    def test_encryption(self):
        priv_key, pub_key = encryption_func.create_rsa_keys()
        pr_key = serialization.load_pem_private_key(priv_key,
                                                    password=None,
                                                    backend=default_backend())
        pu_key = serialization.load_pem_public_key(bytes.fromhex(pub_key), backend=default_backend())
        with open("private_test.pem", "wb") as file:
            file.write(priv_key)

        # compare created public keys
        self.assertEqual(pr_key.public_key().public_numbers(), pu_key.public_numbers())
        # check public key loading
        self.assertEqual(encryption_func.load_public_key(pub_key).public_numbers(), pu_key.public_numbers())
        # check private key loading
        self.assertEqual(encryption_func.load_private_key("private_test.pem").private_numbers(),pr_key.private_numbers())

    def test_hash(self):
        # create example hash for "Test"-String
        test_str = "Test"
        hasher = hashes.Hash(hashes.SHA512(), default_backend())
        hasher.update(test_str.encode())
        example_hash = hasher.finalize()

        # check hashing function
        self.assertEqual(encryption_func.hash_string(test_str), example_hash)

    def test_signature(self):
        # create hash
        test_str = "Test"
        hasher = hashes.Hash(hashes.SHA512(), default_backend())
        hasher.update(test_str.encode())
        example_hash = hasher.finalize()

        # load example private key
        pr_key = encryption_func.load_private_key("private_test.pem")

        # use predefined signing
        signature_fct = encryption_func.sign_hash(pr_key, example_hash)

        # use signing function
        signature = pr_key.sign(example_hash,
                                     padding.PSS(
                                         mgf=padding.MGF1(hashes.SHA512()),
                                         salt_length=padding.PSS.MAX_LENGTH
                                     ),
                                     utils.Prehashed(hashes.SHA512()))

        # verify both signatures to test if signatures are correct
        pu2 = pr_key.public_key()

        result1 = pu2.verify(
            signature,
            example_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH),
            utils.Prehashed(hashes.SHA512()))
        result2 = pu2.verify(
            signature_fct,
            example_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH),
            utils.Prehashed(hashes.SHA512()))

        # check signing function
        self.assertIsNone(result1)
        self.assertIsNone(result2)

    def test_config(self):
        # load config-file
        data1 = encryption_func.load_config("train_config.json")
        with open("train_config.json") as f:
            data2 = json.load(f)
        # check config loading
        self.assertEqual(data1, data2)

        # use predefined verification
        result_1 = encryption_func.verify_digital_signature(data1)
        # usual verification
        ds = data1["digital_signature"]
        for sig in ds:
            public_key = serialization.load_pem_public_key(bytes.fromhex(data1["rsa_public_keys"][sig["station"]]), backend=default_backend())
            try:
                result_2 = public_key.verify(bytes.fromhex(sig["sig"][0]),
                              bytes.fromhex(sig["sig"][1]),
                              padding.PSS(mgf=padding.MGF1(hashes.SHA512()),
                                          salt_length=padding.PSS.MAX_LENGTH),
                              utils.Prehashed(hashes.SHA512())
                              )
            except:
                result_2 = "Error"

        # check verification of config-file
        self.assertIsNone(result_1)
        self.assertIsNone(result_2)

    def test_modeldecryption(self):
        # load config-file
        with open("train_config.json") as f:
            data2 = json.load(f)
        # load encrypted symmetric key
        sym_key = data2["user_encrypted_sym_key"]
        # load user private key
        with open("demo_privkey.pem", "rb") as key:
            tpr_key = serialization.load_pem_private_key(key.read(),
                                                                 password=None,
                                                                 backend=default_backend())
        # decrypt symmetric key
        sym_key2 = bytes.fromhex(sym_key)
        decrypted_key = tpr_key.decrypt(
            sym_key2,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        )
        
        # decrypt example model
        decr_models = []
        fernet = Fernet(decrypted_key)
        for model in ["analysis_results.pkl"]:
            with open(model, "rb") as mf:
                token = mf.read()
            fernet_decrypt = fernet.decrypt(token)
            decr_models.append(fernet_decrypt)
        # use predefined decryption function
        decr_models_usual = encryption_func.decrypt_models(["analysis_results.pkl"], decrypted_key)
        # compare decryption results
        self.assertEqual(decr_models_usual, decr_models)

    def test_symkeydecryption(self):
        # load example private key
        with open("private_test.pem", "rb") as key:
            pr_key = serialization.load_pem_private_key(key.read(),
                                                                 password=None,
                                                                 backend=default_backend())
        # generate belonging public key
        pu2 = pr_key.public_key()
        # generate symmetric key key and encrypt it according to the public key
        sym_key = Fernet.generate_key()
        encr_sym_key = pu2.encrypt(sym_key,
                                   padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA512()),
                                                algorithm=hashes.SHA512(),
                                                label=None)
                                   )
        # generate hex-value of key
        sym_key_hex = encr_sym_key.hex()

        # decrypt symmetric key
        sym_key2 = bytes.fromhex(sym_key_hex)
        decrypted_key = pr_key.decrypt(
            sym_key2,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        )
        # decrypt symmetric key by predefined function
        decrypted_key2 = encryption_func.decrypt_symmetric_key(sym_key2, pr_key)

        # compare results
        self.assertEqual(decrypted_key, decrypted_key2)


if __name__ == '__main__':
    unittest.main()
