#!/bin/bash

# Survey IP Metadata - Local Run Script
# This script sets up the conda environment and runs the tool

echo "=========================================="
echo "Survey IP Metadata - Local Setup & Run"
echo "=========================================="
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Miniconda or Anaconda."
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✓ Conda found: $(conda --version)"
echo ""

# Check if environment exists
if conda env list | grep -q "^proxycheck "; then
    echo "✓ Environment 'proxycheck' already exists"
else
    echo "📦 Creating conda environment 'proxycheck'..."
    conda env create -f environment.yml
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create environment"
        exit 1
    fi
    echo "✓ Environment created successfully"
fi

echo ""
echo "🚀 Activating environment and running tool..."
echo ""

# Run the tool
conda run -n proxycheck python -m survey_ip.cli --input data/sample_ips.txt --output results.csv

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS! Results saved to results.csv"
    echo "=========================================="
    echo ""
    echo "To view results:"
    echo "  cat results.csv"
    echo "  # OR"
    echo "  open results.csv"
    echo ""
    echo "To run again with different options:"
    echo "  conda activate proxycheck"
    echo "  python -m survey_ip.cli --input YOUR_IPS.txt --output output.csv"
    echo "  conda deactivate"
else
    echo ""
    echo "❌ Error running the tool. Check the error messages above."
    exit 1
fi
