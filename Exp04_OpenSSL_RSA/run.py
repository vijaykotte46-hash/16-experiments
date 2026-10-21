"""RSA-OAEP file encryption with OpenSSL, including rejection checks."""
import hashlib
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from lab_support import command, record


def experiment(results):
    command(['openssl', 'version'])
    with tempfile.TemporaryDirectory(prefix='exp04-') as work:
        work = Path(work)
        message = b'Cryptography CSL0509: RSA-OAEP protects this short laboratory file.\n'
        (work / 'message.txt').write_bytes(message)
        command(['openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', 'rsa_keygen_bits:3072', '-out', 'private.pem'], work, quiet=True)
        command(['openssl', 'pkey', '-in', 'private.pem', '-pubout', '-out', 'public.pem'], work)
        padding = ['-pkeyopt', 'rsa_padding_mode:oaep', '-pkeyopt', 'rsa_oaep_md:sha256', '-pkeyopt', 'rsa_mgf1_md:sha256']
        command(['openssl', 'pkeyutl', '-encrypt', '-pubin', '-inkey', 'public.pem', '-in', 'message.txt', '-out', 'encrypted.bin'] + padding, work)
        command(['openssl', 'pkeyutl', '-decrypt', '-inkey', 'private.pem', '-in', 'encrypted.bin', '-out', 'decrypted.txt'] + padding, work)
        recovered = (work / 'decrypted.txt').read_bytes()
        assert recovered == message
        print('Exact file equality: PASS')
        print('Recovered:', recovered.decode().strip())
        print('SHA-256:', hashlib.sha256(message).hexdigest())
        (work / 'oversize.bin').write_bytes(b'x' * 319)
        command(['openssl', 'pkeyutl', '-encrypt', '-pubin', '-inkey', 'public.pem', '-in', 'oversize.bin', '-out', 'rejected.bin'] + padding, work, expected='nonzero', quiet=True)
        print('319-byte input correctly rejected; OAEP SHA-256 limit is 318 bytes for RSA-3072.')
        damaged = bytearray((work / 'encrypted.bin').read_bytes())
        damaged[20] ^= 1
        (work / 'damaged.bin').write_bytes(damaged)
        command(['openssl', 'pkeyutl', '-decrypt', '-inkey', 'private.pem', '-in', 'damaged.bin', '-out', 'invalid.txt'] + padding, work, expected='nonzero', quiet=True)
        print('Modified ciphertext rejected: PASS')
        for name in ['message.txt', 'public.pem', 'encrypted.bin', 'decrypted.txt']:
            (results / name).write_bytes((work / name).read_bytes())
        return {'rsa_bits': 3072, 'oaep_digest': 'SHA-256', 'plaintext_bytes': len(message), 'ciphertext_bytes': 384, 'exact_round_trip': True, 'tamper_rejected': True, 'oversized_input_rejected': True, 'private_key_published': False}


if __name__ == '__main__':
    record(__file__, experiment)

