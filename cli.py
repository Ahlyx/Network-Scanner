from rich.console import Console
from rich.table import Table
from rich import box
import scanner
import argparse


console = Console(emoji=False)

def get_vendor(mac):
    oui = mac[:8].upper()
    vendors = {
        "00:50:56": "VMware",
        "00:0C:29": "VMware VM",
        "00:1A:11": "Google",
        "B8:27:EB": "Raspberry Pi",
        "DC:A6:32": "Raspberry Pi",
        "00:17:88": "Philips Hue",
        "18:B4:30": "Nest",
        "AC:84:C6": "Tuya Smart",
    }
    return vendors.get(oui, "Unknown")


def display_results(hosts, subnet):
    table = Table(
        title=f"Network Scan Results — {subnet}",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )

    table.add_column("IP Address", style="cyan", width=18)
    table.add_column("MAC Address", style="white", width=20)
    table.add_column("Vendor", style="green", width=14)
    table.add_column("Open Ports", style="white", width=40)

    for host in hosts:
        vendor = get_vendor(host["mac"])

        if host["ports"]:
            port_lines = []
            for p in host["ports"]:
                if p["ot_flag"]:
                    port_lines.append(f"[red]{p['port']} {p['service']} ⚠ OT[/red]")
                else:
                    port_lines.append(f"{p['port']} {p['service']}")
            ports_str = "\n".join(port_lines)
        else:
            ports_str = "[dim]none[/dim]"

        table.add_row(host["ip"], host["mac"], vendor, ports_str)

    console.print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Network scanner - ARP scan with OT port detection"
    )
    parser.add_argument(
        "--subnet",
        default="192.168.234.0/24",
        help="Subnet to scan in CIDR notation e.g. 192.168.1.0/24"
    )
    args = parser.parse_args()
    subnet = args.subnet

    console.print(f"\n[cyan]Scanning {subnet}...[/cyan]\n")

    hosts = scanner.scan(subnet)

    if not hosts:
        console.print("[red]No hosts found.[/red]")
    else:
        console.print(f"[green]Found {len(hosts)} host(s)[/green]\n")
        display_results(hosts, subnet)