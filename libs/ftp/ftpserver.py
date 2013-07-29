import argparse
import json
import os
import uuid

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from libs.utils.mobile.qrcode_image import get_qr_code


def main(port, root_dir, username, password):
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user(username, password, root_dir, perm='elradfmwM')
    #authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('0.0.0.0', port)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()


import socket

#Ref: http://www.pythonclub.org/python-network-application/get-ip-address
def get_local_ip():
    localIP = socket.gethostbyname(socket.gethostname())
    print "local ip:%s " % localIP

    ipList = socket.gethostbyname_ex(socket.gethostname())
    print ipList
    for i in ipList[2]:
        if i != localIP:
            print "external IP:%s" % i
            if "192.168" in i:
                return i


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    ############################
    # Default parameters
    parser.add_argument("--port", help="Ftp server port", default=21)
    parser.add_argument("--folder", help="Folder to serve", default=os.getcwd())
    #parser.add_argument("--username", help="Username for access the Ftpserver", default=None)
    #parser.add_argument("--password", help="Password for access the Ftpserver", default=None)
    #parser.add_argument("other", help="other options", nargs='*')
    #print sys.argv
    #print parser
    args = vars(parser.parse_args())

    setting_path = os.path.join(os.getcwd(), "setting.txt")
    try:
        f = open(setting_path, "r")
        setting = json.load(f)
        f.close()
    except:
        setting = {"username": str(uuid.uuid4()), "password": str(uuid.uuid4())}

    username = setting["username"]
    password = setting["password"]

    try:
        f = open(setting_path, "w")
        json.dump(setting, f, indent=4)
        f.close()
    except:
        print "Save setting error"

    print username, password

    local_ip = get_local_ip()

    url = "ftp://%s:%s@%s:%d" % (username, password, local_ip, int(args["port"]))
    print url

    qrcode_path = get_qr_code(url)
    os.startfile(qrcode_path)
    main(int(args["port"]), args["folder"], username, password)