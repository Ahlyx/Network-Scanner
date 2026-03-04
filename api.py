from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import scanner
import ipaddress 



app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/scan")
@limiter.limit("5/minute")
def run_scan(request: Request, subnet: str = "192.168.234.0/24"):
    try:
        ipaddress.IPv4Network(subnet, strict=False)
    except ValueError:
        return {"error": "Invalid subnet format"}
    
    hosts = scanner.scan(subnet)
    return {
        "subnet": subnet,
        "hosts_found": len(hosts),
        "hosts": hosts
    }
