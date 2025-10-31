# Setup Instructions for Survey IP Metadata Tool

## Using Conda Environment (Recommended)

### Step 1: Create Conda Environment

```bash
# Create the conda environment from the environment.yml file
conda env create -f environment.yml
```

### Step 2: Activate the Environment

```bash
conda activate proxycheck
```

### Step 3: Verify Installation

```bash
# Check Python version
python --version

# Verify packages are installed
pip list
```

### Step 4: Run the Tool

```bash
# Process sample IPs
python -m survey_ip.cli --input data/sample_ips.txt --output results.csv

# Or with custom options
python -m survey_ip.cli --input data/sample_ips.txt --output my_results.csv --rate 1.0
```

### Step 5: Deactivate When Done

```bash
conda deactivate
```

## Alternative: Using pip with virtual environment

If you prefer not to use conda:

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the tool
python -m survey_ip.cli --input data/sample_ips.txt --output results.csv
```

## Quick Start Commands

```bash
# One-line setup with conda
conda env create -f environment.yml && conda activate proxycheck

# Run with sample data
python -m survey_ip.cli --input data/sample_ips.txt --output results.csv

# View results
cat results.csv
# OR
open results.csv  # Opens in default CSV viewer
```

## Testing the Installation

```bash
# Activate environment
conda activate proxycheck

# Run tests
pytest tests/

# Or test with sample data
python -m survey_ip.cli --input data/sample_ips.txt --output test_output.csv
cat test_output.csv
```

## Troubleshooting

### Conda not found
- Install Miniconda or Anaconda from: https://docs.conda.io/en/latest/miniconda.html

### Package installation fails
```bash
# Update conda
conda update conda

# Recreate environment
conda env remove -n proxycheck
conda env create -f environment.yml
```

### Permission errors
```bash
# Use user installation
pip install --user -r requirements.txt
```

## Environment Management

```bash
# List all conda environments
conda env list

# Remove environment
conda env remove -n proxycheck

# Update environment
conda env update -f environment.yml --prune

# Export current environment
conda env export > environment_backup.yml
