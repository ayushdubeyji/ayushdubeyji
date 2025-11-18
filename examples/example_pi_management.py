"""
Example: Installing a library on Raspberry Pi
"""

from gemini_workspace import GeminiWorkspace

def main():
    # Initialize workspace
    workspace = GeminiWorkspace('config.yaml')
    
    # Example 1: Install numpy on Raspberry Pi
    print("Example 1: Installing numpy on Raspberry Pi")
    result = workspace.process_prompt("Install numpy on my raspberry pi")
    print(f"Result: {result}\n")
    
    # Example 2: Run diagnostics
    print("Example 2: Running diagnostics on Raspberry Pi")
    result = workspace.process_prompt("Diagnose my raspberry pi system")
    print(f"Result: {result}\n")
    
    # Example 3: Install apt package
    print("Example 3: Installing git via apt")
    result = workspace.process_prompt("Install git on my pi using apt")
    print(f"Result: {result}\n")

if __name__ == '__main__':
    main()
