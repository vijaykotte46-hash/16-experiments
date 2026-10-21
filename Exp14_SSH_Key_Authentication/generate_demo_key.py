"""Verify RSA key generation only; two-system SSH authentication remains a manual lab."""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from lab_support import command, record


def experiment(results):
    with tempfile.TemporaryDirectory(prefix='exp14-') as work:
        command(['ssh-keygen', '-t', 'rsa', '-b', '3072', '-N', '', '-C', 'synthetic-CSL0509-demo', '-f', 'id_lab_rsa'], work)
        command(['ssh-keygen', '-lf', 'id_lab_rsa.pub'], work)
        (results/'demo_public_key.pub').write_bytes((Path(work)/'id_lab_rsa.pub').read_bytes())
        print('The temporary demo private key was not retained or published.')
        print('No SSH login between systems was attempted; that part remains pending.')
        return {'rsa_bits': 3072, 'key_generation_verified': True, 'two_system_authentication_verified': False, 'kali_environment': False}


if __name__ == '__main__':
    record(__file__, experiment)

