import requests
import sys
import os
from ipwhois import IPWhois
from ipwhois.exceptions import IPDefinedError
import logging

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import rate_limited, safe_get

logger = logging.getLogger(__name__)

# ip-api.com free endpoint (no key) — check rate limits and terms
IP_API_URL = "http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,as,query,reverse,timezone"

@rate_limited(1.0)  # default: 1 request per second to be safe; override in CLI
def geoip_lookup_ipapi(ip: str) -> dict:
    """Query ip-api.com for geo + ASN + ISP + org. Returns dict (status==success) or raise."""
    resp = requests.get(IP_API_URL.format(ip=ip), timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise RuntimeError(f"ip-api error for {ip}: {data.get('message')}")
    # normalize keys
    return {
        "ip": data.get("query"),
        "country": data.get("country"),
        "region": data.get("regionName"),
        "city": data.get("city"),
        "zip": data.get("zip"),
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "isp": data.get("isp"),
        "org": data.get("org"),
        "as": data.get("as"),
        "reverse": data.get("reverse"),
    }

def rdap_lookup(ip: str) -> dict:
    """Get RDAP/WWHOIS-like registry data using ipwhois. Good for netname, org contact, rdap fields."""
    try:
        obj = IPWhois(ip)
        res = obj.lookup_rdap(depth=1)
    except IPDefinedError:
        return {}
    except Exception as e:
        logger.debug("RDAP lookup error for %s: %s", ip, e)
        return {}
    # extract common fields
    result = {}
    network = res.get("network", {}) or {}
    result["netname"] = network.get("name")
    result["country_reg"] = network.get("country")
    result["cidr"] = network.get("cidr")
    result["start_address"] = network.get("start_address")
    result["end_address"] = network.get("end_address")
    # org name (may be under entities)
    result["org_raw"] = str(res.get("objects", {}) or "")
    return result

def lookup_ip(ip: str, use_rdap=True) -> dict:
    out = {}
    try:
        out.update(geoip_lookup_ipapi(ip))
    except Exception as e:
        logger.warning("geoip lookup failed for %s: %s", ip, e)
    if use_rdap:
        rd = rdap_lookup(ip)
        out.update(rd)
    return out
