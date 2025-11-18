#!/bin/bash
# Quick start script for mobile/Codespace usage
# This provides a simplified setup flow optimized for quick mobile access

set -e

echo "📱 Gemini CLI Workspace - Mobile Quick Start"
echo "============================================="
echo ""

# Check if running in Codespace
if [ -n "$CODESPACE_NAME" ]; then
    echo "✓ Running in GitHub Codespace: $CODESPACE_NAME"
    IS_CODESPACE=true
else
    echo "ℹ️  Running locally"
    IS_CODESPACE=false
fi

# Function to check if API key is set
check_api_key() {
    if [ -n "$GEMINI_API_KEY" ]; then
        echo "✓ GEMINI_API_KEY is set"
        return 0
    else
        return 1
    fi
}

# Check for dependencies
echo ""
echo "Checking dependencies..."
if command -v python3 &> /dev/null; then
    echo "✓ Python 3: $(python3 --version)"
else
    echo "✗ Python 3 not found!"
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import google.generativeai" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install --quiet -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Create config if needed
if [ ! -f config.yaml ]; then
    echo ""
    echo "Creating config.yaml from template..."
    cp config.example.yaml config.yaml
    echo "✓ config.yaml created"
fi

# Create sketches directory
mkdir -p sketches

echo ""
echo "============================================="
echo "🔑 API Key Setup"
echo "============================================="

if ! check_api_key; then
    echo ""
    echo "⚠️  GEMINI_API_KEY not found!"
    echo ""
    echo "To use this tool, you need a Gemini API key."
    echo "Get one from: https://makersuite.google.com/app/apikey"
    echo ""
    
    if [ "$IS_CODESPACE" = true ]; then
        echo "To set it in Codespace, run:"
        echo "  export GEMINI_API_KEY='your-key-here'"
        echo ""
        echo "Or add it as a Codespace secret for automatic setup:"
        echo "  Repository Settings → Secrets → Codespaces → New secret"
    else
        echo "To set it temporarily, run:"
        echo "  export GEMINI_API_KEY='your-key-here'"
        echo ""
        echo "Or create a .env file:"
        echo "  echo 'GEMINI_API_KEY=your-key-here' > .env"
    fi
    echo ""
    read -p "Enter your Gemini API key now (or press Enter to skip): " api_key
    
    if [ -n "$api_key" ]; then
        export GEMINI_API_KEY="$api_key"
        echo "✓ API key set for this session"
        
        # Optionally save to .env
        if [ "$IS_CODESPACE" = false ]; then
            read -p "Save to .env file for future sessions? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                echo "GEMINI_API_KEY=$api_key" > .env
                echo "✓ Saved to .env file"
            fi
        fi
    fi
fi

echo ""
echo "============================================="
echo "📋 Device Configuration (Optional)"
echo "============================================="
echo ""
echo "To manage Raspberry Pi or ESP devices, edit config.yaml"
echo "Current configuration:"
echo ""
python3 -c "
import yaml
try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print('Raspberry Pi:')
    rpi = config.get('raspberry_pi', {})
    print(f'  Host: {rpi.get(\"host\", \"Not set\")}')
    print(f'  Username: {rpi.get(\"username\", \"Not set\")}')
    
    print()
    print('ESP Devices:')
    esp = config.get('esp_devices', {})
    print(f'  Sketch Directory: {esp.get(\"sketch_directory\", \"Not set\")}')
    print(f'  Default Device: {esp.get(\"default_device\", \"Not set\")}')
except Exception as e:
    print(f'Error reading config: {e}')
"

echo ""
echo "============================================="
echo "🚀 Ready to Use!"
echo "============================================="
echo ""
echo "Choose an option:"
echo "  1. Interactive mode (recommended for mobile)"
echo "  2. Single command mode"
echo "  3. View examples"
echo "  4. Exit"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo ""
        echo "Starting interactive mode..."
        echo "Type 'exit' or 'quit' to exit, 'help' for examples"
        echo ""
        python3 gemini_workspace.py -i
        ;;
    2)
        echo ""
        read -p "Enter your command: " cmd
        python3 gemini_workspace.py "$cmd"
        ;;
    3)
        echo ""
        echo "Example commands:"
        echo "  - Install numpy on my raspberry pi"
        echo "  - Diagnose my raspberry pi"
        echo "  - Create an ESP8266 sketch to blink LED on GPIO 2"
        echo "  - Create ESP32 WiFi connection sketch"
        echo "  - Upload sketch to ESP8266 at 192.168.1.100 via OTA"
        echo ""
        read -p "Press Enter to continue..."
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
