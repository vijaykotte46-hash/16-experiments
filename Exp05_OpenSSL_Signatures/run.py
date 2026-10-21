"""SHA-256 and RSA-PSS signing; reject a modified message."""
import hashlib
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from lab_support import command, record


def experiment(results):
    command(['openssl', 'version'])
    with tempfile.TemporaryDirectory(prefix='exp05-') as work:
        work = Path(work)
        original = b'Approve laboratory report version 1.\n'
        changed = b'Approve laboratory report version 2.\n'
        (work / 'message.txt').write_bytes(original)
        (work / 'modified.txt').write_bytes(changed)
        command(['openssl', 'dgst', '-sha256', 'message.txt', 'modified.txt'], work)
        command(['openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', 'rsa_keygen_bits:3072', '-out', 'private.pem'], work, quiet=True)
        command(['openssl', 'pkey', '-in', 'private.pem', '-pubout', '-out', 'public.pem'], work)
        opts = ['-sigopt', 'rsa_padding_mode:pss', '-sigopt', 'rsa_pss_saltlen:digest']
        command(['openssl', 'dgst', '-sha256', '-sign', 'private.pem', '-out', 'signature.bin'] + opts + ['message.txt'], work)
        command(['openssl', 'dgst', '-sha256', '-verify', 'public.pem', '-signature', 'signature.bin'] + opts + ['message.txt'], work)
        command(['openssl', 'dgst', '-sha256', '-verify', 'public.pem', '-signature', 'signature.bin'] + opts + ['modified.txt'], work, expected='nonzero', quiet=True)
        print('Modified message verification rejected: PASS')
        for name in ['message.txt', 'modified.txt', 'public.pem', 'signature.bin']:
            (results / name).write_bytes((work / name).read_bytes())
        return {'sha256_original': hashlib.sha256(original).hexdigest(), 'sha256_modified': hashlib.sha256(changed).hexdigest(), 'signature_scheme': 'RSA-PSS SHA-256', 'valid_signature_accepted': True, 'modified_message_rejected': True}


if __name__ == '__main__':
    record(__file__, experiment)

