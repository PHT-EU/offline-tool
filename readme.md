# PHT Train-User-Client

Offline Tool for key generation and decryption of results

## Documentation
The documentation of our PHT Offline Tool can be found [here](https://pht-medic.github.io/documentation/offline_tool/)

Please install the version based on your local OS. Currently we support: Windows,
Mac and Linux. If you want to work on the code itself follow the instructions below.

## Getting Started locally
This version depends on Python3.6 - please install it locally [https://www.python.org/downloads/release/python-360/](https://www.python.org/downloads/release/python-360/).
Before you can start the application you need to import a couple modules to your python interpreter. We suggest to create a virtual enviorment
and install the requirements. Go with your command to the cloned repository directory and create a virtualenv. Within this 
virtual environment install the dependencies.

```
pip install -r requirements.txt
```

To run the GUI in the right order on your local machine you start the script 

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


## Built With

* [PyQt5](https://pypi.org/project/PyQt5/) - The python framework used for the GUI
