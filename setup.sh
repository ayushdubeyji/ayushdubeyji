#!/bin/bash
# Setup script for Gemini CLI Agentic Workspace

echo "🚀 Setting up Gemini CLI Agentic Workspace..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment (optional but recommended)
read -p "Create a virtual environment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create config file
if [ ! -f config.yaml ]; then
    cp config.example.yaml config.yaml
    echo "✓ Created config.yaml from template"
    echo "⚠️  Please edit config.yaml with your settings:"
    echo "   - Add your Gemini API key"
    echo "   - Configure Raspberry Pi connection details"
else
    echo "✓ config.yaml already exists"
fi

# Create sketches directory
mkdir -p sketches
echo "✓ Created sketches directory"

# Check for Arduino CLI (optional)
if command -v arduino-cli &> /dev/null
then
    echo "✓ Arduino CLI found: $(arduino-cli version)"
else
    echo "⚠️  Arduino CLI not found (optional for ESP compilation)"
    echo "   Install from: https://arduino.github.io/arduino-cli/"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.yaml with your API keys and device settings"
echo "2. Set GEMINI_API_KEY environment variable (optional)"
echo "3. Run: python gemini_workspace.py -i"
echo ""
echo "For help: python gemini_workspace.py --help"
