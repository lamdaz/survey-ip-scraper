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
    """Load IPs from file. Supports both plain IPs and IP:PORT format."""
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Parse IP:PORT or plain IP
            if ':' in line:
                parts = line.split(':')
                ip = parts[0].strip()
                port = parts[1].strip() if len(parts) > 1 else None
            else:
                ip = line.strip()
                port = None
            yield (ip, port, line)  # Return IP, port, and original line

def is_residential_proxy(isp_name, org_name):
    """Detect if proxy is residential based on ISP/org name."""
    if not isp_name and not org_name:
        return False
    
    # Common datacenter/hosting keywords (NOT residential)
    datacenter_keywords = [
        'digital ocean', 'digitalocean', 'linode', 'ovh', 'hetzner',
        'amazon', 'aws', 'azure', 'google cloud', 'gcp',
        'vultr', 'scaleway', 'hostinger', 'contabo',
        'choopa', 'quadranet', 'psychz', 'vpn', 'proxy',
        'hosting', 'server', 'datacenter', 'data center',
        'cloud', 'dedicated', 'colocation', 'colo'
    ]
    
    combined = f"{isp_name} {org_name}".lower()
    
    # If contains datacenter keywords, it's NOT residential
    for keyword in datacenter_keywords:
        if keyword in combined:
            return False
    
    # Major USA residential ISPs and mobile carriers
    usa_residential_isps = [
        # Mobile carriers
        't-mobile', 'tmobile', 't mobile',
        'verizon', 'verizon wireless',
        'at&t', 'att', 'at&t mobility',
        'sprint',
        'us cellular', 'uscellular',
        'boost mobile',
        'cricket wireless',
        'metro pcs', 'metropcs',
        
        # Cable/Broadband ISPs
        'comcast', 'xfinity',
        'charter', 'spectrum',
        'cox', 'cox communications',
        'optimum', 'cablevision',
        'mediacom',
        'suddenlink',
        'wow', 'wideopenwest',
        'rcn',
        'armstrong',
        
        # DSL/Fiber ISPs
        'centurylink', 'century link',
        'frontier', 'frontier communications',
        'windstream',
        'consolidated communications',
        'earthlink',
        'viasat',
        'hughesnet',
        
        # Regional ISPs
        'grande communications',
        'atlantic broadband',
        'wave broadband',
        'astound broadband',
        'sparklight',
        'midco',
        'buckeye',
    ]
    
    # Check for USA residential ISPs first (most reliable)
    for isp in usa_residential_isps:
        if isp in combined:
            return True
    
    # Common residential ISP keywords (international)
    residential_keywords = [
        'telecom', 'telecommunications', 'communications',
        'broadband', 'internet service',
        'cable', 'fiber', 'fibre', 'dsl',
        'mobile', 'wireless', 'cellular',
        'adsl', 'vdsl',
        'network provider', 'network services'
    ]
    
    for keyword in residential_keywords:
        if keyword in combined:
            return True
    
    # If it looks like a regular ISP name (not datacenter), likely residential
    return True

def main():
    parser = argparse.ArgumentParser(description="Survey IP metadata and filter residential proxies")
    parser.add_argument("--input", "-i", required=True, help="File with IPs, one per line (supports IP:PORT)")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="CSV output file")
    parser.add_argument("--socks5-output", "-s", default="socks5.txt", help="Output file for residential proxies")
    parser.add_argument("--no-rdap", action="store_true", help="Skip RDAP lookups")
    parser.add_argument("--rate", type=float, default=1.0, help="Requests per second to ip-api (default 1.0)")
    args = parser.parse_args()

    # Load IPs with port info
    ip_data = list(load_ips_from_file(args.input))
    if not ip_data:
        print("No IPs found in input")
        return

    fieldnames = ["ip","port","country","region","city","zip","lat","lon","isp","org","as","reverse","netname","country_reg","cidr","start_address","end_address","is_residential"]

    residential_proxies = []

    with open(args.output, "w", newline="", encoding="utf-8") as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames=fieldnames)
        writer.writeheader()
        
        for ip, port, original_line in tqdm(ip_data, desc="Processing IPs"):
            try:
                data = lookup_ip(ip, use_rdap=not args.no_rdap)
                
                # Check if residential
                isp = data.get("isp", "")
                org = data.get("org", "")
                is_residential = is_residential_proxy(isp, org)
                
                data["port"] = port or ""
                data["is_residential"] = "Yes" if is_residential else "No"
                
                # If residential and has port, add to socks5 output
                if is_residential and port:
                    residential_proxies.append(original_line)
                
            except Exception as e:
                logging.exception("Error processing %s: %s", ip, e)
                data = {"ip": ip, "port": port or "", "is_residential": "Unknown"}
            
            # Ensure all fields exist
            row = {k: data.get(k, "") for k in fieldnames}
            writer.writerow(row)

    print(f"Wrote results to {args.output}")
    
    # Write residential proxies to socks5.txt
    if residential_proxies:
        with open(args.socks5_output, "w") as f:
            f.write("\n".join(residential_proxies) + "\n")
        print(f"Found {len(residential_proxies)} residential proxies → {args.socks5_output}")
    else:
        print("No residential proxies found")

if __name__ == "__main__":
    main()
