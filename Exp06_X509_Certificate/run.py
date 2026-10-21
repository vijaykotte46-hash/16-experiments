"""Create and inspect a self-signed leaf certificate for an isolated lab."""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from lab_support import command, record


def experiment(results):
    command(['openssl', 'version'])
    with tempfile.TemporaryDirectory(prefix='exp06-') as work:
        work = Path(work)
        command(['openssl', 'req', '-x509', '-newkey', 'rsa:3072', '-sha256', '-nodes', '-days', '365', '-keyout', 'private.pem', '-out', 'certificate.pem', '-subj', '/C=IN/O=Cryptography Lab/CN=localhost', '-addext', 'subjectAltName=DNS:localhost,IP:127.0.0.1', '-addext', 'basicConstraints=critical,CA:FALSE', '-addext', 'keyUsage=critical,digitalSignature,keyEncipherment', '-addext', 'extendedKeyUsage=serverAuth'], work, quiet=True)
        description = command(['openssl', 'x509', '-in', 'certificate.pem', '-noout', '-text'], work).stdout
        command(['openssl', 'x509', '-in', 'certificate.pem', '-noout', '-subject', '-issuer', '-dates', '-serial', '-fingerprint', '-sha256'], work)
        command(['openssl', 'verify', '-CAfile', 'certificate.pem', '-purpose', 'sslserver', '-verify_hostname', 'localhost', 'certificate.pem'], work)
        command(['openssl', 'verify', '-CAfile', 'certificate.pem', '-verify_hostname', 'wrong.example', 'certificate.pem'], work, expected='nonzero', quiet=True)
        print('Wrong hostname rejected: PASS')
        command(['openssl', 'verify', '-no-CAfile', '-no-CApath', '-no-CAstore', 'certificate.pem'], work, expected='nonzero', quiet=True)
        print('Certificate rejected without explicit trust: PASS')
        (results / 'certificate.pem').write_bytes((work / 'certificate.pem').read_bytes())
        (results / 'certificate_details.txt').write_text(description)
        return {'subject': 'C=IN,O=Cryptography Lab,CN=localhost', 'key_bits': 3072, 'requested_validity_days': 365, 'san': ['DNS:localhost', 'IP:127.0.0.1'], 'is_ca': False, 'explicit_trust_verification': True, 'wrong_hostname_rejected': True, 'untrusted_self_signed_rejected': True}


if __name__ == '__main__':
    record(__file__, experiment)
