# Quick Start Guide - Survey IP Metadata

## 🚀 Fastest Way to Run

```bash
# 1. Make the script executable (first time only)
chmod +x run_local.sh

# 2. Run it!
./run_local.sh
```

That's it! The script will handle everything automatically.

---

## 📋 Manual Setup (Step by Step)

### With Conda (Recommended)

```bash
# Step 1: Create environment
conda env create -f environment.yml

# Step 2: Activate environment
conda activate proxycheck

# Step 3: Run the tool
python -m survey_ip.cli --input data/sample_ips.txt --output results.csv

# Step 4: View results
cat results.csv
```

### With pip/venv

```bash
# Step 1: Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR: venv\Scripts\activate  # Windows

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run the tool
python -m survey_ip.cli --input data/sample_ips.txt --output results.csv

# Step 4: View results
cat results.csv
```

---

## 💡 Common Usage Examples

### Example 1: Basic Usage
```bash
conda activate proxycheck
python -m survey_ip.cli --input data/sample_ips.txt --output results.csv
```

### Example 2: Fast Mode (Skip RDAP)
```bash
python -m survey_ip.cli --input my_ips.txt --no-rdap --rate 2.0 --output fast_results.csv
```

### Example 3: Custom Rate Limiting
```bash
# Slower (more respectful to API)
python -m survey_ip.cli --input ips.txt --rate 0.5

# Faster (within limits)
python -m survey_ip.cli --input ips.txt --rate 2.0
```

### Example 4: Process Your Own IPs
```bash
# Create your IP list
echo "8.8.8.8" > my_ips.txt
echo "1.1.1.1" >> my_ips.txt
echo "208.67.222.222" >> my_ips.txt

# Process them
python -m survey_ip.cli --input my_ips.txt --output my_results.csv

# View results
cat my_results.csv
```

---

## 📊 Understanding the Output

The tool creates a CSV file with these columns:

```csv
ip,country,region,city,zip,lat,lon,isp,org,as,reverse,netname,country_reg,cidr
8.8.8.8,United States,California,Mountain View,,37.4056,-122.0775,Google LLC,Google LLC,AS15169 Google LLC,dns.google,...
```

### Key Fields:
- **ip**: The IP address queried
- **country/region/city**: Geographic location
- **lat/lon**: GPS coordinates
- **isp**: Internet Service Provider
- **org**: Organization that owns the IP
- **as**: Autonomous System Number
- **netname**: Network name from registry

---

## 🛠️ Troubleshooting

### Issue: "conda: command not found"
**Solution**: Install Miniconda
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### Issue: "IPDefinedError: x.x.x.x is not a public IP"
**Solution**: Only use public IP addresses
- ❌ Don't use: 10.x.x.x, 192.168.x.x, 172.16-31.x.x, 127.x.x.x
- ✅ Use public IPs like: 8.8.8.8, 1.1.1.1, etc.

### Issue: Rate limit errors
**Solution**: Slow down the requests
```bash
python -m survey_ip.cli --input ips.txt --rate 0.5
```

### Issue: No results appearing
**Solution**: Check internet connection and API status
```bash
# Test with a single known IP
echo "8.8.8.8" > test.txt
python -m survey_ip.cli --input test.txt --output test_out.csv
cat test_out.csv
```

---

## 📁 Input File Format

Create a text file with one IP per line:

```
# Google DNS
8.8.8.8
8.8.4.4

# Cloudflare DNS
1.1.1.1
1.0.0.1

# OpenDNS
208.67.222.222
208.67.220.220
```

Lines starting with `#` are ignored (comments).

---

## 🎯 Pro Tips

1. **Start Small**: Test with a few IPs first
   ```bash
   head -5 large_ip_list.txt > test_sample.txt
   python -m survey_ip.cli --input test_sample.txt
   ```

2. **Use Rate Limiting**: Respect API limits
   ```bash
   # Safe default (1 req/sec)
   python -m survey_ip.cli --input ips.txt --rate 1.0
   ```

3. **Skip RDAP for Speed**: If you don't need registry data
   ```bash
   python -m survey_ip.cli --input ips.txt --no-rdap
   ```

4. **Process in Batches**: For large lists
   ```bash
   split -l 100 huge_list.txt batch_
   for file in batch_*; do
     python -m survey_ip.cli --input "$file" --output "results_$file.csv"
     sleep 60  # Wait between batches
   done
   ```

5. **Keep Environment Active**: Avoid reactivation
   ```bash
   # Activate once
   conda activate proxycheck
   
   # Run multiple times
   python -m survey_ip.cli --input ips1.txt
   python -m survey_ip.cli --input ips2.txt
   python -m survey_ip.cli --input ips3.txt
   
   # Deactivate when done
   conda deactivate
   ```

---

## 🔄 Workflow Example

Complete workflow from start to finish:

```bash
# 1. Setup (one time)
conda env create -f environment.yml

# 2. Activate
conda activate proxycheck

# 3. Prepare your IP list
cat > my_survey_ips.txt << EOF
8.8.8.8
1.1.1.1
208.67.222.222
EOF

# 4. Run the analysis
python -m survey_ip.cli \
  --input my_survey_ips.txt \
  --output survey_results.csv \
  --rate 1.0

# 5. View results
cat survey_results.csv

# 6. Open in spreadsheet (optional)
# Linux: xdg-open survey_results.csv
# Mac: open survey_results.csv
# Windows: start survey_results.csv

# 7. Deactivate when done
conda deactivate
```

---

## 📞 Need Help?

- Check `SETUP.md` for detailed setup instructions
- Read `README.md` for comprehensive documentation
- Look at `data/sample_ips.txt` for input examples
- Run `python -m survey_ip.cli --help` for command options

---

**Happy IP hunting! 🎯**
