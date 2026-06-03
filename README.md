This repository documents a Buffer Overflow Exploitation Lab performed on a vulnerable application (VulnServer) in a controlled environment for educational purposes.

The objective of this project is to understand how memory corruption vulnerabilities can be identified and exploited to gain control over program execution flow, ultimately demonstrating how attackers may achieve remote code execution in unsafe software.

The methodology includes:

Spiking to identify vulnerable input functions
Fuzzing to detect crash points in the application
Payload analysis to determine crash behavior
Cyclic pattern generation to identify the exact EIP offset
Verification of control over the instruction pointer

This lab demonstrates the foundational steps of buffer overflow exploitation, including how improper input validation can lead to severe security risks such as arbitrary code execution.

⚠️ This project is strictly for educational and ethical hacking practice in a controlled lab environment.
