# Gemini CLI Agentic Workspace 🤖

An intelligent agentic workspace powered by Google's Gemini AI that helps you manage IoT devices through natural language commands.

## Features ✨

### 1. Raspberry Pi Management 🥧
- **SSH into your Pi** and execute commands
- **Install libraries** (pip, apt, npm) with natural language
- **Diagnose system** health and performance
- **Upload programs** via SFTP

### 2. ESP8266/ESP32 Development 📡
- **Create sketches** from natural language descriptions
- **Built-in templates** for common tasks:
  - LED blinking
  - WiFi connection
  - OTA updates
  - Sensor reading
- **Compile sketches** using Arduino CLI
- **Upload via OTA** to your devices

## Quick Start 🚀

### For Mobile Users 📱

Want to use this from your phone? Check out the [Mobile Usage Guide](MOBILE_GUIDE.md)!

**TL;DR for mobile:**
1. Open this repo on GitHub mobile
2. Create a Codespace
3. Run `./quick-start.sh`
4. Done! 🎉

### For Desktop Users

### Prerequisites

1. **Python 3.8+**
2. **Gemini API Key** - Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Arduino CLI** (optional, for ESP compilation) - [Installation Guide](https://arduino.github.io/arduino-cli/installation/)

### Installation

#### Option 1: GitHub Codespaces (Easiest - Works on Mobile!)

1. Click "Code" → "Codespaces" → "Create codespace on main"
2. Wait for setup to complete
3. Run `./quick-start.sh`

See [MOBILE_GUIDE.md](MOBILE_GUIDE.md) for detailed instructions.

#### Option 2: Docker (Recommended for Desktop)

```bash
# Using docker-compose
docker-compose up

# Or build manually
docker build -t gemini-workspace .
docker run -it -e GEMINI_API_KEY='your-key' gemini-workspace
```

#### Option 3: Local Installation

```bash
# Clone the repository
git clone https://github.com/ayushdubeyji/ayushdubeyji.git
cd ayushdubeyji

# Install Python dependencies
pip install -r requirements.txt

# Copy and configure settings
cp config.example.yaml config.yaml
# Edit config.yaml with your settings
```

### Configuration

#### Quick Setup

```bash
# Set API key via environment variable (easiest)
export GEMINI_API_KEY='your-api-key'

# Or copy and edit config
cp config.example.yaml config.yaml
# Edit config.yaml with your settings

# Or use .env file
cp .env.example .env
# Edit .env with your credentials
```

#### Detailed Configuration

Edit `config.yaml`:

```yaml
gemini:
  api_key: "YOUR_GEMINI_API_KEY"  # Or set GEMINI_API_KEY env var
  model: gemini-pro

raspberry_pi:
  host: raspberrypi.local  # or IP address
  username: pi
  password: your_password  # or use key_path

esp_devices:
  sketch_directory: ./sketches
  ota_port: 8266
```

## Usage 💻

### Interactive Mode

```bash
python gemini_workspace.py -i
```

Then type natural language commands:

```
gemini> Install numpy on my raspberry pi
gemini> Create an ESP32 sketch to blink LED on GPIO 2
gemini> Diagnose my pi system
gemini> Upload sketch to ESP8266 at 192.168.1.100 via OTA
```

### Single Command Mode

```bash
python gemini_workspace.py "Install pandas on my raspberry pi"
python gemini_workspace.py "Create ESP8266 WiFi connection sketch"
```

## Examples 📚

### Raspberry Pi Commands

```python
# Install Python packages
"Install numpy on my raspberry pi"
"Install scipy using pip on my pi"

# Install system packages
"Install git on my pi using apt"

# System diagnostics
"Diagnose my raspberry pi"
"Check the temperature of my pi"

# Execute commands
"Run uptime on my raspberry pi"
```

### ESP8266/ESP32 Commands

```python
# Create sketches
"Create an ESP8266 sketch to blink LED on GPIO 2"
"Create an ESP32 sketch to read sensor from pin A0"
"Create ESP8266 sketch with WiFi and OTA support"

# Upload sketches
"Upload sketch at ./sketches/blink.ino to ESP8266 at 192.168.1.100"
```

## Project Structure 📁

```
.
├── gemini_workspace.py      # Main CLI entry point
├── agents/
│   ├── pi_agent.py          # Raspberry Pi management
│   └── esp_agent.py         # ESP8266/ESP32 management
├── utils/
│   └── config_manager.py    # Configuration handling
├── examples/
│   ├── example_pi_management.py
│   └── example_esp_sketches.py
├── sketches/                # Generated ESP sketches
├── config.yaml              # Your configuration
├── config.example.yaml      # Example configuration
└── requirements.txt         # Python dependencies
```

## How It Works 🔧

1. **Natural Language Processing**: Gemini AI interprets your commands
2. **Intent Recognition**: Determines which agent (Pi or ESP) should handle the request
3. **Action Execution**: The appropriate agent performs the requested operation
4. **Result Reporting**: You get feedback on what happened

## Supported Operations 🛠️

### Raspberry Pi Agent
- `install_library` - Install packages (pip, apt, npm)
- `diagnose` - System health check
- `upload_program` - Upload files via SFTP
- `execute_command` - Run any shell command

### ESP Agent
- `create_sketch` - Generate Arduino sketches from templates
- `compile_sketch` - Compile using Arduino CLI
- `upload_ota` - Upload firmware over-the-air

## Security Notes 🔒

- Store API keys in environment variables or secure config files
- Use SSH keys instead of passwords when possible
- Don't commit `config.yaml` with sensitive data
- OTA uploads should be on trusted networks

## Troubleshooting 🔍

### "Could not connect to Raspberry Pi"
- Check host/IP address in config
- Verify SSH is enabled on your Pi
- Test connection: `ssh pi@raspberrypi.local`

### "arduino-cli not found"
- Install Arduino CLI: https://arduino.github.io/arduino-cli/
- Add to PATH: `export PATH=$PATH:/path/to/arduino-cli`

### "Gemini API key not found"
- Set environment variable: `export GEMINI_API_KEY=your_key`
- Or add to config.yaml

## Contributing 🤝

Contributions welcome! Feel free to:
- Add new sketch templates
- Improve agent capabilities
- Enhance error handling
- Add tests

## Recent Improvements 🎉

This project has been enhanced with:
- ✅ **GitHub Codespaces Support** - Use from any device, including mobile!
- ✅ **Docker Containerization** - Easy deployment with Docker/docker-compose
- ✅ **Enhanced Environment Management** - .env file support for credentials
- ✅ **Mobile-Optimized Quick Start** - Interactive setup wizard
- ✅ **CI/CD Pipeline** - Automated testing and security scanning
- ✅ **Comprehensive Mobile Guide** - See [MOBILE_GUIDE.md](MOBILE_GUIDE.md)

See [IMPROVEMENTS.md](IMPROVEMENTS.md) for detailed documentation on workflow improvements.

## Documentation 📚

- [Mobile & Codespace Usage Guide](MOBILE_GUIDE.md) - How to use from your phone
- [Improvements Documentation](IMPROVEMENTS.md) - Detailed workflow improvements
- [Configuration Examples](config.example.yaml) - Configuration template
- [Code Examples](examples/) - Python usage examples

## License 📄

MIT License - feel free to use this project for your own IoT adventures!

## Author 👨‍💻

Created by [@ayushdubeyji](https://github.com/ayushdubeyji)

- 🔭 Currently working on Gen AI projects
- 🌱 Learning Gemini API and agentic systems
- 💬 Ask me about IoT, AI, and automation

---

**Made with ❤️ and Gemini AI**
