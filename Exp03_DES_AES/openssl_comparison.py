"""Supplemental benchmark only; CrypTool execution is still required by the assignment."""
import csv
import os
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from lab_support import command, record


def experiment(results):
    command(['openssl', 'version'])
    print('SUPPLEMENTAL OpenSSL run. This is NOT a CrypTool performance measurement.')
    payload = (b'HELLO WORLD - CSL0509\n' * 50000)[:1048576]
    observations = []
    with tempfile.TemporaryDirectory(prefix='exp03-') as work:
        work = Path(work)
        (work / 'input.bin').write_bytes(payload)
        for cipher, key_len, iv_len in [('des-cbc', 8, 8), ('aes-128-cbc', 16, 16), ('aes-256-cbc', 32, 16)]:
            key, iv = os.urandom(key_len).hex(), os.urandom(iv_len).hex()
            flags = ['-provider', 'default', '-provider', 'legacy'] if cipher == 'des-cbc' else []
            base = ['openssl', 'enc', '-' + cipher] + flags + ['-K', key, '-iv', iv]
            def invoke(extra):
                subprocess.run(base + extra, cwd=work, capture_output=True, check=True)
            invoke(['-in', 'input.bin', '-out', 'cipher.bin'])
            times = []
            for _ in range(5):
                start = time.perf_counter()
                invoke(['-in', 'input.bin', '-out', 'cipher.bin'])
                times.append((time.perf_counter() - start) * 1000)
            invoke(['-d', '-in', 'cipher.bin', '-out', 'recovered.bin'])
            assert (work / 'recovered.bin').read_bytes() == payload
            row = {'cipher': cipher, 'input_bytes': len(payload), 'ciphertext_bytes': (work / 'cipher.bin').stat().st_size, 'median_ms': round(statistics.median(times), 3), 'min_ms': round(min(times), 3), 'max_ms': round(max(times), 3), 'trials': 5, 'round_trip': True}
            observations.append(row)
            print(row)
    print('Timing includes process launch, provider loading, file I/O, padding and encryption; same input and host.')
    print('These are not isolated cipher-throughput measurements; hardware acceleration can favor AES.')
    print('CBC supplies no authentication. DES is obsolete; this comparison is educational.')
    with (results / 'benchmark.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=observations[0].keys())
        writer.writeheader(); writer.writerows(observations)
    return {'tool': 'OpenSSL (supplemental)', 'cryptool_executed': False, 'benchmarks': observations}


if __name__ == '__main__':
    record(__file__, experiment)

