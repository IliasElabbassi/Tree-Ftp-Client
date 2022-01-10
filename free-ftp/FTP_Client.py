import socket
import sys
import logging

class FTP_Client:
    def __init__(self):
        self.PORT = 21 
        self.HOST = "ftp.free.fr"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setupLogger()

    def setupLogger(self):
        self.logger = logging.getLogger('FTP Client Logs')
        logging.basicConfig(
            filename='test.log',
            level=logging.DEBUG,
            format='%(asctime)s:%(levelname)s:%(message)s'
            )

    def connect(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
            logging.info("Connection to the distant ftp server succeed {0}:{1}".format(self.HOST, self.PORT))
        except socket.error:
            logging.error("connection to the distant server failed {0}:{1}".format(self.HOST, self.PORT))
            sys.exit()
    

def main():
    ftp_client = FTP_Client()
    ftp_client.connect()

if __name__ == "__main__":
    main()