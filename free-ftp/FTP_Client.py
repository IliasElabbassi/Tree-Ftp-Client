import socket
import sys
import logging

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

    def connect(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
            logging.info("Connection to the distant ftp server succeed {0}:{1} as {2}".format(self.HOST, self.PORT, self.USERNAME))
        except socket.error:
            logging.error("connection to the distant server failed {0}:{1}".format(self.HOST, self.PORT))
            sys.exit()
    

def main():
    if len(sys.argv) < 3:
        print("need args : HOST USERNAME")
        sys.exit()

#    host = "ftp.free.fr"
    host = sys.argv[1]
    username = sys.argv[2]

    ftp_client = FTP_Client(
        host=host,
        username=username
    )
    ftp_client.connect()

if __name__ == "__main__":
    main()