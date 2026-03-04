from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import scanner

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/scan")
def run_scan(subnet: str = "192.168.234.0/24"):
    hosts = scanner.scan(subnet)
    return {
        "subnet": subnet,
        "hosts_found": len(hosts),
        "hosts": hosts
    }
