"""John auditing restricted to synthetic hashes created by this script."""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from lab_support import command, record


def experiment(results, john):
    print('Authorized synthetic fixtures only; no account database is read.')
    command([john, '--list=build-info'])
    with tempfile.TemporaryDirectory(prefix='exp13-') as work:
        work = Path(work)
        samples = [('weak_lab', 'password123'), ('pin_lab', '427'), ('long_lab', 'Lab-only!K8q#V4m@X7t$R2n')]
        records = []
        for index, (name, password) in enumerate(samples):
            hashed = subprocess.run(['openssl', 'passwd', '-6', '-salt', f'LabSalt{index}', '-stdin'], input=password+'\n', text=True, capture_output=True, check=True).stdout.strip()
            records.append(name + ':' + hashed)
        (work/'hashes.txt').write_text('\n'.join(records)+'\n')
        (work/'pin.txt').write_text(records[1]+'\n')
        (work/'words.txt').write_text('password\nletmein\npassword123\nwelcome\n')
        command([john, '--format=sha512crypt', '--wordlist=words.txt', '--pot=lab.pot', 'hashes.txt'], work)
        shown = command([john, '--show', '--format=sha512crypt', '--pot=lab.pot', 'hashes.txt'], work).stdout
        assert 'weak_lab:password123' in shown and 'long_lab:' not in shown
        print('Dictionary recovered weak_lab; long_lab not recovered from the supplied dictionary.')
        command([john, '--format=sha512crypt', '--mask=?d?d?d', '--max-run-time=30', '--pot=pin.pot', 'pin.txt'], work)
        pin = command([john, '--show', '--format=sha512crypt', '--pot=pin.pot', 'pin.txt'], work).stdout
        assert 'pin_lab:427' in pin
        print('Bounded exhaustive search recovered the three-digit lab PIN: PASS')
        print('A limited dictionary miss does not establish that a password is uncrackable.')
        for name in ['hashes.txt', 'words.txt']:
            (results/name).write_bytes((work/name).read_bytes())
        return {'target': 'three synthetic lab hashes', 'hash_format': 'sha512crypt', 'dictionary_entries': 4, 'weak_password_recovered': True, 'bounded_three_digit_pin_recovered': True, 'long_sample_recovered_in_dictionary': False, 'kali_environment': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--john', default='john', help='Path to John the Ripper jumbo binary')
    args = parser.parse_args()
    record(__file__, lambda results: experiment(results, args.john))

