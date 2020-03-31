# PHT Train-User-Client

Offline Tool for key generation and decryption of results

## Getting Started

Before you can start the application you need to import a couple modules to your python interpreter:

```
pip install cryptography
pip install numpy
pip install PyQt5
```

To run the the GUI in the right order on your local machine you start the script 

```
main.py
```
from there on you can maneuver yourself through the different parts of the application. 

&nbsp;

To select your own encrypted symmetric key for decrypting your model files place it into this directory:
```
Pht-offline-tool/functionality/encr_sym_key
```

## Using Test-data

To use the given test_data for testing the decryption process execute the script

```
Pht-offline-tool/test_data/test.py
```

This script will generate you three example models and an encrypted symmetric key that you will need to decrypt these models.
In order to decrypt the test data successfully you need to load the private and encrypted symmetric key, which are stored in the same directory, into the application:

 ```
Pht-offline-tool/test_data/rsa_private_key
```

You will find the neccessary steps on the ModelPage of the application.

## Create standalone application

To create an application that you can use on different machines and operating systems follow the tutorial by mhermrmann

```
https://github.com/mherrmann/fbs-tutorial
```


## Built With

* [PyQt5](https://pypi.org/project/PyQt5/) - The python framework used for the GUI
