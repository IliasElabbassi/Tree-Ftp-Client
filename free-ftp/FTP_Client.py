from distutils.log import error
from lib2to3.pytree import Base
from queue import Empty
from re import S, VERBOSE
import socket
import sys
import logging

BUFFER_SIZE = 4080 # buffer size
FORMAT = "utf-8"
VERBOSE = False

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
    
    def read_multiple_line(self):
        read = True
        data = self.buffered_readLine()
        while read:
            if data.__contains__('OK.'):
                read = False
            else:
                print(data)
                data = self.buffered_readLine()

    def connect(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
            print(self.buffered_readLine())
            logging.info("Connection to the distant ftp server succeed {0}:{1} as {2}".format(self.HOST, self.PORT, self.USERNAME))
        except socket.error:
            logging.error("connection to the distant server failed {0}:{1}".format(self.HOST, self.PORT))
            sys.exit()


    def USER(self):
        try:
            if VERBOSE:
                print("$ USER")
            logging.info("send USER {0} cmd to {1}:{2}".format(self.USERNAME, self.HOST, self.PORT))
            self.socket.send("USER {0}\r\n".format(self.USERNAME).encode(FORMAT))
            print(self.buffered_readLine())
        except:
            logging.error("failed CONNECT:USER !!!")
            return

    def PASS(self):
        try:
            if VERBOSE:
                print("$ PASS")
            logging.info("send PASS cmd to {0}:{1}".format(self.HOST, self.PORT))
            self.socket.send("PASS RV\r\n".encode(FORMAT))
            print(self.buffered_readLine())
        except:
            logging.error("failed CONNECT:PASS !!!")
            return

    def PASV(self):
        try:
            if VERBOSE:
                print("$ PASV")
            logging.info("send PASV cmd to {0}:{1}".format(self.HOST, self.PORT))
            self.socket.send("PASV\r\n".encode(FORMAT))
            print(self.buffered_readLine())
        except BaseException:
            logging.error("failled CONNECT:PASV !!!")
            return

    def PORT(self, port):
        try:
            if VERBOSE:
                print("$ PORT")
            logging.info("send PORT {2} cmd to {0}:{1}".format(self.HOST, self.PORT, port))
            self.socket.send("PRT {0}\r\n".format(port).encode(FORMAT))
            print(self.buffered_readLine())
        except BaseException:
            logging.error("failled CONNECT:PORT !!!")
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
            if VERBOSE:
                print("$ LIST")
            logging.info("send LIST cmd to {0}:{1}".format(self.HOST, self.PORT))
            self.socket.send("LIST\r\n".encode(FORMAT))
            while True:
                print(self.buffered_readLine())
        except:
            logging.error("failed LIST_FILES:LIST !!!")
            return
    
    def HELP(self):
        logging.info("Starting HELP method...")

        try:
            if VERBOSE:
                print("$ HELP")
            logging.info("send HELP cmd to {0}:{1}".format(self.HOST, self.PORT))
            self.socket.send("HELP\r\n".encode(FORMAT))
            self.read_multiple_line()

        except:
            logging.error("failed HELP:HELP !!!")
            return

def main():
    if len(sys.argv) < 3:
        print("need args : HOST USERNAME")
        sys.exit()

    try:
        if sys.argv[3] == '-v':
            VERBOSE = True
    except:
        pass
    

    #host = "ftp.free.fr"
    host = sys.argv[1]
    username = sys.argv[2]

    ftp_client = FTP_Client(
        host=host,  
        username=username
    )
    ftp_client.connect()
    ftp_client.USER()
    ftp_client.PASS()
    #ftp_client.HELP()
    #ftp_client.PASV()
    #ftp_client.PORT(21)
    #ftp_client.list_files()

if __name__ == "__main__":
    main()