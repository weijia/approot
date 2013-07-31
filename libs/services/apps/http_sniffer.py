import pcap
import libsys
from libs.windows.net_adapter import get_up_net
from libs.utils.network.http_request_sniffer import get_active_adapter, capture_http_request


def main():
    pc = pcap.pcap(get_up_net())
    #pc = pcap.pcap('\\Device\\NPF_{0C6699AA-C188-4B82-9E38-DB523EF58833}')
    pc.setfilter('tcp port 80')
    for uri, method, host in capture_http_request(pc):
        print uri, method, host


if __name__ == "__main__":
    main()

