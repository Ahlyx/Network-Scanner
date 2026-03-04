from scapy.all import ARP, Ether, srp



def scan(subnet):
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    print(f"Sending packets on interface: {r'\Device\NPF_{54127133-D621-44A7-ACF7-2170E801C8AA}'}")
    print(f"Packet summary: {packet.summary()}")

    # verbose=True this time so we can see what's happening
    answered, unanswered = srp(packet, iface=r"\Device\NPF_{54127133-D621-44A7-ACF7-2170E801C8AA}", timeout=2, verbose=True)
    
    print(f"\nAnswered: {len(answered)}")
    print(f"Unanswered: {len(unanswered)}")

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