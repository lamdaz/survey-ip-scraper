# Survey IP Metadata - IP Geolocation & Company Detection

A Python tool for scraping and analyzing IP addresses to detect geographic location, ISP/company information, ASN data, and network registration details.















































































































































<!-- AUTO-GENERATED STATS - DO NOT EDIT MANUALLY -->
## 📊 Latest Scan Results

**Last Updated:** 2025-11-01 17:25:42 UTC

- **Total IPs Scanned:** 12
- **Unique Countries:** 9
- **Unique ISPs:** 7

### Top Countries
- United States: 4 IPs
- Vietnam: 1 IPs
- The Netherlands: 1 IPs
- South Korea: 1 IPs
- India: 1 IPs

### Top ISPs
- DigitalOcean, LLC: 4 IPs
- Performive LLC: 3 IPs
- Vietnam Posts and Telecommunications Group: 1 IPs
- Korea Telecom: 1 IPs
- Global Connectivity Solutions LLP: 1 IPs

<!-- END AUTO-GENERATED STATS -->














































































































































## Features

✅ **Geolocation Detection**: Country, region, city, coordinates, timezone  
✅ **ISP & Organization Detection**: Identify which company owns the IP  
✅ **ASN Information**: Autonomous System Number and details  
✅ **RDAP/WHOIS Data**: Network registration information  
✅ **Reverse DNS Lookup**: Hostname resolution  
✅ **Rate Limiting**: Configurable request throttling  
✅ **Batch Processing**: Process multiple IPs from file  
✅ **CSV Export**: Results exported to CSV format  

## Installation

### Prerequisites
- Python 3.8 or higher
- Conda (recommended) or pip package manager

### Option 1: Using Conda (Recommended)

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate proxycheck

# You're ready to go!
```

### Option 2: Using pip

```bash
# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Quick Start Script

For the easiest setup, simply run:

```bash
# Make the script executable (first time only)
chmod +x run_local.sh

# Run the tool with sample data
./run_local.sh
```

This script will automatically:
- Check for conda installation
- Create the environment if needed
- Run the tool with sample data
- Display the results

## Usage

### Basic Usage

Process a list of IP addresses from a file:

```bash
python -m survey_ip.cli --input data/sample_ips.txt --output results.csv
```

### Command Line Options

```bash
python -m survey_ip.cli [OPTIONS]

Options:
  -i, --input FILE      Input file with IP addresses (one per line) [REQUIRED]
  -o, --output FILE     Output CSV file (default: results.csv)
  --no-rdap            Skip RDAP/WHOIS lookups (faster but less data)
  --rate FLOAT         Requests per second to ip-api.com (default: 1.0)
  -h, --help           Show help message
```

### Input Format

Create a text file with one IP address per line. **Supports both plain IPs and IP:PORT format** (commonly used for proxies/SOCKS5):

```
# Plain IP addresses
8.8.8.8
1.1.1.1
93.184.216.34

# IP:PORT format (tool extracts IP only)
103.82.27.24:10001
104.248.197.67:1080
107.152.98.5:4145

# Comments starting with # are ignored
```

**Perfect for proxy lists!** The tool automatically extracts the IP from IP:PORT format.

### Example

```bash
# Process IPs with default settings
python -m survey_ip.cli --input my_ips.txt

# Faster processing without RDAP lookups
python -m survey_ip.cli --input my_ips.txt --no-rdap --rate 2.0

# Custom output file
python -m survey_ip.cli --input my_ips.txt --output ip_report.csv
```

## Output Data

The tool generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| `ip` | IP address |
| `country` | Country name |
| `region` | Region/state name |
| `city` | City name |
| `zip` | Postal code |
| `lat` | Latitude coordinate |
| `lon` | Longitude coordinate |
| `isp` | Internet Service Provider name |
| `org` | Organization name |
| `as` | Autonomous System info (ASN) |
| `reverse` | Reverse DNS hostname |
| `netname` | Network name from RDAP |
| `country_reg` | Country from registry |
| `cidr` | CIDR notation of IP block |
| `start_address` | Start of IP range |
| `end_address` | End of IP range |

### Sample Output

```csv
ip,country,region,city,isp,org,as
8.8.8.8,United States,California,Mountain View,Google LLC,Google LLC,AS15169 Google LLC
1.1.1.1,Australia,Queensland,Brisbane,Cloudflare Inc,APNIC Research and Development,AS13335 Cloudflare Inc.
```

## Project Structure

```
survey-ip-metadata/
├── src/
│   └── survey_ip/
│       ├── __init__.py
│       ├── cli.py              # Command-line interface
│       ├── lookup.py           # IP lookup logic
│       ├── utils.py            # Helper functions
│       └── config_example.yaml # Configuration example
├── data/
│   └── sample_ips.txt          # Sample IP addresses
├── tests/
│   └── test_lookup.py          # Unit tests
├── .gitignore
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project metadata
└── README.md                  # This file
```

## API Usage

You can also use the library programmatically:

```python
from survey_ip.lookup import lookup_ip

# Lookup a single IP
result = lookup_ip("8.8.8.8", use_rdap=True)
print(result)
# Output: {'ip': '8.8.8.8', 'country': 'United States', 'isp': 'Google LLC', ...}

# Lookup without RDAP (faster)
result = lookup_ip("1.1.1.1", use_rdap=False)
```

## Data Sources

This tool uses the following free services:

- **ip-api.com**: Geolocation, ISP, organization, ASN data
  - Free tier: 45 requests/minute
  - Documentation: https://ip-api.com/docs
  
- **RDAP (Registration Data Access Protocol)**: Network registration details
  - Provides netname, CIDR, registry information
  - Uses `ipwhois` library

## Rate Limiting

To respect API rate limits and avoid being blocked:

- Default rate: 1 request per second (safe for ip-api.com free tier)
- Adjustable via `--rate` parameter
- ip-api.com limit: 45 requests/minute (0.75 req/sec)
- Consider upgrading to paid plan for higher volumes

## Testing

Run the test suite:

```bash
pytest tests/
```

Or test with sample data:

```bash
python -m survey_ip.cli --input data/sample_ips.txt --output test_results.csv
```

## Use Cases

- 🔍 **Security Analysis**: Identify suspicious IP addresses and their origins
- 📊 **Survey Analytics**: Understand geographic distribution of survey respondents
- 🌐 **Network Monitoring**: Track and analyze network traffic sources
- 🚫 **Fraud Detection**: Identify VPN/proxy usage and geographic anomalies
- 📈 **Marketing Analytics**: Analyze visitor demographics and locations
- 🔒 **Compliance**: Ensure data residency and geographic restrictions

## Limitations

- **Rate Limits**: Free APIs have rate limits; use responsibly
- **Accuracy**: Geolocation accuracy varies; may be inaccurate for VPNs/proxies
- **Private IPs**: Cannot lookup private IP ranges (10.x, 192.168.x, etc.)
- **IPv6**: Currently optimized for IPv4 addresses

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - see LICENSE file for details

## Disclaimer

This tool is for educational and legitimate research purposes only. Always ensure you have permission to scan IP addresses and comply with applicable laws and terms of service.

## Troubleshooting

### Common Issues

**Problem**: `IPDefinedError` for private IPs  
**Solution**: Only use public IP addresses (not 10.x, 192.168.x, 172.16-31.x, or 127.x)

**Problem**: Rate limit errors  
**Solution**: Reduce the `--rate` parameter or add delays between batches

**Problem**: Empty results  
**Solution**: Check internet connection and verify IP-API service status

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing issues for solutions
- Submit pull requests for improvements

## Changelog

### v0.1.0 (Initial Release)
- IP geolocation lookup
- ISP/organization detection
- ASN information retrieval
- RDAP/WHOIS integration
- CSV export functionality
- Rate limiting support
- CLI interface

---

**Made with ❤️ for network analysis and security research**
