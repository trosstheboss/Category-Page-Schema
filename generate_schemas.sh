#!/bin/bash

echo "========================================"
echo "Category Page Schema Generator"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python detected:"
python3 --version
echo ""

# Check if pandas is installed
python3 -c "import pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "Running schema generator..."
echo ""

python3 schema_generator.py

if [ $? -eq 0 ]; then
    echo ""
    echo "SUCCESS: Schema files generated in output/ directory"
else
    echo ""
    echo "ERROR: Schema generation failed"
    echo "Check the error messages above"
    exit 1
fi
