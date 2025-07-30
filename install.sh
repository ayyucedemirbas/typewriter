#!/bin/bash

# Typewriter Sounds - Installation Script
echo "🎵 Installing Typewriter Sounds..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip3"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "🚀 To run Typewriter Sounds:"
    echo "   python3 typewriter.py"
    echo ""
    echo "⚠️  Don't forget to grant Accessibility permissions:"
    echo "   System Preferences → Security & Privacy → Privacy → Accessibility"
    echo "   Add Terminal (or your Python IDE) to the list"
else
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi
