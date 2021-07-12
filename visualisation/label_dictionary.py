
main_func_labels = {
    "MIT License" : "MIT License" + "\n" + "\n" + "Copyright (c) 2020 Personal Health Train / Implementations / GermanMII / DIFUTURE / PHT-Offline-Tool" + "\n" + "\n" + "Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the Software), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:" + "\n" + "\n" + "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software." + "\n" + "\n" + "THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.",
    "Copyright" : "Copyright" + " © " + "<a href=\"https://pht.difuture.de\"><font color=black> MIT </font></a>" + "created 2020, by Felix.B",
}

choose_page_labels = {
    "title" : "PHT offline tool",
    "button_left" : "Security Values",
    "label_right" : "Choose your model files and decrypt these using private and encrypted symmetric key",
    "button_right": "Model Page",
    "label_left" : "Generate your private and public keys aswell as hash signing for submitting valid trains",
    "href_bottom": "<a href=\"https://pht.difuture.de\"><font color=black>pht.difuture.de</font></a>",
    "signature" : "Created by Felix Bötte"
}

Model_Page_labels = {
    "button_topl" : "Select model files directory",
    "label_topl" : "No directory selected yet",
    "label_list" : "List of Modelfiles",
    "label_botr" : "Select the model directory first",
    "label_botr2" : "No model files selected yet",
    "decry_but" : "Decrypt selected models",
    "show_but" : "Show decrypted files",
    "return_but" : "Return",
    "label_topr" : "No key file selected",
    "label_topr2" : "No private key selected yet",
    "button_topr2" : "Select private key",
    "button_topr" : "Select encrypted symmetric key"
}

Security_Page_labels = {
    "button_topl" : "Generate private and public key",
    "label_topl" : "No keys generated yet" + "\n" + "\n" + "No path selected yet",
    "label_topr" : "Select a valid private key",
    "button_topr" : "Select private key",
    "button_sign" : "Sign",
    "button_return" : "Return",
    "button_copy" : "Copy",
    "label_rtxtbox" : "Signature",
    "label_ltxtbox" : "Paste your hash below",
    "label_botl" : "No hash signed yet",
}

Model_Page_func = {
    "encry_key_func" : "Chosen encrypted symmetric key loaded successfully:" + "\n" + "\n",
    "encry_key_error" : "You haven´t selected a valid key file",
    "config_failed_load":"Error while loading config file. Please check your input.",
    "config_encry_key_succ":"Encrypted Key got loaded succesfully.",
    "config_encry_key_failed": "Error while trying to load Encrypted Key. Please check your input.",
    "pk_except" : "Please select a key file",
    "pk_error_label" : "You haven't selected a valid key file",
    "pk_error_label_2": "You haven't selected a valid key file",
    "pk_error_msg" : "The selected private key is invalid. Choose a valid key or generate a new one",
    "pk_error_msg_2": "The selected private key is invalid. Choose a valid key or generate a new one",
    "pk_suc_label" : "The selected private key loaded successfully:" + "\n" + "\n",
    "model_label" : "No models selected" + "\n" + "\n" + "Please click on the file(s) to select them",
    "no_direc_label" : "No directory selected yet",
    "dir_label" : "Selected directory:" + "\n" + "\n",
    "dir_label2" : "Please click on the files to select them",
    "dir_err_label" : "Please select a valid directory",
    "missing_pk_msg" : "No private key selected to decrypt the models. Please select one.",
    "missing_symk_msg" : "You haven't selected a symmetric key. Please define one above",
    "mismatch_pk" : "You haven't selected a matching private key for the encrypted models",
    "mismatch_symk" : "You haven't selected a matching symmetric key for the encrypted models",
    "decry_succ" : "Selected models have been successfully decrypted ",
    "show_models_err" : "No files decrypted yet. Please select the models in your selected directory and decrypt them",
}

Security_Page_func = {
    "key_name_title" : "Generate your keys",
    "key_name_msg" : "Enter the name for your key pair:",
    "key_name_err" : "The file name is not valid. Please only enter letters and numbers",
    "key_succ" : "Keys successfully generated in:" + "\n" + "\n",
    "key_err" : "You did not select a valid directory",
    "pick_key_label" : "Please select a keyfile",
    "pick_key_label_again" : "Could not load keyfile. Please try again",
    "invalid_key" : "You haven´t selected a valid keyfile",
    "invalid_key_err" : "The selected private key is invalid. Choose a valid key or generate a new one",
    "load_key" : "The selected private key loaded successfully:" + "\n" + "\n",
    "no_pk_hash_err" : "Please select a private key to sign the hash",
    "hash_sign" : "Successfully singed the hash value.",
    "invalid_hash" : "Please select a hash in SHA512 format.",






}