# Start here — Windows laptop

## 1. Fix that was made

Experiment 2 had images ending in `.png.png`, while its README linked to `.png`. The four images have been renamed to match their existing links. The original practical content and CrypTool workspace files have been retained.

## 2. Open and run Experiments 4–9

Open the repository folder in VS Code. Use Python 3.11 or newer and make sure `openssl version` succeeds in the integrated terminal.

```powershell
python --version
openssl version
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe tools/run_supported.py
```

Using the interpreter's full path avoids PowerShell activation-policy issues. Choose this `.venv` interpreter in VS Code as well. If an executable is missing, install it before continuing; a command-not-found error is not a cryptographic result.

Each experiment stores its actual run under `results`. For screenshots, show the VS Code window or terminal with the relevant setup and output, then use Windows Snipping Tool. Save images with the names listed in that experiment's README. Never capture a real private key, account password or API token.

## 3. Finish in this order

1. Experiment 3 in CrypTool.
2. Experiments 4–9: run the prepared scripts and capture the required environment/results.
3. Experiments 10 and 12: capture the provided local HTTP/HTTPS fixture in Wireshark.
4. Experiment 13: run the supplied synthetic audit in Kali.
5. Experiment 14: connect two owned Linux lab VMs with SSH public-key authentication.
6. Experiment 15: create and verify the OpenVPN tunnel between those VMs.
7. Experiment 11: use that tunnel for the plaintext-versus-encrypted traffic comparison.
8. Experiment 16 in Cisco Packet Tracer and save the real `.pkt` topology.

The VM IP addresses in the guides are examples. Substitute actual addresses from your isolated lab.

## 4. Add real screenshot links

Once an image actually exists, add a relative link such as:

```markdown
![OpenSSL results](screenshots/02_RSA_Results.png)
```

File names and capital letters must match. Windows may hide extensions; enable file-name extensions so that `.png` is not accidentally added twice.

## 5. Check before submission

```powershell
.venv\Scripts\python.exe tools/check_repository.py
```

This checks folder/image structure only. Review each pending item in `REMAINING_WORK.md` and update status only after completing it. Existing rendered log PNGs are snapshots of the recorded preparation run; after rerunning, optionally install Pillow and execute `python tools/render_logs.py` to refresh them. They remain log illustrations, not tool screenshots.

## 6. Git publication

From the cloned repository after reviewing changes:

```powershell
git status
git add .
git commit -m "Add cryptography lab implementations and documented evidence"
git push
```

Check the staged file list before committing. `.private`, private keys, SSH identities, VPN profiles and temporary John pot files are ignored. Use GitHub's normal authentication flow rather than pasting credentials into a chat. If applying a provided patch to a fresh clone, first run `git apply --check PATH_TO_PATCH`, then `git apply PATH_TO_PATCH`; apply it only once.
