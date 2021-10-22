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


## Using Test-data

To use the given test_data for testing the decryption process execute the script

```
Pht-offline-tool/test_data/test.py
```

This script will generate you three example models and an encrypted symmetric key that you will need to decrypt these models.
In order to decrypt the test data successfully you need to load the private and encrypted symmetric key into the application. 
Both keys are stored in the same directory:

 ```
Pht-offline-tool/test_data/rsa_private_key

Pht-offline-tool/test_data/encr_sym_key
```

You will find the neccessary functions for key-loading on the ModelPage of the application.


## Design options

For the application is a dark-mode available. To activate it uncomment the line 45 in main.py

 ```
#app.setStyleSheet(open("./visualisation/darkorange.stylesheet").read())
```

## Create standalone application

To create an application that you can use on different machines and operating systems follow the tutorial by mhermrmann

```
https://github.com/mherrmann/fbs-tutorial
```


## Built With

* [PyQt5](https://pypi.org/project/PyQt5/) - The python framework used for the GUI
