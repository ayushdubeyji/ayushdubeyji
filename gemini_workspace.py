#!/usr/bin/env python3
"""
Gemini CLI Agentic Workspace
Main entry point for the agentic system that integrates with Gemini CLI
to manage Raspberry Pi and ESP8266/ESP32 devices.
"""

import os
import sys
import argparse
from typing import Dict, Any

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not required, just nice to have

try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai package not installed.")
    print("Install with: pip install google-generativeai")
    sys.exit(1)

from agents.pi_agent import RaspberryPiAgent
from agents.esp_agent import ESPAgent
from utils.config_manager import ConfigManager


class GeminiWorkspace:
    """Main workspace class for managing agentic operations."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the workspace with configuration."""
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()
        
        # Initialize Gemini API
        api_key = self.config.get('gemini', {}).get('api_key') or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY or add to config.yaml")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            self.config.get('gemini', {}).get('model', 'gemini-pro')
        )
        
        # Initialize agents
        self.pi_agent = RaspberryPiAgent(self.config.get('raspberry_pi', {}))
        self.esp_agent = ESPAgent(self.config.get('esp_devices', {}))
        
    def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Process a natural language prompt and route to appropriate agent.
        
        Args:
            prompt: User's natural language command
            
        Returns:
            Dict containing the result of the operation
        """
        # Use Gemini to understand the intent
        system_prompt = """You are an AI assistant that helps manage IoT devices.
Analyze the user's request and determine:
1. Which agent should handle it: 'raspberry_pi' or 'esp_device'
2. What action should be taken
3. Extract relevant parameters

Respond in JSON format with:
{
    "agent": "raspberry_pi" or "esp_device",
    "action": "specific action like install_library, diagnose, upload_program, create_sketch, upload_ota",
    "parameters": {relevant parameters}
}

Example prompts:
- "Install numpy on my raspberry pi" -> {"agent": "raspberry_pi", "action": "install_library", "parameters": {"library": "numpy"}}
- "Create an ESP32 sketch to blink LED on GPIO 2" -> {"agent": "esp_device", "action": "create_sketch", "parameters": {"device": "esp32", "task": "blink led", "gpio": 2}}
"""
        
        try:
            response = self.model.generate_content(f"{system_prompt}\n\nUser request: {prompt}")
            intent = self._parse_intent(response.text)
            
            # Route to appropriate agent
            if intent['agent'] == 'raspberry_pi':
                return self.pi_agent.execute(intent['action'], intent['parameters'])
            elif intent['agent'] == 'esp_device':
                return self.esp_agent.execute(intent['action'], intent['parameters'])
            else:
                return {"status": "error", "message": "Unknown agent"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _parse_intent(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini's response to extract intent."""
        import json
        import re
        
        # Try to extract JSON from the response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            return json.loads(json_match.group())
        
        # Fallback parsing
        return {
            "agent": "raspberry_pi" if "pi" in response_text.lower() else "esp_device",
            "action": "diagnose",
            "parameters": {}
        }


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Gemini CLI Agentic Workspace for IoT Device Management'
    )
    parser.add_argument(
        'prompt',
        nargs='*',
        help='Natural language command to execute'
    )
    parser.add_argument(
        '-c', '--config',
        default='config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Start interactive mode'
    )
    
    args = parser.parse_args()
    
    # Initialize workspace
    try:
        workspace = GeminiWorkspace(args.config)
    except Exception as e:
        print(f"Error initializing workspace: {e}")
        sys.exit(1)
    
    if args.interactive:
        # Interactive mode
        print("Gemini Workspace Interactive Mode")
        print("Type 'exit' or 'quit' to exit")
        print("Type 'help' for example commands\n")
        
        while True:
            try:
                prompt = input("gemini> ").strip()
                if prompt.lower() in ['exit', 'quit']:
                    break
                if not prompt:
                    continue
                if prompt.lower() == 'help':
                    print("\n📚 Example Commands:")
                    print("\nRaspberry Pi:")
                    print("  - Install numpy on my raspberry pi")
                    print("  - Diagnose my raspberry pi")
                    print("  - Run uptime on my raspberry pi")
                    print("\nESP8266/ESP32:")
                    print("  - Create an ESP8266 sketch to blink LED on GPIO 2")
                    print("  - Create ESP32 WiFi connection sketch")
                    print("  - Upload sketch to ESP8266 at 192.168.1.100 via OTA")
                    print("\nType 'exit' or 'quit' to exit\n")
                    continue
                    
                result = workspace.process_prompt(prompt)
                print(f"\nResult: {result}\n")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
    else:
        # Single command mode
        if not args.prompt:
            parser.print_help()
            sys.exit(1)
            
        prompt = ' '.join(args.prompt)
        result = workspace.process_prompt(prompt)
        print(f"Result: {result}")


if __name__ == '__main__':
    main()
