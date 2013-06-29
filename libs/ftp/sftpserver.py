#!/usr/bin/env python

"""
An RFC-4217 asynchronous FTPS server supporting both SSL and TLS.
Requires PyOpenSSL module (http://pypi.python.org/pypi/pyOpenSSL).
"""

from cert import gen_cer_file

from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
import libsys
from configuration import g_config_dict

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('user', '12345abcdef6789', 'c:\\', perm='elradfmw')
    authorizer.add_anonymous('.')
    handler = TLS_FTPHandler
    handler.certfile = 'cert.pem'
    gen_cer_file(handler.certfile)
    handler.authorizer = authorizer
    # requires SSL for both control and data channel
    #handler.tls_control_required = True
    #handler.tls_data_required = True
    print 'opening port on:', g_config_dict["ufs_sftp_server_port"]
    server = FTPServer(('', int(g_config_dict["ufs_sftp_server_port"])), handler)
    server.serve_forever()

if __name__ == '__main__':
    main()