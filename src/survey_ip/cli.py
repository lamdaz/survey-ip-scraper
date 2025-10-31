import argparse
import csv
from tqdm import tqdm
from .lookup import lookup_ip
import logging
import yaml
import os

logger = logging.getLogger(__name__)

DEFAULT_OUTPUT = "results.csv"

def load_ips_from_file(path):
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            yield line

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
