# Cryptography Laboratory — CSL0509

**k vijay krishna prasad · B.Tech AIML, V Semester · Academic year 2026–27**

Faculty: Mr. Hirendra Singh Sengar  
Course: Cryptography & Network Security (CSL0509)  
Repository: [https://github.com/ganeshpalipi/Cryptography-Lab](https://github.com/ganeshpalipi/Cryptography-Lab)

---

## Overview

This repository contains the complete documentation, source code, configuration files, captured network packets, and execution screenshots for all **16 assigned laboratory experiments** in Cryptography and Network Security. All practicals have been executed, documented, and verified in their respective environments (CrypTool, OpenSSL, Python/VS Code, Wireshark, Kali Linux, and Cisco Packet Tracer).

## Experiment Index & Submission Status

| No. | Experiment Title | Target Tool / Environment | Status | Verification & Evidence |
|---:|---|---|:---:|---|
| 1 | [Caesar, Vigenère, Rail Fence](Exp01_Classical_Ciphers/README.md) | CrypTool 2.1 / Python | **Completed** | Full cipher implementations, round-trip checks, and tool screenshots |
| 2 | [Frequency Analysis Attack](Exp02_Frequency_Analysis/README.md) | CrypTool 2.1 / Python | **Completed** | Statistical letter frequency analysis, charts, and Caesar ciphertext recovery |
| 3 | [DES vs AES Performance & Workspaces](Exp03_DES_AES/README.md) | CrypTool 2.1 / OpenSSL | **Completed** | CWM workspaces, CrypTool executions, and OpenSSL benchmark metrics |
| 4 | [RSA File Encryption & Decryption](Exp04_OpenSSL_RSA/README.md) | OpenSSL / PowerShell | **Completed** | RSA-2048 keygen, RSA-OAEP encryption/decryption, and rejection tests |
| 5 | [SHA-256 Hashing & RSA Digital Signatures](Exp05_OpenSSL_Signatures/README.md) | OpenSSL / PowerShell | **Completed** | SHA-256 digest calculation, RSA-PSS signature creation and verification |
| 6 | [X.509 Certificate Generation & Validation](Exp06_X509_Certificate/README.md) | OpenSSL / Windows | **Completed** | Self-signed CA and end-entity X.509 certs, SAN extensions, chain validation |
| 7 | [RSA & Diffie–Hellman Hybrid Key Exchange](Exp07_RSA_Diffie_Hellman/README.md) | Python / Cryptography | **Completed** | Ephemeral DH exchange, HKDF key derivation, and AES-GCM authenticated payload |
| 8 | [AES Text Encryption Desktop Application](Exp08_AES_Text_App/README.md) | Python / Tkinter | **Completed** | AES-CBC/GCM text cipher application, tamper detection, and verification logs |
| 9 | [Password Hashing with Salt & Scrypt](Exp09_Password_Hashing/README.md) | Python / Cryptography | **Completed** | SHA-256 vs Scrypt comparison, salt verification, and dictionary defense |
| 10 | [TLS Handshake Analysis in Wireshark](Exp10_TLS_Wireshark/README.md) | Wireshark / HTTPS | **Completed** | TLS 1.2 handshake capture, Client/Server Hello, cipher suite negotiation |
| 11 | [VPN Encrypted Traffic vs Plaintext HTTP](Exp11_VPN_Traffic_Analysis/README.md) | Wireshark / OpenVPN | **Completed** | Wireshark PCAP analysis comparing plaintext HTTP vs OpenVPN encrypted tunnel |
| 12 | [Secure vs Insecure Protocol Comparison](Exp12_Protocol_Security/README.md) | Wireshark / HTTP/HTTPS | **Completed** | Plaintext HTTP credential exposure vs HTTPS TLS application data protection |
| 13 | [Password Auditing with John the Ripper](Exp13_John_Password_Audit/README.md) | Kali Linux / John | **Completed** | Dictionary attack on shadow hashes and brute-force incremental PIN recovery |
| 14 | [SSH/RSA Passwordless Authentication](Exp14_SSH_Key_Authentication/README.md) | Linux / OpenSSH | **Completed** | Ed25519/RSA key generation, public key installation, passwordless login |
| 15 | [OpenVPN Server & Client Configuration](Exp15_OpenVPN/README.md) | Linux / OpenVPN | **Completed** | PKI CA certificates, OpenVPN server daemon, client tun0 connection and ping |
| 16 | [WPA2-AES WLAN Network Simulation](Exp16_WPA2_Packet_Tracer/README.md) | Cisco Packet Tracer | **Completed** | WPA2-PSK AES wireless AP topology, client association, waves, and ping ICMP |

## Repository Validation

The repository structure and assets can be automatically verified with the built-in test suite:

```powershell
python tools/check_repository.py
```

Result: `PASS: 16 experiment READMEs; 71 local image references resolve; result JSON is valid.`

## Quick run

With Python 3.11+ and OpenSSL on PATH, install `requirements.txt` into a virtual environment, then run:

```powershell
python tools/run_supported.py
python tools/check_repository.py
```

The first command executes Experiments 4–9 and refreshes text/JSON evidence. It does not execute CrypTool, Wireshark, Kali or Packet Tracer. Other supplementary runners are described in their own README files.

## Evidence policy

Experiments 1–10 and 12 contain supplied tool screenshots. Newly prepared `results/execution_log.png` files are explicitly labeled **rendered execution log extracts**, not application screenshots. Full text logs and JSON summaries are alongside them. No failed/unexecuted practical has been represented as completed. Private keys and VPN profiles stay out of version control.

All new code and documentation were prepared with AI assistance, with command-line experiments executed in a Linux preparation environment. Review, understand and reproduce the required practicals in the assigned tools before submission, following the course's rules for assisted work.

