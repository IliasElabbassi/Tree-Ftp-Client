from distutils.log import error
from queue import Empty
from re import S
import socket
import sys
import logging

BUFFER_SIZE = 4080 # buffer size
FORMAT = "utf-8"

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

    def getMsg(self):
        try:
            return self.socket.recv(BUFFER_SIZE).decode(FORMAT)
        except:
            logging.error("in getMsg :")
    
    def read(self):
        data = self.getMsg()
        while data:
            print(data)
            data = self.getMsg()

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

    """
        try:
            print("$ AUTH")
            self.socket.send("AUTH".encode(FORMAT))
            print(self.buffered_readLine())
            logging.info("send AUTH SSL cmd to {0}:{1}".format(self.HOST, self.PORT))
        except:
            logging.error("in CONNECT:AUTH")
    
        try:
            print("$ USER anonymous")
            self.socket.send("USER anonymous".encode(FORMAT))
            logging.info("send USER anonymous cmd to {0}:{1}".format(self.HOST, self.PORT))
            print(self.getMsg())
        except:
            logging.error("in CONNECT:USER")
        try:
            print("$ PASS ********")
            self.socket.send("PASS ********".encode(FORMAT))
            logging.info("send PASS ******** cmd to {0}:{1}".format(self.HOST, self.PORT))
            print(self.getMsg())
        except:
            logging.error("in CONNECT:PASS")

        try:
            print("$ SYS")
            self.socket.send("SYS".encode(FORMAT))
            logging.info("send SYS cmd to {0}:{1}".format(self.HOST, self.PORT))
            print(self.getMsg())
        except:
            logging.error("in CONNECT:SYS")

        try:
            print("$ FEAT")
            self.socket.send("FEAT".encode(FORMAT))
            logging.info("send FEAT cmd to {0}:{1}".format(self.HOST, self.PORT))
            print(self.getMsg())
        except:
            logging.error("in CONNECT:FEAT")
    """
        

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
            print(self.read())
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

    #host = "ftp.free.fr"
    host = sys.argv[1]
    username = sys.argv[2]

    ftp_client = FTP_Client(
        host=host,  
        username=username
    )
    ftp_client.connect()
    ftp_client.HELP()

if __name__ == "__main__":
    main()