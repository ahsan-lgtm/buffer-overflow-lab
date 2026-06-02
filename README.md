🧪 Vulnserver Buffer Fuzzer Suite

A Python-based fuzzing toolkit designed for authorized penetration testing in a controlled lab environment.
This tool targets the vulnerable Vulnserver application and helps identify buffer overflow crash points in various command handlers.

⚠️ Disclaimer

This project is strictly for:

Educational purposes
Authorized security testing
Lab environments (e.g., Vulnserver, vulnerable VMs)

Do NOT use this tool against systems you do not own or have explicit permission to test.


📌 Features
Automated buffer fuzzing against multiple Vulnserver commands
Crash detection via socket behavior (reset, timeout, disconnect)
Fine-grained fuzzing around crash points
Supports key vulnerable commands:
TRUN .
GMON /.../
STATS
RTIME
KSTET
GTER
HTER
LTER
and others
Massive payload bombardment mode for stress testing

🛠️ Requirements
Python 3.x
Network access to target system (Vulnserver VM recommended)

No external libraries required (uses built-in socket, time, sys).

🚀 Usage
1. Clone the repository
https://github.com/ahsan-lgtm/buffer-overflow-fuzzer-lab.git

cd buffer-overflow-fuzzer-lab

3. Run the fuzzer
python3 fuzzer.py

⚙️ Configuration

Edit the script to set your target:

TARGET = "192.168.18.108"
PORT = 9999

🔍 How It Works

The fuzzer:

Connects to the target service via TCP

Sends structured payloads:

COMMAND + "A" * buffer_size
Observes response behavior:
Normal response → service alive
Timeout/reset → possible crash
Performs:
Range-based fuzzing
Fine-grained stepping near crash points
Multi-command testing




