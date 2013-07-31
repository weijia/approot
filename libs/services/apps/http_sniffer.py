import pcap
from libs.utils.network.http_request_sniffer import get_active_adapter, capture_http_request


def main():
    #pc = pcap.pcap()
    pc = pcap.pcap(get_active_adapter())
    pc.setfilter('tcp port 80')
    for uri, method, host in capture_http_request(pc):
        print uri, method, host


if __name__ == "__main__":
    main()

