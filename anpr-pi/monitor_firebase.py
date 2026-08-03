"""
Real-time Firebase monitor to debug barrier issues
Shows what's actually in the database and monitors changes
"""

import time
import requests
from datetime import datetime


BASE_URL = "https://boom-barrier-24f9b-default-rtdb.asia-southeast1.firebasedatabase.app"


def get_entire_db():
    """Get the entire Firebase database to see the structure"""
    try:
        url = f"{BASE_URL}/.json"
        resp = requests.get(url, timeout=3)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def get_barrier_data():
    """Get just the barrier node"""
    try:
        url = f"{BASE_URL}/barrier.json"
        resp = requests.get(url, timeout=3)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def monitor_realtime(duration=30):
    """Monitor Firebase in real-time for changes"""
    print("=" * 70)
    print("  FIREBASE REAL-TIME MONITOR")
    print("=" * 70)
    print(f"\nMonitoring for {duration} seconds... Press Ctrl+C to stop\n")
    
    # Show full database structure first
    print("📊 FULL DATABASE STRUCTURE:")
    print("-" * 70)
    full_db = get_entire_db()
    import json
    print(json.dumps(full_db, indent=2))
    print("-" * 70)
    
    print("\n🔍 MONITORING /barrier NODE FOR CHANGES:\n")
    
    previous_state = None
    start_time = time.time()
    
    try:
        while (time.time() - start_time) < duration:
            current_state = get_barrier_data()
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            if current_state != previous_state:
                print(f"\n⚡ [{timestamp}] CHANGE DETECTED:")
                print(f"   Command: {current_state.get('command', 'N/A')}")
                print(f"   State:   {current_state.get('state', 'N/A')}")
                print(f"   Raw:     {current_state}")
                previous_state = current_state
            else:
                # Show heartbeat every 2 seconds
                if int(time.time() - start_time) % 2 == 0:
                    print(f"[{timestamp}] No changes... (Command: {current_state.get('command', 'N/A')}, State: {current_state.get('state', 'N/A')})", end="\r")
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Monitoring stopped by user")
    
    print("\n\n" + "=" * 70)
    print("  FINAL STATE CHECK")
    print("=" * 70)
    final_state = get_barrier_data()
    print(f"Command: {final_state.get('command', 'N/A')}")
    print(f"State:   {final_state.get('state', 'N/A')}")
    print(f"Raw:     {final_state}")
    print()


def test_write_and_monitor():
    """Write a test value and see if hardware responds"""
    print("=" * 70)
    print("  WRITE TEST - Checking if hardware responds")
    print("=" * 70)
    
    print("\n📝 Writing OPEN command to Firebase...")
    try:
        # Write OPEN
        requests.put(f"{BASE_URL}/barrier/command.json", json="OPEN", timeout=3)
        requests.put(f"{BASE_URL}/barrier/state.json", json="OPEN", timeout=3)
        print("✅ Written: command=OPEN, state=OPEN")
    except Exception as e:
        print(f"❌ Write failed: {e}")
        return
    
    print("\n🔍 Monitoring for hardware response (10 seconds)...")
    print("   If hardware reads this, you should see the barrier state change\n")
    
    for i in range(10):
        state = get_barrier_data()
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] command={state.get('command', 'N/A'):10s} | state={state.get('state', 'N/A'):10s}", end="")
        
        # Check if state changed (hardware responding)
        if state.get('state') in ['OPENING', 'OPENED', 'OPEN']:
            print(" ✅ HARDWARE RESPONDED!")
        else:
            print()
        
        time.sleep(1)
    
    print("\n📝 Writing CLOSE command to Firebase...")
    try:
        requests.put(f"{BASE_URL}/barrier/command.json", json="CLOSE", timeout=3)
        requests.put(f"{BASE_URL}/barrier/state.json", json="CLOSED", timeout=3)
        print("✅ Written: command=CLOSE, state=CLOSED")
    except Exception as e:
        print(f"❌ Write failed: {e}")
        return
    
    print("\n🔍 Monitoring for hardware response (5 seconds)...\n")
    for i in range(5):
        state = get_barrier_data()
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] command={state.get('command', 'N/A'):10s} | state={state.get('state', 'N/A'):10s}")
        time.sleep(1)


if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 70)
    print("  FIREBASE BARRIER DIAGNOSTIC TOOL")
    print("=" * 70)
    print("\nThis tool will help diagnose why the physical barrier isn't opening\n")
    print("Options:")
    print("  1. Monitor real-time changes (30 seconds)")
    print("  2. Test write and check hardware response")
    print("  3. Show current database state")
    print("  4. All of the above")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        monitor_realtime(30)
    elif choice == "2":
        test_write_and_monitor()
    elif choice == "3":
        print("\n📊 CURRENT DATABASE STATE:")
        print("-" * 70)
        import json
        print(json.dumps(get_entire_db(), indent=2))
        print("-" * 70)
    elif choice == "4":
        print("\n📊 CURRENT DATABASE STATE:")
        print("-" * 70)
        import json
        print(json.dumps(get_entire_db(), indent=2))
        print("-" * 70)
        input("\nPress Enter to continue to write test...")
        test_write_and_monitor()
        input("\nPress Enter to continue to real-time monitor...")
        monitor_realtime(30)
    else:
        print("Invalid choice")
        sys.exit(1)
