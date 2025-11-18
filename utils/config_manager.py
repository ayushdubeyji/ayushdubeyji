"""
Configuration Manager
Handles loading and managing configuration for the workspace.
"""

import os
import yaml
from typing import Dict, Any


class ConfigManager:
    """Manage configuration files for the workspace."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.
        
        Returns:
            Configuration dictionary
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f) or {}
                return config
            except Exception as e:
                print(f"Warning: Could not load config from {self.config_path}: {e}")
                return self._default_config()
        else:
            # Create default config
            config = self._default_config()
            self.save_config(config)
            return config
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        Save configuration to YAML file.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            True if successful
        """
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _default_config(self) -> Dict[str, Any]:
        """
        Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "gemini": {
                "api_key": None,  # Set via GEMINI_API_KEY env var or edit this
                "model": "gemini-pro"
            },
            "raspberry_pi": {
                "host": "raspberrypi.local",
                "port": 22,
                "username": "pi",
                "password": None,  # Or use key_path
                "key_path": None  # Path to SSH private key
            },
            "esp_devices": {
                "sketch_directory": "./sketches",
                "default_device": "esp8266",
                "ota_port": 8266
            }
        }
