from functionality import encryption_func

class test_decryption():

    def __init__(self):
        '''self.symkey = open("./test_data/encr_sym_key", "rb")
        self.model = open("./test_data/model")
        self.private_key = open("./test_data/rsa_private_key", )
        self.public_key = open("./test_data/rsa_public_key")'''
        print(len(
            "cfb57759d4a1fc224584c3259595017d25beb3700afc04562f3a60047b725908932eedafe52632063dc7a01c3d0c7867c85c13979a9b5bce851af6e04445e538"))
        self.decrypt_models()



    def decrypt_models(self):

        with open("C:/Users/fboet/PycharmProjects/pht-offline-tool/test_data/encr_sym_key", "rb") as encr_sym_key:
            encr_key = encr_sym_key.read()
            print("symkey read")
            priv_key = encryption_func.load_private_key("C:/Users/fboet/PycharmProjects/pht-offline-tool/test_data/rsa_private_key")
            print("private key read")
        decry_sym_key = encryption_func.decrypt_symmetric_key(encr_key, priv_key)
        print("symkey decrypted")

        model = [''"C:/Users/fboet/PycharmProjects/pht-offline-tool/test_data/model1"'']
        print(model[0])
        decrypted_model = encryption_func.decrypt_models(model, decry_sym_key)
        print(len(decrypted_model))
        print("model decrypted")

        with open(model[0], "w") as decr_model:
            decr_model.write(str(decrypted_model[0]))

        print("model updated")






        '''print("symkey read")
        decry_sym_key = encryption_func.decrypt_symmetric_key(encr_key, self.private_key)
        print("symkey decrypted")

        decrypted_model = encryption_func.decrypt_models(self.model, decry_sym_key)
        print("model decrypted")

        with open(self.model, "rb") as decr_model:
            decr_model.write(decrypted_model)

        print("model written")'''

























if __name__ =="__main__":
   test_decryption()
