#!/usr/bin/env python

import getopt, sys
import dpkt, pcap

def usage():
    print >>sys.stderr, 'usage: %s [-i device] [pattern]' % sys.argv[0]
    sys.exit(1)

def main():
    opts, args = getopt.getopt(sys.argv[1:], 'i:h')
    name = None
    for o, a in opts:
        if o == '-i': name = a
        else: usage()

    pc = pcap.pcap(name)
    pc.setfilter('tcp port 8080')#8080 is the proxy port.
    decode = { pcap.DLT_LOOP:dpkt.loopback.Loopback,
               pcap.DLT_NULL:dpkt.loopback.Loopback,
               pcap.DLT_EN10MB:dpkt.ethernet.Ethernet }[pc.datalink()]
    try:
        print 'listening on %s: %s' % (pc.name, pc.filter)
        for ts, pkt in pc:
            #print ts, pkt
            #print ts, `decode(pkt)`
            eth = dpkt.ethernet.Ethernet(pkt)
            ip = eth.data
            tcp = ip.data
            if tcp.dport == 8080 and len(tcp.data) > 0:
                try:
                    http = dpkt.http.Request(tcp.data)
                    print http.uri
                    print http
                except:
                    #print tcp.data
                    pass

    except KeyboardInterrupt:
        nrecv, ndrop, nifdrop = pc.stats()
        print '\n%d packets received by filter' % nrecv
        print '%d packets dropped by kernel' % ndrop

if __name__ == '__main__':
    main()

