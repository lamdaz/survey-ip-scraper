#!/usr/bin/env python3
"""
check_socks5.py
Reads socks5.txt (one proxy per line, allowed formats below),
checks SOCKS5 proxies concurrently, measures latency, performs geolocation,
and writes results.csv

Formats supported in socks5.txt:
 - 1.2.3.4:1080
 - 1.2.3.4:1080:username:password
"""

import asyncio
import csv
import time
import json
from typing import Optional, Tuple
import aiohttp
from aiohttp import ClientError
from aiohttp_socks import ProxyConnector, ProxyType

INPUT_FILE = "socks5.txt"
OUTPUT_FILE = "results.csv"
CONCURRENCY = 400           # adjust down if you get resource limits
TIMEOUT = 10                # seconds per attempt
RETRIES = 2                 # number of retries per proxy
GEO_API = "http://ip-api.com/json/"  # free; rate-limited. Replace if needed.

async def fetch_visible_ip(session: aiohttp.ClientSession, proxy_url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Call an IP-echo service to see what IP the remote site sees for this proxy.
    Returns (ip, error)
    """
    try:
        async with session.get("http://httpbin.org/ip", timeout=TIMEOUT) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("origin") or data.get("ip") or data.get("origin"), None
            return None, f"HTTP {resp.status}"
    except Exception as e:
        return None, str(e)

async def geolocate(session: aiohttp.ClientSession, ip: str) -> dict:
    """
    Query GEO_API for ip details. Non-fatal — returns empty dict on failure.
    """
    try:
        async with session.get(GEO_API + ip, timeout=TIMEOUT) as r:
            if r.status == 200:
                return await r.json()
    except Exception:
        pass
    return {}

def parse_proxy_line(line: str) -> Tuple[str, Optional[str]]:
    """
    Accepts:
      ip:port
      ip:port:user:pass
    Returns proxy_url (for aiohttp_socks ProxyConnector) and auth (unused; connector handles)
    """
    parts = line.strip().split(':')
    if len(parts) == 2:
        host, port = parts
        return f"socks5://{host}:{port}", None
    elif len(parts) >= 4:
        host, port, user, pw = parts[0], parts[1], parts[2], ":".join(parts[3:])
        return f"socks5://{user}:{pw}@{host}:{port}", None
    else:
        raise ValueError("Unsupported proxy line format")

async def check_proxy(proxy_line: str, sem: asyncio.Semaphore) -> dict:
    proxy_line = proxy_line.strip()
    if not proxy_line:
        return {"proxy": "", "status": "skipped", "error": "empty line"}
    try:
        proxy_url, _ = parse_proxy_line(proxy_line)
    except Exception as e:
        return {"proxy": proxy_line, "status": "bad_format", "error": str(e)}

    # Use a ProxyConnector for socks5
    # aiohttp_socks ProxyConnector accepts proxy_type and host/port OR accepts proxy URL in constructor
    # We'll rely on the proxy_url above.
    for attempt in range(1, RETRIES + 2):
        try:
            async with sem:
                start = time.perf_counter()
                connector = ProxyConnector.from_url(proxy_url, rdns=True)
                timeout = aiohttp.ClientTimeout(total=TIMEOUT+2)
                async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                    ip, ip_err = await fetch_visible_ip(session, proxy_url)
                latency = time.perf_counter() - start

            if ip:
                # geolocate the reported IP (best-effort)
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT+2)) as geo_sess:
                    geo = await geolocate(geo_sess, ip.split(',')[0].strip())
                return {
                    "proxy": proxy_line,
                    "status": "ok",
                    "latency_s": round(latency, 3),
                    "visible_ip": ip,
                    "country": geo.get("country"),
                    "region": geo.get("regionName"),
                    "city": geo.get("city"),
                    "isp": geo.get("isp"),
                    "error": ""
                }
            else:
                # If it explicitly failed with an error, retry up to RETRIES
                final_err = ip_err or "unknown"
                if attempt <= RETRIES:
                    await asyncio.sleep(0.1)  # tiny backoff
                    continue
                return {
                    "proxy": proxy_line,
                    "status": "dead",
                    "latency_s": "",
                    "visible_ip": "",
                    "country": "",
                    "region": "",
                    "city": "",
                    "isp": "",
                    "error": final_err
                }

        except asyncio.TimeoutError as e:
            err = "timeout"
        except ClientError as e:
            err = f"client_error:{e}"
        except Exception as e:
            err = f"error:{e}"

        # retry logic
        if attempt <= RETRIES:
            await asyncio.sleep(0.1)
            continue
        return {
            "proxy": proxy_line,
            "status": "dead",
            "latency_s": "",
            "visible_ip": "",
            "country": "",
            "region": "",
            "city": "",
            "isp": "",
            "error": err
        }

async def main():
    # read proxies
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    sem = asyncio.Semaphore(CONCURRENCY)
    tasks = [check_proxy(ln, sem) for ln in lines]

    results = []
    # gather in batches to avoid memory spikes
    BATCH = 500
    for i in range(0, len(tasks), BATCH):
        batch = tasks[i:i+BATCH]
        batch_results = await asyncio.gather(*batch)
        results.extend(batch_results)
        # optional: print progress
        print(f"Completed {min(i+BATCH, len(tasks))}/{len(tasks)}")

    # write CSV
    fieldnames = ["proxy","status","latency_s","visible_ip","country","region","city","isp","error"]
    with open(OUTPUT_FILE, "w", newline='', encoding="utf-8") as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    # also dump summary
    ok = sum(1 for r in results if r["status"] == "ok")
    dead = sum(1 for r in results if r["status"] == "dead")
    print(f"Done. {ok} alive, {dead} dead. Results: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
