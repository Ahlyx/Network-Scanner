from scapy.all import ARP, Ether, srp, conf
conf.verb = 0


def scan(subnet):
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    answered, unanswered = srp(packet, iface="ens33", timeout=2, verbose=False)

    hosts = []
    for sent, received in answered:
        hosts.append({
            "ip": received.psrc,
            "mac": received.hwsrc
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