from ftplib import FTP_TLS
ftps = FTP_TLS()
ftps.connect('127.0.0.1', 5000)
ftps.login('user', '12345')           # login anonymously before securing control channel
ftps.prot_p()          # switch to secure data connection
ftps.retrlines('LIST') # list directory content securely