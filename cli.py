from rich.console import Console
from rich.table import Table
from rich import box
import scanner

console = Console()



def display_results(hosts, subnet):
    table = Table(
        title=f"Network Scan Results — {subnet}",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )

    table.add_column("IP Address", style="cyan", width=20)
    table.add_column("MAC Address", style="white", width=20)
    table.add_column("Vendor", style="green", width=20)

    for host in hosts:
        vendor = get_vendor(host["mac"])
        table.add_row(host["ip"], host["mac"], vendor)

    console.print(table)

def get_vendor(mac):
    # Check the first 8 characters (OUI prefix) of the MAC address
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


if __name__ == "__main__":
    subnet = "192.168.234.0/24"

    console.print(f"\n[cyan]Scanning {subnet}...[/cyan]\n")

    hosts = scanner.scan(subnet)

    if not hosts:
        console.print("[red]No hosts found.[/red]")
    else:
        console.print(f"[green]Found {len(hosts)} host(s)[/green]\n")
        display_results(hosts, subnet)