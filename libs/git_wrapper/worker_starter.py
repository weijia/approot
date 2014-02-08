import Pyro4




if __name__ == '__main__':

    pyro_daemon = Pyro4.Daemon(port=8018)
    uri = self.pyro_daemon.register(self, "ufs_launcher")
    ns = Pyro4.locateNS()
    ns.register("ufs_launcher", uri)
    print "uri=", uri
    self.pyro_daemon.requestLoop()