"""
Simple gate control utility
Usage: python tools/control_gate.py [open|close|status]
"""

import sys
from src.firebase_gate import open_gate, close_gate, get_gate_status


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/control_gate.py [open|close|status]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "open":
        if open_gate():
            print("✅ Gate opened successfully")
        else:
            print("❌ Failed to open gate")
            sys.exit(1)
    
    elif command == "close":
        if close_gate():
            print("✅ Gate closed successfully")
        else:
            print("❌ Failed to close gate")
            sys.exit(1)
    
    elif command == "status":
        status = get_gate_status()
        print(f"📊 Gate Status:")
        print(f"   State:   {status.get('state', 'N/A')}")
        print(f"   Command: {status.get('command', 'N/A')}")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Usage: python tools/control_gate.py [open|close|status]")
        sys.exit(1)


if __name__ == "__main__":
    main()
