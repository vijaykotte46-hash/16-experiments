"""Run the six OpenSSL/Python exercises; stop on the first failure."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
jobs = [
    ['Exp04_OpenSSL_RSA/run.py'],
    ['Exp05_OpenSSL_Signatures/run.py'],
    ['Exp06_X509_Certificate/run.py'],
    ['Exp07_RSA_Diffie_Hellman/main.py'],
    ['Exp08_AES_Text_App/app.py', 'demo'],
    ['Exp09_Password_Hashing/main.py'],
]
for args in jobs:
    subprocess.run([sys.executable] + args, cwd=root, check=True)
print('Experiments 4–9 passed. Their text/JSON logs were refreshed.')
print('Existing rendered log PNGs are snapshot evidence; regenerate them separately if needed.')

