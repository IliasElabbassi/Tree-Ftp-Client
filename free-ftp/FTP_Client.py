from distutils.log import error
from queue import Empty
from re import S
import socket
import sys
import logging

BUFFER_SIZE = 1024 # standard buffer size
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
        buffer = ""
        data = self.getMsg()
        while data:
            buffer+=data
            data=self.getMsg
        
        return buffer

    def connect(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
            logging.info("Connection to the distant ftp server succeed {0}:{1} as {2}".format(self.HOST, self.PORT, self.USERNAME))
        except socket.error:
            logging.error("connection to the distant server failed {0}:{1}".format(self.HOST, self.PORT))
            sys.exit()

        try:
            self.socket.send("AUTH".encode(FORMAT))
            print(self.getMsg())
        except:
            logging.error("in CONNECT : ")

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
            print(self.getMsg())
        except:
            logging.error("Couldn't make the request")
            return
    
    def HELP(self):
        logging.info("Starting HELP method...")

        try:
            # send LIST cmd to the ftp server
            self.socket.send("HELP\r\n".encode(FORMAT))
            print(self.getMsg())
        except:
            logging.error("Couldn't make the request")
            return

        try:
            reply = ""
            while True:
                temp = self.socket.recv(BUFFER_SIZE)
                if temp:
                    reply += temp
                else:
                    break
            print(reply)
        except NameError:
            logging.error("in HELP: {0}".format(NameError))
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