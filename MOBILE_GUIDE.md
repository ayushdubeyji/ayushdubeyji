# Mobile & Codespace Usage Guide 📱

This guide explains how to use the Gemini CLI Workspace from your mobile device via GitHub Codespaces.

## Why Use Codespaces for Mobile?

GitHub Codespaces provides a full development environment accessible from any device with a web browser, including your phone! This means you can:

- ✅ Manage your Raspberry Pi from anywhere
- ✅ Create and upload ESP sketches on the go
- ✅ Access a full Linux terminal on your phone
- ✅ No local installation required
- ✅ All dependencies pre-configured

## Quick Start (Mobile)

### 1. Open Codespace

1. Navigate to this repository on GitHub mobile app or browser
2. Tap/click the **Code** button
3. Select **Codespaces** tab
4. Click **Create codespace on main**

Wait a few minutes for the Codespace to initialize.

### 2. Run Quick Start Script

Once the Codespace opens, you'll see a terminal. Run:

```bash
./quick-start.sh
```

This interactive script will:
- Check and install dependencies
- Help you set up your Gemini API key
- Guide you through configuration
- Start the tool in interactive mode

### 3. Set Your API Key

You need a Gemini API key to use this tool:

1. Get your key from: https://makersuite.google.com/app/apikey
2. Set it in the Codespace:
   ```bash
   export GEMINI_API_KEY='your-key-here'
   ```

**Pro tip for mobile**: Save your API key as a Codespace secret so it's automatically available:
1. Go to: Repository Settings → Secrets → Codespaces
2. Click "New secret"
3. Name: `GEMINI_API_KEY`
4. Value: Your API key
5. Click "Add secret"

Now every Codespace will have your API key automatically!

## Usage Modes

### Interactive Mode (Recommended for Mobile)

Best for mobile usage - you can type natural language commands:

```bash
python gemini_workspace.py -i
```

Then type commands like:
```
gemini> Install numpy on my raspberry pi
gemini> Create an ESP8266 sketch to blink LED
gemini> Diagnose my pi system
gemini> exit
```

### Single Command Mode

Run one command and exit:

```bash
python gemini_workspace.py "Install pandas on my raspberry pi"
```

### Quick Start Script

Most mobile-friendly option:

```bash
./quick-start.sh
```

## Configuration for Your Devices

Edit `config.yaml` to configure your devices:

```bash
# On mobile, use nano or vim
nano config.yaml
```

### Raspberry Pi Configuration

```yaml
raspberry_pi:
  host: raspberrypi.local  # or IP address like 192.168.1.100
  port: 22
  username: pi
  password: your_password  # or use key_path
  key_path: null  # Path to SSH key
```

### ESP Device Configuration

```yaml
esp_devices:
  sketch_directory: ./sketches
  default_device: esp8266
  ota_port: 8266
```

## Tips for Mobile Usage

### 1. Use Port Forwarding

If you need to access web interfaces:
- Codespace automatically forwards ports
- Check the "Ports" tab in the Codespace interface

### 2. Save Your Work

Codespaces auto-save, but you can also:
```bash
git add .
git commit -m "Update configs"
git push
```

### 3. SSH Key Management

For Raspberry Pi access, you can upload your SSH key:

```bash
# Create .ssh directory
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Create/edit your key (paste your private key content)
nano ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa

# Test connection
ssh pi@raspberrypi.local
```

### 4. Keep Codespace Alive

Free Codespaces stop after inactivity:
- Keep the browser tab open
- Or upgrade to Pro for longer sessions

### 5. Multiple Sessions

You can have multiple terminal tabs:
- Click the `+` icon in the terminal panel
- Run different commands in each

## Docker Alternative

If you prefer Docker:

```bash
# Build the container
docker build -t gemini-workspace .

# Run interactively
docker run -it \
  -e GEMINI_API_KEY='your-key' \
  -v $(pwd)/config.yaml:/app/config.yaml \
  -v $(pwd)/sketches:/app/sketches \
  gemini-workspace

# Or use docker-compose
docker-compose up
```

## Example Commands

### Raspberry Pi Management

```bash
# Install packages
python gemini_workspace.py "Install numpy on my raspberry pi"
python gemini_workspace.py "Install git on my pi using apt"

# System diagnostics
python gemini_workspace.py "Diagnose my raspberry pi"
python gemini_workspace.py "Check temperature of my pi"

# Run commands
python gemini_workspace.py "Run uptime on my raspberry pi"
```

### ESP8266/ESP32 Development

```bash
# Create sketches
python gemini_workspace.py "Create ESP8266 blink sketch on GPIO 2"
python gemini_workspace.py "Create ESP32 WiFi connection sketch"
python gemini_workspace.py "Create ESP8266 OTA update sketch"

# Upload via OTA (requires device on network)
python gemini_workspace.py "Upload sketch to ESP8266 at 192.168.1.100"
```

## Troubleshooting

### "Gemini API key not found"

Set the environment variable:
```bash
export GEMINI_API_KEY='your-key-here'
```

Or edit `config.yaml`:
```yaml
gemini:
  api_key: your-key-here
```

### "Could not connect to Raspberry Pi"

1. Check your Pi is on and accessible
2. Verify the IP/hostname in `config.yaml`
3. Test connection: `ssh pi@raspberrypi.local`
4. Check firewall settings

### "arduino-cli not found"

This is optional for ESP compilation. To install:
```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
export PATH=$PATH:~/bin
```

### Codespace Won't Start

1. Check GitHub status
2. Try deleting and recreating the Codespace
3. Check your GitHub account limits

## Performance on Mobile

### Tips for Better Performance:

1. **Use Interactive Mode**: Less overhead than multiple command invocations
2. **Close Unused Tabs**: Browser memory matters on mobile
3. **Use WiFi**: Better than mobile data for large operations
4. **Landscape Mode**: More terminal real estate
5. **External Keyboard**: Bluetooth keyboard greatly improves usability

### Bandwidth Considerations:

- Initial Codespace setup: ~100-200 MB
- Typical usage: < 1 MB per command
- SSH operations: Minimal data usage
- OTA uploads: Depends on sketch size

## Security Best Practices

1. **Never commit API keys**: Use environment variables or secrets
2. **Use SSH keys**: More secure than passwords for Pi access
3. **Keep dependencies updated**: Run `pip install -r requirements.txt --upgrade`
4. **Review generated sketches**: Before uploading to devices
5. **Use private repositories**: For your configuration

## Advanced: Automation with GitHub Actions

You can automate device management using GitHub Actions. See `.github/workflows/` for examples.

Example workflow to check Pi status daily:

```yaml
name: Daily Pi Health Check
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
jobs:
  check-pi:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Check Pi
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          python gemini_workspace.py "Diagnose my raspberry pi"
```

## Getting Help

- 📖 See main [README.md](../README.md) for general documentation
- 💬 Open an issue for bugs or feature requests
- 🔧 Check [examples/](../examples/) for code samples

## Next Steps

Once you're comfortable with mobile usage:

1. Set up automatic backups of your configs
2. Create custom sketch templates
3. Automate repetitive tasks with scripts
4. Share your Codespace configuration with team members

Happy coding from your phone! 📱✨
