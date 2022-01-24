# Tree FTP Client

# install
Clone the current repo
```
virtualenv env
./env/Scripts/activate # activate the virtual environement (depends on your OS)
pip install setuptools
python setup.py build
python setup.py install
```

## How to use it

```py
from TreeFtp import FTP_Client

host = "ftp.ubuntu.com" # or any other ftp server
username = "anonymous"
VERBOSE = True

ftp_client = FTP_Client.FTP_Client(
        host=host,
        username=username,
        verbose=VERBOSE
    ).launch() # launch() setup everything you need (you can pass a password throught this method also)
```


<b></b>Or</b>

If it do not launch

```
python ./TreeFtp/FTP_Client.py ftp.ubuntu.com anonymous -v
```
But you will probably need to change an import on the FTP_Client.py file (see FTP_Client.py file for more information).

## Command implemented :

**CMD** : you can pass ant cmd not implemented directly here<br>
**USER** : username cBouommand<br>
**PASS** : password command<br>
**PASV** : passive mode command<br>
**CWD** : change working directory command<br>
**LIST** : list files of the current directory<br>

## More
See **output.txt** inside the root directory for the output of the code above.

To change the level of recursion when exploring the files :

```py
ftp_client = FTP_Client.FTP_Client(
        host=host,
        username=username,
        verbose=VERBOSE,
        level=3 # HERE
    ).launch()
```

To add a password to the ftp client :
```py
ftp_client = FTP_Client.FTP_Client(
        host=host,
        username=username,
        verbose=VERBOSE,
    ).launch("my_password")
```

For the demo look at "TreeFtp Demo.mkv"