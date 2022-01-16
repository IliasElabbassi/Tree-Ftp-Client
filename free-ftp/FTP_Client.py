from distutils.log import error
import socket
import sys
import logging

BUFFER_SIZE = 4080 # buffer size
FORMAT = "utf-8"
VERBOSE = True

class FTP_Client:
    def __init__(self, host, username):
        """
        PORT : to port of the ftp server
        HOST : the ip/url of the ftp server
        USERNAME : username set form the conenction
        socket : the socket that permit us to send and receiv data from the ftp server
        """
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
        """
        Read single line from server
        """
        line = ""
        while True:
            part = self.socket.recv(1).decode(FORMAT)
            if part != "\n":
                line+=part
            elif part == "\n":
                break
        return line
    
    def read_multiple_line(self):
        """
        Read multiple line from server
        """
        read = True
        data = self.buffered_readLine()
        while read:
            if data.__contains__('OK.'):
                read = False
            else:
                print(data)
                data = self.buffered_readLine()

    def connect(self):
        """
        Connect to the ftp server
        """
        try:
            self.socket.connect((self.HOST, self.PORT))
            print(self.buffered_readLine())
            logging.info("Connection to the distant ftp server succeed {0}:{1} as {2}".format(self.HOST, self.PORT, self.USERNAME))
        except socket.error:
            logging.error("connection to the distant server failed {0}:{1}".format(self.HOST, self.PORT))
            sys.exit()

    def USER(self):
        """
        USER: set user name
        """
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
        """
        PASS: set a password
        """
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
        """
        PASV: goes into passive mode
        """
        try:
            if VERBOSE:
                print("$ PASV")
            logging.info("send PASV cmd to {0}:{1}".format(self.HOST, self.PORT))
            self.socket.send("PASV\r\n".encode(FORMAT))
            print(self.buffered_readLine())
        except BaseException:
            logging.error("failled CONNECT:PASV !!!")
            return

    def CMD_PORT(self):
        """
        PORT: change port of the conenction
        """
        try:
            if VERBOSE:
                print("$ PORT {0}".format(self.PORT))
            logging.info("send PORT {0} cmd to {1}:{2}".format(self.PORT, self.HOST, self.PORT))
            self.socket.send("PRT {0}\r\n".format(self.PORT).encode(FORMAT))
            print(self.buffered_readLine())
        except BaseException:
            logging.error("failled CONNECT:PORT !!!")
            return


    def list_files(self):
        """
        LIST: Show information of a specific file/folder or current folder

        this method will send a LIST commande to the FTP server and process the data received acordingly:
            -
            -
            -
        """
        try:
            # send LIST cmd to the ftp server
            if VERBOSE:
                print("$ LIST")
            logging.info("send LIST cmd to {0}:{1}".format(self.HOST, self.PORT))
            self.socket.send("LIST\r\n".encode(FORMAT))
            for i in range(0,20):
                print(self.buffered_readLine())
        except:
            logging.error("failed LIST_FILES:LIST !!!")
            raise
            return
    
  
    def HELP(self):
        """
        HELP: display all the cmd I can make
        """
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
    """
    if len(sys.argv) < 3:
        print("need args : HOST USERNAME")
        sys.exit()

    try:
        if sys.argv[3] == "-v":
            VERBOSE = True
    except:
        pass
    """
    
    try:
        #host = "ftp.free.fr"
        host = sys.argv[1]
        username = sys.argv[2]
    except:
        pass


    ftp_client = FTP_Client(
        host="ftp.ubuntu.com",  
        username="anonymous"
    )
    ftp_client.connect()
    ftp_client.USER()
    ftp_client.PASS()
    #ftp_client.HELP()
    #ftp_client.PASV()
    #ftp_client.CMD_PORT()
    ftp_client.list_files()

if __name__ == "__main__":
    main()