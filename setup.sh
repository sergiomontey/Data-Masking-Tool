#!/bin/bash

# Data Masking Tool - Setup Script
# This script sets up the environment and installs dependencies

echo "========================================"
echo "Data Masking Tool - Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.8+
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "ERROR: Python 3.8 or higher is required"
    exit 1
fi

echo "✓ Python version check passed"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt --break-system-packages

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "ERROR: Failed to install dependencies"
    echo "Try running: pip3 install pandas openpyxl Faker cryptography"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  python3 data_masking_tool.py"
echo ""
echo "To run the demo:"
echo "  python3 test_demo.py"
echo ""
echo "For help, see README.md or QUICK_START.md"
echo ""
