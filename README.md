# Network Scanner

A Python-based network scanner that performs ARP host discovery, TCP port scanning, and OT/ICS protocol detection. Built with Scapy, FastAPI, and Rich — available as both a CLI tool and a web dashboard.

Built on Linux (Ubuntu) inside a VMware lab environment, designed with OT/ICS security in mind.

---

## Features

- ARP scan a subnet to discover live hosts and their MAC addresses
- TCP port scan each discovered host
- Automatic OT/ICS protocol flagging for industrial ports (Modbus, S7comm, DNP3, EtherNet/IP, BACnet, OPC-UA, and more)
- MAC vendor identification
- Rich CLI table output
- Web dashboard with real-time scan results
- Input validation to prevent subnet injection
- Rate limiting on the API (5 requests/minute)

---

## Project Structure

```
Network-Scanner/
│
├── api.py          # FastAPI backend — serves the web dashboard and scan endpoint
├── scanner.py      # Core scanning logic — ARP discovery and port scanning via Scapy
├── cli.py          # CLI interface using Rich for formatted terminal output
│
├── static/
│   └── index.html  # Web dashboard — HTML, CSS, JS in a single file
│
└── requirements.txt
```

---

## Requirements

- Python 3.12+
- Linux (Scapy requires raw socket access — run with `sudo`)
- Root/sudo privileges for ARP scanning

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### CLI

```bash
sudo venv/bin/python3 cli.py
```

Outputs a Rich-formatted table with discovered hosts, MAC addresses, vendor info, and open ports. OT ports are highlighted in red.

### Web Dashboard

Start the API server:

```bash
sudo venv/bin/python3 -m uvicorn api:app --reload
```

Open your browser and go to:

```
http://localhost:8000/static/index.html
```

Enter a subnet (e.g. `192.168.1.0/24`) and click **SCAN**.

### API Endpoint

```
GET /api/scan?subnet=192.168.1.0/24
```

Returns JSON:

```json
{
  "subnet": "192.168.1.0/24",
  "hosts_found": 2,
  "hosts": [
    {
      "ip": "192.168.1.1",
      "mac": "aa:bb:cc:dd:ee:ff",
      "ports": [
        {
          "port": 502,
          "service": "Modbus",
          "ot_flag": true
        }
      ]
    }
  ]
}
```

---

## OT/ICS Port Detection

The scanner flags the following industrial control system ports:

| Port  | Protocol         | Device Type                  |
|-------|------------------|------------------------------|
| 502   | Modbus           | PLCs, industrial controllers |
| 102   | S7comm           | Siemens PLCs                 |
| 20000 | DNP3             | Power/water infrastructure   |
| 44818 | EtherNet/IP      | Rockwell/Allen-Bradley PLCs  |
| 47808 | BACnet           | Building automation systems  |
| 4840  | OPC-UA           | Industrial data exchange     |
| 1962  | PCWorx           | Phoenix Contact devices      |
| 2222  | EtherNet/IP alt  | Industrial Ethernet          |
| 9600  | OMRON FINS       | OMRON PLCs                   |

---

## Security Notes

- CORS is restricted to `localhost` only
- Subnet input is validated using Python's `ipaddress` module before being passed to Scapy
- The web frontend uses `textContent` and `createElement` throughout — no `innerHTML` — to prevent XSS
- Rate limited to 5 scans per minute via slowapi
- Scapy requires root privileges for raw packet sending — always run with `sudo`

---

## Important

**Only scan networks you own or have explicit permission to scan.** Unauthorized network scanning is illegal in most jurisdictions. This tool is intended for use in lab environments and on networks you control.

---

## Tech Stack

- [Scapy](https://scapy.net/) — ARP packet crafting and network scanning
- [FastAPI](https://fastapi.tiangolo.com/) — REST API backend
- [Rich](https://rich.readthedocs.io/) — Terminal formatting
- [slowapi](https://github.com/laurentS/slowapi) — Rate limiting
- [uvicorn](https://www.uvicorn.org/) — ASGI server

---

## License

MIT
