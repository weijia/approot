import OpenSSL
import os

def gen_cer_file(filename = 'cert.pem'):
    if os.path.exists(filename):
        print 'cert exists'
        return
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

    ca = OpenSSL.crypto.X509()
    ca.set_version(3)
    ca.set_serial_number(1)
    ca.get_subject().CN = "zpadtech.com"
    ca.gmtime_adj_notBefore(0)
    ca.gmtime_adj_notAfter(24 * 60 * 60)
    ca.set_issuer(ca.get_subject())
    ca.set_pubkey(key)
    ca.add_extensions([
      OpenSSL.crypto.X509Extension("basicConstraints", True,
                                   "CA:TRUE, pathlen:0"),
      OpenSSL.crypto.X509Extension("keyUsage", True,
                                   "keyCertSign, cRLSign"),
      OpenSSL.crypto.X509Extension("subjectKeyIdentifier", False, "hash",
                                   subject=ca),
      ])
    ca.sign(key, "sha1")

    '''
    key = OpenSSL.crypto.PKey()
    key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
    '''

    req = OpenSSL.crypto.X509Req()
    req.get_subject().CN = "zpadtech.com"
    req.set_pubkey(key)
    req.sign(key, "sha1")

    f = open(filename, "w")
    # Write private key
    #print OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
    f.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key))

    '''
    # Write request
    print OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_PEM, req)


    '''


    '''
    ca_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                              "ca.pem")
    ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM,
                                            "ca.pem")
    req = OpenSSL.crypto.load_certificate_request(OpenSSL.crypto.FILETYPE_PEM,
                                                  open("req.csr").read())
    '''
    ca_cert = ca
    ca_key = key
    cert = OpenSSL.crypto.X509()
    cert.set_subject(req.get_subject())
    cert.set_serial_number(1)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(24 * 60 * 60)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(ca_key, "sha1")

    #print OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    f.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
    
if __name__ == '__main__':
    gen_cer_file()