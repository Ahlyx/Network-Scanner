from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import scanner
import ipaddress 


app = FastAPI()
MAX_SCAN_ADDRESSES = 256

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/scan")
@limiter.limit("5/minute")
def run_scan(request: Request, subnet: str = "192.168.234.0/24"):
    try:
        network = ipaddress.ip_network(subnet, strict=False)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid IPv4 subnet")

    if not isinstance(network, ipaddress.IPv4Network):
        raise HTTPException(status_code=400, detail="only IPv4 lab subnets are supported")
    if network.num_addresses > MAX_SCAN_ADDRESSES:
        raise HTTPException(status_code=400, detail="subnet is too large; maximum is /24")
    
    hosts = scanner.scan(network.with_prefixlen)
    return {
        "subnet": network.with_prefixlen,
        "hosts_found": len(hosts),
        "hosts": hosts
    }
