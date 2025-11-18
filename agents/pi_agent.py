"""
Raspberry Pi Agent
Handles SSH connections and operations on Raspberry Pi devices.
"""

import subprocess
from typing import Dict, Any, Optional
import paramiko
import socket


class RaspberryPiAgent:
    """Agent for managing Raspberry Pi via SSH."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Raspberry Pi agent with configuration.
        
        Args:
            config: Configuration dict with host, username, password/key_path
        """
        self.host = config.get('host', 'raspberrypi.local')
        self.port = config.get('port', 22)
        self.username = config.get('username', 'pi')
        self.password = config.get('password')
        self.key_path = config.get('key_path')
        self.ssh_client: Optional[paramiko.SSHClient] = None
        
    def connect(self) -> bool:
        """
        Establish SSH connection to Raspberry Pi.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.key_path:
                self.ssh_client.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    key_filename=self.key_path,
                    timeout=10
                )
            elif self.password:
                self.ssh_client.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=10
                )
            else:
                # Try default key locations
                self.ssh_client.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    timeout=10
                )
            
            return True
        except (paramiko.SSHException, socket.error) as e:
            return False
    
    def disconnect(self):
        """Close SSH connection."""
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
    
    def execute_command(self, command: str) -> Dict[str, Any]:
        """
        Execute a command on the Raspberry Pi.
        
        Args:
            command: Shell command to execute
            
        Returns:
            Dict with stdout, stderr, and exit_code
        """
        if not self.ssh_client:
            if not self.connect():
                return {
                    "status": "error",
                    "message": f"Could not connect to Raspberry Pi at {self.host}"
                }
        
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            exit_code = stdout.channel.recv_exit_status()
            
            return {
                "status": "success" if exit_code == 0 else "error",
                "stdout": stdout.read().decode('utf-8'),
                "stderr": stderr.read().decode('utf-8'),
                "exit_code": exit_code
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def install_library(self, library: str, package_manager: str = "auto") -> Dict[str, Any]:
        """
        Install a library on the Raspberry Pi.
        
        Args:
            library: Name of the library to install
            package_manager: Package manager to use (pip, apt, npm, auto)
            
        Returns:
            Dict with installation result
        """
        if package_manager == "auto":
            # Try to detect the right package manager
            if library.startswith("python-") or library in ["numpy", "scipy", "pandas", "matplotlib"]:
                package_manager = "pip"
            else:
                package_manager = "apt"
        
        if package_manager == "pip":
            command = f"pip3 install {library}"
        elif package_manager == "apt":
            command = f"sudo apt-get update && sudo apt-get install -y {library}"
        elif package_manager == "npm":
            command = f"npm install -g {library}"
        else:
            return {"status": "error", "message": f"Unknown package manager: {package_manager}"}
        
        result = self.execute_command(command)
        result["library"] = library
        result["package_manager"] = package_manager
        return result
    
    def diagnose_system(self) -> Dict[str, Any]:
        """
        Run diagnostic commands on the Raspberry Pi.
        
        Returns:
            Dict with system information
        """
        diagnostics = {}
        
        # System info
        commands = {
            "os_info": "cat /etc/os-release | grep PRETTY_NAME",
            "kernel": "uname -r",
            "cpu": "lscpu | grep 'Model name'",
            "memory": "free -h",
            "disk": "df -h /",
            "temperature": "vcgencmd measure_temp",
            "uptime": "uptime",
            "python_version": "python3 --version",
            "pip_packages": "pip3 list"
        }
        
        for key, command in commands.items():
            result = self.execute_command(command)
            if result["status"] == "success":
                diagnostics[key] = result["stdout"].strip()
            else:
                diagnostics[key] = "N/A"
        
        return {
            "status": "success",
            "diagnostics": diagnostics
        }
    
    def upload_file(self, local_path: str, remote_path: str) -> Dict[str, Any]:
        """
        Upload a file to the Raspberry Pi.
        
        Args:
            local_path: Local file path
            remote_path: Remote destination path
            
        Returns:
            Dict with upload result
        """
        if not self.ssh_client:
            if not self.connect():
                return {
                    "status": "error",
                    "message": f"Could not connect to Raspberry Pi at {self.host}"
                }
        
        try:
            sftp = self.ssh_client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            
            return {
                "status": "success",
                "message": f"Uploaded {local_path} to {remote_path}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def execute(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an action on the Raspberry Pi.
        
        Args:
            action: Action to perform
            parameters: Parameters for the action
            
        Returns:
            Dict with result
        """
        try:
            if action == "install_library":
                library = parameters.get("library", "")
                if not library:
                    return {"status": "error", "message": "Library name required"}
                package_manager = parameters.get("package_manager", "auto")
                return self.install_library(library, package_manager)
            
            elif action == "diagnose":
                return self.diagnose_system()
            
            elif action == "upload_program":
                local_path = parameters.get("local_path", "")
                remote_path = parameters.get("remote_path", "")
                if not local_path or not remote_path:
                    return {"status": "error", "message": "Both local_path and remote_path required"}
                return self.upload_file(local_path, remote_path)
            
            elif action == "execute_command":
                command = parameters.get("command", "")
                if not command:
                    return {"status": "error", "message": "Command required"}
                return self.execute_command(command)
            
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
                
        finally:
            self.disconnect()
