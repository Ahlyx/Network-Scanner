from scapy.all import ARP, Ether, srp, conf
import socket

conf.verb = 0

# Known OT/ICS ports
OT_PORTS = {
    502: "Modbus",
    102: "S7comm (Siemens PLC)",
    20000: "DNP3",
    44818: "EtherNet/IP (Rockwell PLC)",
    47808: "BACnet",
    4840: "OPC-UA",
    1962: "PCWorx (Phoenix Contact)",
    2222: "EtherNet/IP",
    9600: "OMRON FINS",
}

# Common general ports to scan
COMMON_PORTS = [21, 22, 23, 80, 443, 8080, 8443] + list(OT_PORTS.keys())


def scan_ports(ip):
    open_ports = []
    for port in COMMON_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append({
                    "port": port,
                    "service": OT_PORTS.get(port, get_common_service(port)),
                    "ot_flag": port in OT_PORTS
                })
            sock.close()
        except Exception:
            pass
    return open_ports


def get_common_service(port):
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        80: "HTTP",
        443: "HTTPS",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
    }
    return services.get(port, "Unknown")


def scan(subnet):
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    answered, unanswered = srp(packet, iface="ens33", timeout=2, verbose=False)

    hosts = []
    for sent, received in answered:
        ip = received.psrc
        mac = received.hwsrc
        ports = scan_ports(ip)
        hosts.append({
            "ip": ip,
            "mac": mac,
            "ports": ports
        })

    return hosts


if __name__ == "__main__":
    subnet = "192.168.234.0/24"
    print(f"Scanning {subnet}...\n")

    hosts = scan(subnet)

    if not hosts:
        print("No hosts found.")
    else:
        print(f"Found {len(hosts)} host(s):\n")
        for host in hosts:
            print(f"  IP: {host['ip']:<16} MAC: {host['mac']}")
            if host['ports']:
                for p in host['ports']:
                    flag = " *** OT DEVICE ***" if p['ot_flag'] else ""
                    print(f"    Port {p['port']:<6} {p['service']}{flag}")
            else:
                print(f"    No open ports found")