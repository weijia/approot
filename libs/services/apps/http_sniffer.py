import pcap
import libsys
from libs.utils.network.http_request_sniffer import get_active_adapter, capture_http_request


def main():
    #pc = pcap.pcap()
    pc = pcap.pcap(get_active_adapter())
    pc.setfilter('tcp port 80')
    for uri, method, host, headers, body in capture_http_request(pc):
        if "cang.baidu.com" in host:
            print method, uri, host, headers, body
        else:
            print method, uri, host, headers


if __name__ == "__main__":
    main()

