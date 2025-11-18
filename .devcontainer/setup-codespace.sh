#!/bin/bash
# Automated setup script for GitHub Codespaces
# This script runs automatically when the codespace is created

set -e

echo "🚀 Setting up Gemini CLI Agentic Workspace in Codespace..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --quiet -r requirements.txt

# Create config file from example if it doesn't exist
if [ ! -f config.yaml ]; then
    cp config.example.yaml config.yaml
    echo "✓ Created config.yaml from template"
fi

# Create sketches directory
mkdir -p sketches
echo "✓ Created sketches directory"

# Check for Arduino CLI (optional)
if command -v arduino-cli &> /dev/null; then
    echo "✓ Arduino CLI found: $(arduino-cli version)"
else
    echo "⚠️  Arduino CLI not found (optional for ESP compilation)"
    echo "   Install with: curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh"
fi

# Make scripts executable
chmod +x gemini_workspace.py setup.sh 2>/dev/null || true

echo ""
echo "✅ Codespace setup complete!"
echo ""
echo "📱 Mobile-friendly usage:"
echo "   1. Set your GEMINI_API_KEY: export GEMINI_API_KEY='your-key-here'"
echo "   2. Edit config.yaml with your device settings"
echo "   3. Run interactive mode: python gemini_workspace.py -i"
echo ""
echo "🔑 Important: Set your Gemini API key before using:"
echo "   export GEMINI_API_KEY='your-api-key'"
echo "   Or edit it in config.yaml"
echo ""
echo "📚 Quick commands:"
echo "   python gemini_workspace.py -i                    # Interactive mode"
echo "   python gemini_workspace.py 'your command here'   # Single command"
echo ""
