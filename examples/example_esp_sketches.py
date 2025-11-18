"""
Example: Creating and uploading ESP sketches
"""

from gemini_workspace import GeminiWorkspace

def main():
    # Initialize workspace
    workspace = GeminiWorkspace('config.yaml')
    
    # Example 1: Create a blink sketch for ESP8266
    print("Example 1: Creating blink sketch for ESP8266")
    result = workspace.process_prompt("Create an ESP8266 sketch to blink LED on GPIO 2")
    print(f"Result: {result}\n")
    
    # Example 2: Create a WiFi connection sketch
    print("Example 2: Creating WiFi connection sketch")
    result = workspace.process_prompt("Create an ESP32 sketch to connect to WiFi")
    print(f"Result: {result}\n")
    
    # Example 3: Create OTA-enabled sketch
    print("Example 3: Creating OTA-enabled sketch")
    result = workspace.process_prompt("Create an ESP8266 sketch with OTA update support")
    print(f"Result: {result}\n")
    
    # Example 4: Upload sketch via OTA
    # Note: This assumes you have a device with OTA already running at the IP
    print("Example 4: Uploading sketch via OTA")
    result = workspace.process_prompt("Upload sketch to ESP8266 at 192.168.1.100 via OTA")
    print(f"Result: {result}\n")

if __name__ == '__main__':
    main()
