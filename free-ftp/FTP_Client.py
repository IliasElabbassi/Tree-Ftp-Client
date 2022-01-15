from distutils.log import error
from queue import Empty
from re import S, VERBOSE
import socket
import sys
import logging

BUFFER_SIZE = 4080 # buffer size
FORMAT = "utf-8"
VERBOSE = True

class FTP_Client:
    def __init__(self, host, username):
        self.PORT = 21 
        self.HOST = host
        self.USERNAME = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setupLogger()

    def setupLogger(self):
        self.logger = logging.getLogger('FTP Client Logs')
        logging.basicConfig(
            filename='test.log',
            level=logging.DEBUG,
            format='%(asctime)s:%(levelname)s:%(message)s'
            )

    def buffered_readLine(self):
        line = ""
        while True:
            part = self.socket.recv(1).decode(FORMAT)
            if part != "\n":
                line+=part
            elif part == "\n":
                break
        return line

    def connect(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
            print(self.buffered_readLine())
            logging.info("Connection to the distant ftp server succeed {0}:{1} as {2}".format(self.HOST, self.PORT, self.USERNAME))
        except socket.error:
            logging.error("connection to the distant server failed {0}:{1}".format(self.HOST, self.PORT))
            sys.exit()

        try:
            if VERBOSE:
                print("$ USER")
            self.socket.send("USER {0}\r\n".format(self.USERNAME).encode(FORMAT))
            print(self.buffered_readLine())
        except:
            logging.error("failed CONNECT:USER !!!")
            return

        try:
            if VERBOSE:
                print("$ PASS")
            self.socket.send("PASS RV\r\n".encode(FORMAT))
            print(self.buffered_readLine())
        except:
            logging.error("failed CONNECT:PASS !!!")
            return


    """
    LIST: Show information of a specific file/folder or current folder

    this method will send a LIST commande to the FTP server and process the data received acordingly:
        -
        -
        -
    """
    def list_files(self):
        logging.info("Starting list_files() method...")

        try:
            # send LIST cmd to the ftp server
            self.socket.send("LIST".encode(FORMAT))
            print(self.buffered_readLine())
        except:
            logging.error("Couldn't make the request")
            return
    
    def HELP(self):
        logging.info("Starting HELP method...")

        try:
            self.socket.send("HELP".encode(FORMAT))
            print(self.buffered_readLine())
        except:
            logging.error("in HELP:HELP")
            return


def main():
    if len(sys.argv) < 3:
        print("need args : HOST USERNAME")
        sys.exit()

    for ele in sys.argv:
        if ele == "-v" or ele == "-V":
            VERBOSE = True

    #host = "ftp.free.fr"
    host = sys.argv[1]
    username = sys.argv[2]

    ftp_client = FTP_Client(
        host=host,  
        username=username
    )
    ftp_client.connect()
    #ftp_client.HELP()

if __name__ == "__main__":
    main()