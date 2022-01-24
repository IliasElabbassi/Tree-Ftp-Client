import socket
import sys
import logging

from TreeFtp import Tree # Comment this if you want to launch with setuptools
# import Tree # Uncomment this if you want to launch without setuptools
import pickle

BUFFER_SIZE = 1024 # buffer size
FORMAT = "utf-8"

class FTP_Client:
    def __init__(self, host, username, verbose=False, level=3):
        """
        PORT : to port of the ftp server
        HOST : the ip/url of the ftp server
        USERNAME : username set form the conenction
        socket : the socket that permit us to send and receiv data from the ftp server
        verbose : if we need to show what is happening
        level : level of recursion after the root directory; when exploring the files
        """
        self.VERBOSE = verbose
        self.recursion_level= level
        self.root = Tree.Node("Files")
        self.level = 0
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

    def buffered_readLine_pasv(self):
        """
        Read single line from server
        """
        try:
            line = ""
            while True:
                part = self.pasv_socket.recv(1).decode(FORMAT)
                if part != "\n":
                    line+=part
                elif part == "\n":
                    break
            return line
        except:
            logging.error("Failed at readline pasv")
    
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
                if self.VERBOSE:
                    print(data)
                data = self.buffered_readLine()

    def connect(self):
        """
        Connect to the ftp server
        """
        try:
            self.socket.connect((self.HOST, self.PORT))
            self.socket.settimeout(5)
            if self.VERBOSE:
                print(self.buffered_readLine())
            else:
                self.buffered_readLine()
            logging.info("Connection to the distant ftp server succeed {0}:{1} as {2}".format(self.HOST, self.PORT, self.USERNAME))
        except socket.error:
            logging.error("connection to the distant server failed {0}:{1}".format(self.HOST, self.PORT))
            sys.exit()

    def USER(self):
        """
        USER: set user name
        """
        try:
            logging.info("send USER {0} cmd to {1}:{2}".format(self.USERNAME, self.HOST, self.PORT))
            self.socket.send("USER {0}\r\n".format(self.USERNAME).encode(FORMAT))
            if self.VERBOSE:
                print("$ USER")
                print(self.buffered_readLine())
            else:
                self.buffered_readLine()
        except:
            logging.error("failed CONNECT:USER !!!")
            return

    def PASS(self, psw="RV"):
        """
        PASS: set a password
        """
        try:
            logging.info("send PASS cmd to {0}:{1}".format(self.HOST, self.PORT))
            self.socket.send("PASS {0}\r\n".format(psw).encode(FORMAT))
            if self.VERBOSE:
                print("$ PASS")
                print(self.buffered_readLine())
            else:
                self.buffered_readLine()
        except:
            logging.error("failed CONNECT:PASS !!!")
            return

    def PASV(self):
        """
        PASV: goes into passive mode
        """
        try:
            logging.info("send PASV cmd to {0}:{1}".format(self.HOST, self.PORT))
            self.socket.send("PASV\r\n".encode(FORMAT))
            data = self.buffered_readLine()
            new = self.PASV_get_new_url(data)
            self.connect_args(new[0], new[1])

            if self.VERBOSE:
                print("$ PASV")
                print(data)
                print(new)

        except BaseException:
            logging.error("failled CONNECT:PASV !!!")
            return

    def PASV_get_new_url(self, data):
        data_split = data.split(" ")
        data_split = data_split[len(data_split)-1].split(",")
        data_split[0] = data_split[0].replace("(","")
        data_split[len(data_split)-1] = data_split[len(data_split)-1].replace(")","")
        data_split[len(data_split)-1] = data_split[len(data_split)-1].replace(".","")

        url = "{0}.{1}.{2}.{3}".format(
            data_split[0],
            data_split[1],
            data_split[2],
            data_split[3],
        )

        port = int(data_split[4])*256+int(data_split[5])

        return (url, str(port))

    def connect_args(self, host, port):
        """
        Connect to the ftp server, with different host/port
        """
        try:
            self.pasv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.pasv_socket.connect((host, int(port)))
            self.pasv_socket.settimeout(5)
            logging.info("Connection to the distant ftp server succeed {0}:{1} as {2}".format(host, port, self.USERNAME))
        except socket.error:
            logging.error("connection to the distant server failed {0}:{1}".format(host, port))
            sys.exit()

    def CMD_PORT(self, port):
        """
        PORT: change port of the conenction
        """
        try:

            logging.info("send PORT {0} cmd to {1}:{2}".format(port, self.HOST, self.PORT))
            self.socket.send("PORT {0}\r\n".format(port).encode(FORMAT))
            if self.VERBOSE:
                print("$ PORT {0}".format(port))
                print(self.buffered_readLine())
            else:
                self.buffered_readLine()
        except BaseException:
            logging.error("failled CONNECT:PORT !!!")
            return

    def list_files(self):
        """
        LIST: Show information of a specific file/folder or current folder
        """
        try:
            self.PASV() # ask for a new socket to read from
            # send LIST cmd to the ftp server
            logging.info("send LIST cmd to {0}:{1}".format(self.HOST, self.PORT)) # ask to send the list of files
            self.socket.send("LIST\r\n".encode(FORMAT))
            data = self.readFromPassivSocket() # read from the new socket generated in PASV

            if self.VERBOSE:
                print("$ LIST")
                print(self.buffered_readLine())
                print(self.buffered_readLine())
            else:
                self.buffered_readLine()
                self.buffered_readLine()
            return data
        except:
            logging.error("failed LIST_FILES:LIST !!!")
        
    def HELP(self):
        """
        HELP: display all the cmd I can make
        """
        try:
            if self.VERBOSE:
                print("$ HELP")
            logging.info("send HELP cmd to {0}:{1}".format(self.HOST, self.PORT))
            self.socket.send("HELP\r\n".encode(FORMAT))
            self.read_multiple_line()
        except:
            logging.error("failed HELP:HELP !!!")
            return

    def CMD(self, cmd_str):
        """
        CMD: send cmd_str to ftp server
        """
        try:
            logging.info("send {0} cmd to {1}:{2}".format(cmd_str, self.HOST, self.PORT))
            self.socket.send("{0}\r\n".format(cmd_str).encode(FORMAT))
            if self.VERBOSE:
                print("$ {0}".format(cmd_str))
                print(self.buffered_readLine())
            else:
                self.buffered_readLine()
        except:
            logging.error("failed HELP:{0} !!!".format(cmd_str))
            return
        
    def CWD(self, to):
        try:
            logging.info("send CWD {0} cmd".format(to))
            self.socket.send("CWD {0}\r\n".format(to).encode(FORMAT)) # ask to change current working directory
            if self.VERBOSE:
                print("$ CWD {0}".format(to))
                print(self.buffered_readLine())
            else:
                self.buffered_readLine()
        except:
            logging.error("faield CWD {0}!!".format(to))

    def readFromPassivSocket(self):
        try:
            logging.info("Reading from passive socket...")
            data, address = self.pasv_socket.recvfrom(BUFFER_SIZE) # read until there is no data
            if self.VERBOSE:
                print(data.decode(FORMAT))
            # output = open("output.pickle", "wb")
            # pickle.dump(data, output)
            # output.close()
            return data
        except socket.timeout:
            logging.error("Didn't receive data! [Timeout 5s]")

    def gotFilesFromData(self, data):
        if data:
            logging.info("Parsing data from list files...")
            data_split = data.decode(FORMAT).split("\n")

            file_dir = []
            dir = []
            for ele in data_split:
                dir.append(ele.split(" ")[-1].replace("\r", ""))
                file_dir.append(ele.split(" ")[0][:1])
                #print(dir[-1])
            dir.pop()
            file_dir.pop()

            result = []
            for i in range(0,len(dir)-1):
                result.append((
                    file_dir[i],
                    dir[i]
                ))
            return result

        return ""
    
    def generateData(self, data):
        res = self.gotFilesFromData(data)
        self.createChildren(res)

    def createChildren(self, dir):
        logging.info("Creating the tree of files...")
        for ele in dir:
            new_dir = Tree.Node(ele[1], ele[0])
            self.root.add_child(new_dir)
        
        self.root.done = True
    
    def getAllFiles(self, stack, level=0):
        import copy
        stack_c = copy.copy(stack)

        if level >= self.recursion_level:
            return
        while len(stack_c) > 0:
            stack_c.pop(0)
            parent = stack.pop(0)
            if parent.type == "d":
                self.CWD(parent.data)
                data = self.list_files()
                res = self.gotFilesFromData(data)
                for ele in res:
                    new_dir = Tree.Node(ele[1], ele[0])
                    parent.add_child(new_dir)
                stack.append(parent)
                self.getAllFiles(parent.children, level=level+1)
                self.CWD("..")
            else:
                stack.append(parent)
    
    def launch(self, psw="RV"):
        self.connect()
        self.USER()
        self.PASS(psw)

        data = self.list_files()
        self.generateData(data)

        self.getAllFiles(self.root.children)
        self.root.print_tree()
        
def main():
    host = None
    username = None
    VERBOSE = False

    try:
        host = sys.argv[1]
        username = sys.argv[2]
        args = ""

        for i in range(0, len(sys.argv)):
            args +=  sys.argv[i]+" "

        args = args.lower()
        if args.__contains__("-v") or args.__contains__("--v") or args.__contains__("-verbose"):
            VERBOSE = True
    except:
        print("We need the ftp server and username to launch !")
        return -1

    ftp_client = FTP_Client(
        host=host,
        username=username,
        verbose=VERBOSE
    ).launch()


if __name__ == "__main__":
    main()