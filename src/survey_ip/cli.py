import argparse
import csv
import sys
import os
from tqdm import tqdm
import logging
import yaml

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lookup import lookup_ip

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT = "results.csv"

def load_ips_from_file(path):
    """Load IPs from file. Supports both plain IPs and IP:PORT format (extracts IP only)."""
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Extract IP from IP:PORT format if present
            if ':' in line:
                ip = line.split(':')[0]
            else:
                ip = line
            yield ip.strip()

def main():
    parser = argparse.ArgumentParser(description="Survey IP metadata")
    parser.add_argument("--input", "-i", required=True, help="File with IPs, one per line")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT)
    parser.add_argument("--no-rdap", action="store_true", help="Skip RDAP lookups")
    parser.add_argument("--rate", type=float, default=1.0, help="Requests per second to ip-api (default 1.0)")
    args = parser.parse_args()

    # NOTE: rate control is set in lookup decorator by default. For more control, you can edit code.
    ips = list(load_ips_from_file(args.input))
    if not ips:
        print("No IPs found in input")
        return

    fieldnames = ["ip","country","region","city","zip","lat","lon","isp","org","as","reverse","netname","country_reg","cidr","start_address","end_address"]

    with open(args.output, "w", newline="", encoding="utf-8") as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames=fieldnames)
        writer.writeheader()
        for ip in tqdm(ips, desc="Processing IPs"):
            try:
                data = lookup_ip(ip, use_rdap=not args.no_rdap)
            except Exception as e:
                logging.exception("Error processing %s: %s", ip, e)
                data = {"ip": ip}
            # ensure all fields exist
            row = {k: data.get(k, "") for k in fieldnames}
            writer.writerow(row)

    print(f"Wrote results to {args.output}")

if __name__ == "__main__":
    main()
