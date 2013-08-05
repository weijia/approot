#Modified from http://www.thescriptlibrary.com/default.asp?Action=Display&Level=Category3&ScriptLanguage=Python&Category1=Networking&Category2=Client-Side%20Management&Title=List%20Network%20Adapter%20Configuration%20Properties
import win32com.client


def get_up_net():
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
    colItems = objSWbemServices.ExecQuery("Select * from Win32_NetworkAdapterConfiguration")
    for objItem in colItems:

        print '-----------------------------------------------------'
        print "Arp Always Source Route: ", objItem.ArpAlwaysSourceRoute
        print "Arp Use EtherSNAP: ", objItem.ArpUseEtherSNAP
        print "Caption: ", objItem.Caption
        print "Database Path: ", objItem.DatabasePath
        print "Dead GW Detect Enabled: ", objItem.DeadGWDetectEnabled
        z = objItem.DefaultIPGateway
        if z is None:
            a = 1
        else:
            for x in z:
                print "Default IP Gateway: ", x
        print "Default TOS: ", objItem.DefaultTOS
        print "Default TTL: ", objItem.DefaultTTL
        print "Description: ", objItem.Description
        print "DHCP Enabled: ", objItem.DHCPEnabled
        print "DHCP Lease Expires: ", objItem.DHCPLeaseExpires
        print "DHCP Lease Obtained: ", objItem.DHCPLeaseObtained
        print "DHCP Server: ", objItem.DHCPServer
        print "DNS Domain: ", objItem.DNSDomain
        z = objItem.DNSDomainSuffixSearchOrder
        if z is None:
            a = 1
        else:
            for x in z:
                print "DNS Domain Suffix Search Order: ", x
        print "DNS Enabled For WINS Resolution: ", objItem.DNSEnabledForWINSResolution
        print "DNS Host Name: ", objItem.DNSHostName
        z = objItem.DNSServerSearchOrder
        if z is None:
            a = 1
        else:
            for x in z:
                print "DNS Server Search Order: ", x
        print "Domain DNS Registration Enabled: ", objItem.DomainDNSRegistrationEnabled
        print "Forward Buffer Memory: ", objItem.ForwardBufferMemory
        print "Full DNS Registration Enabled: ", objItem.FullDNSRegistrationEnabled
        z = objItem.GatewayCostMetric
        if z is None:
            a = 1
        else:
            for x in z:
                print "Gateway Cost Metric: ", x
        print "IGMP Level: ", objItem.IGMPLevel
        print "Index: ", objItem.Index
        z = objItem.IPAddress
        if z is None:
            a = 1
        else:
            for x in z:
                print "IP Address: ", x
        print "IP Connection Metric: ", objItem.IPConnectionMetric
        print "IP Enabled: ", objItem.IPEnabled
        print "IP Filter Security Enabled: ", objItem.IPFilterSecurityEnabled
        print "IP Port Security Enabled: ", objItem.IPPortSecurityEnabled
        z = objItem.IPSecPermitIPProtocols
        if z is None:
            a = 1
        else:
            for x in z:
                print "IP Sec Permit IP Protocols: ", x
        z = objItem.IPSecPermitTCPPorts
        if z is None:
            a = 1
        else:
            for x in z:
                print "IP Sec Permit TCP Ports: ", x
        z = objItem.IPSecPermitUDPPorts
        if z is None:
            a = 1
        else:
            for x in z:
                print "IPSec Permit UDP Ports: ", x
        z = objItem.IPSubnet
        if z is None:
            a = 1
        else:
            for x in z:
                print "IP Subnet: ", x
        print "IP Use Zero Broadcast: ", objItem.IPUseZeroBroadcast
        print "IPX Address: ", objItem.IPXAddress
        print "IPX Enabled: ", objItem.IPXEnabled
        z = objItem.IPXFrameType
        if z is None:
            a = 1
        else:
            for x in z:
                print "IPX Frame Type: ", x
        print "IPX Media Type: ", objItem.IPXMediaType
        z = objItem.IPXNetworkNumber
        if z is None:
            a = 1
        else:
            for x in z:
                print "IPX Network Number: ", x
        print "IPX Virtual Net Number: ", objItem.IPXVirtualNetNumber
        print "Keep Alive Interval: ", objItem.KeepAliveInterval
        print "Keep Alive Time: ", objItem.KeepAliveTime
        print "MAC Address: ", objItem.MACAddress
        print "MTU: ", objItem.MTU
        print "Num Forward Packets: ", objItem.NumForwardPackets
        print "PMTUBH Detect Enabled: ", objItem.PMTUBHDetectEnabled
        print "PMTU Discovery Enabled: ", objItem.PMTUDiscoveryEnabled
        print "Service Name: ", objItem.ServiceName
        print "Setting ID: ", objItem.SettingID
        print "Tcpip Netbios Options: ", objItem.TcpipNetbiosOptions
        print "Tcp Max Connect Retransmissions: ", objItem.TcpMaxConnectRetransmissions
        print "Tcp Max Data Retransmissions: ", objItem.TcpMaxDataRetransmissions
        print "Tcp Num Connections: ", objItem.TcpNumConnections
        print "Tcp Use RFC1122 Urgent Pointer: ", objItem.TcpUseRFC1122UrgentPointer
        print "Tcp Window Size: ", objItem.TcpWindowSize
        print "WINS Enable LMHosts Lookup: ", objItem.WINSEnableLMHostsLookup
        print "WINS Host Lookup File: ", objItem.WINSHostLookupFile
        print "WINS Primary Server: ", objItem.WINSPrimaryServer
        print "WINS Scope ID: ", objItem.WINSScopeID
        print "WINS Secondary Server: ", objItem.WINSSecondaryServer

        if objItem.IPEnabled:
            #if "VirtualBox" in objItem.Description:
            #    print "virtual box adapter", objItem.Description
            #    continue
            z = objItem.IPAddress
            if z is None:
                #print "ip address:", z
                continue
            else:
                for x in z:
                    if "0.0.0.0" in x:
                        #print "0.0.0.0 in address:", x
                        continue
                    if "169.254" in x:
                        #print "169.254 in address:", x
                        continue
                    if "192.168.56" in x:
                        #print "192.168.56 in address:", x
                        continue
                    print "valid adapter:", "\\Device\\NPF_"+objItem.SettingID
                    return "\\Device\\NPF_"+objItem.SettingID
        else:
            #print "objItem.IPEnabled", objItem.IPEnabled
            pass

if __name__ == "__main__":
    get_up_net()