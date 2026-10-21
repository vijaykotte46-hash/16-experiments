# Evidence provenance and validation

## Source and scope

- Base repository: https://github.com/ganeshpalipi/Cryptography-Lab
- Starting commit: 67a9c1b (the full commit is retained in Git history).
- Requirements: supplied Cryptography CSL0509 activity document, academic year 2026–27.
- Existing Experiments 1–2 were preserved; only Experiment 2's doubled PNG extensions were corrected.
- Preparation execution: Linux x86_64, Python 3.12.14, OpenSSL 3.0.13, cryptography 50.0.2. Per-run timestamps and versions are in execution logs.
- John was built from official source commit `5184bc0b8c105f8c5978b112e723d65b2de3e63e` and run against only locally generated synthetic hashes.

## What was executed

| Work | Verification |
|---|---|
| CrypTool DES/AES practical | Five user-supplied Windows CrypTool 2.1 Build 9778.2 screenshots dated 17 October 2026; AES-256-CBC and DES-ECB recover the original 21-character message |
| CrypTool matched 8 MiB initial runs | Three additional user-supplied screenshots: DES and AES-256 completed at 100%; both display 0 seconds, so durations remain unresolved; DES log shows zero errors and one preview truncation warning |
| DES/AES supplement | 1 MiB round trips, five timed trials per cipher |
| RSA/OAEP | Linux run plus two original student Windows PowerShell screenshots dated 17 October 2026: Python 3.9.13, OpenSSL 3.0.19, exact file round trip, oversized-input and modified-ciphertext rejection; all assertions passed |
| RSA-PSS signature | Linux run plus an original student Windows PowerShell screenshot dated 17 October 2026: OpenSSL 3.0.19, distinct SHA-256 hashes, valid signature accepted and changed message rejected; all assertions passed |
| X.509 | Linux run plus three original student Windows PowerShell screenshots dated 17 October 2026: Python 3.9.13, OpenSSL 3.0.19, generation, attributes, explicit trust and correct hostname pass, wrong hostname/untrusted certificate rejected; all assertions passed |
| RSA/DH | Linux run plus two original student Windows VS Code screenshots dated 18 October 2026: Python 3.9.13 virtual environment, cryptography 50.0.2, toy arithmetic, RSA-OAEP, shared-secret equality, HKDF and AES-GCM round trip; all assertions passed |
| AES app | Linux Unicode/empty-message and CLI file tests; original student Windows VS Code screenshot dated 18 October 2026 records demo code, Python 3.9.13, cryptography 50.0.2, exact recovery, matching SHA-256, fresh nonce and wrong-key/tamper rejection; all assertions passed |
| Password hashing | Linux run plus two original student Windows VS Code screenshots dated 18 October 2026: Python 3.9.13, equal unsalted hashes, distinct salted hashes, five-entry dictionary/scrypt comparison and wrong-password rejection; all assertions passed |
| HTTP/TLS fixture | Actual localhost HTTP, TLS 1.2 and TLS 1.3 exchanges |
| Windows Wireshark TLS capture | Student supplied original 21-packet `tls12_lab.pcapng` and seven screenshots dated 18 October 2026; loopback TCP port 8443, TLS 1.2 / ECDHE-RSA-AES256-GCM-SHA384, certificate fields and encrypted application records verified |
| HTTP/HTTPS comparison | Student supplied original 34-packet Windows loopback capture and six screenshots dated 18 October 2026: 13 HTTP packets, 21 TLS packets, readable HTTP request/response and encrypted TLS 1.2 application data |
| John | Dictionary weak-password recovery and bounded three-digit PIN recovery |
| SSH supplement | RSA key generation and public-key fingerprint only |

OpenSSL signatures and certificate files were also independently verified after the scripts finished. The AES CLI was tested through its keygen/encrypt/decrypt commands, including verification that a wrong key writes no plaintext output.

## What was not executed

CrypTool was not executed in the Linux preparation environment; Experiment 3 was subsequently verified from the user's Windows screenshots. Both original `.cwm` workspaces were subsequently supplied and uploaded without modification; their gzip/XML structure was validated, but they were not executed here. Controlled CrypTool timing remains pending. Wireshark was not executed in the Linux preparation environment; the student subsequently captured Experiments 10 and 12 on Windows and supplied the original PCAPNG and GUI screenshots. The supplied PCAPNG was parsed offline and its certificate decoded with OpenSSL. Two-system SSH authentication, an OpenVPN tunnel and Cisco Packet Tracer were not executed here. Raw capture permission was unavailable, and a TUN device and the required GUI tools were unavailable. The OpenVPN generator was syntax-checked only. Linux command-line execution is not evidence of using VS Code or Kali.

The Experiment 4 through 9 files under `results/` remain artifacts of their earlier Linux runs. Windows execution is separately evidenced by the student’s terminal screenshots; Windows-generated public artifacts and logs have not been supplied.

## Image provenance

New `results/execution_log.png` images render actual saved log extracts with a clear label. They may omit middle lines from long logs and lines with non-portable fonts; the full UTF-8 text is retained separately. They do not imitate application windows and do not substitute for the course's required screenshots. Re-running a script changes random keys, certificates, timings and some outputs; regenerate log images if you want them to match a new run.

## Reproduction

Run each listed script from the repository root following its README. Python assertions enforce the stated comparisons. Do not run with Python's `-O` option because it disables assertions. `tools/check_repository.py` validates local image references and the 16 README folders, not practical completion.

Public lab test keys/passwords in examples are teaching inputs. Actual generated private keys are temporary or kept under ignored `.private` paths; no reusable private key is included in the deliverable.


## Experiment 10 capture provenance

The PCAPNG and seven PNG screenshots are unmodified student uploads. The capture SHA-256 is `9b30f533a8ddacce3febae3f76a3ec2fb1aeca4dc7949e1f871b5f9ad21738f1`. All 21 captured packets use 127.0.0.1 with TCP port 8443; screenshots report zero dropped packets. No TLS session secrets or server private key were supplied. Existing Experiment 10 `results/` files remain the earlier Linux application-level fixture evidence, separate from this Windows packet capture.

## Experiment 12 capture provenance

The original `http_https_comparison.pcapng` has SHA-256 `7f7852e9e80aadd9f3370994b41f9e1aa90fd99cc36addd420b2d81c51302526`. All 34 packets are localhost traffic on TCP server ports 8000 or 8443. Six original screenshots record the capture filter, both successful curl requests, HTTP packet list and stream, and HTTPS encrypted record and TCP stream. The PCAPNG was parsed offline: the marker is plaintext in the HTTP flow and absent as plaintext in the HTTPS flow. No TLS session keys were supplied and HTTPS content was not decrypted. Readable `localhost` strings in the HTTPS TCP stream belong to the initial TLS 1.2 certificate; they are not the application message. Screenshots and capture are copied without modification.

Experiment 12 publication status: the six screenshots and analysis are published. Automatic approval review blocked publication of the PCAPNG pending explicit approval for packet payload and local metadata disclosure; the capture file is not yet included in the repository.
