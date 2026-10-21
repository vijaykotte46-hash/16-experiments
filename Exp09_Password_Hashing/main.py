"""Compare unsalted SHA-256, salted SHA-256 and scrypt on synthetic passwords."""
import hashlib
import hmac
import os
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from lab_support import record


def derive(password, salt):
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32, maxmem=64*1024*1024)


def experiment(results):
    password = 'LabPassword123!'
    salt_a, salt_b = os.urandom(16), os.urandom(16)
    plain_a = hashlib.sha256(password.encode()).hexdigest()
    plain_b = hashlib.sha256(password.encode()).hexdigest()
    salted_a = hashlib.sha256(salt_a + password.encode()).hexdigest()
    salted_b = hashlib.sha256(salt_b + password.encode()).hexdigest()
    assert plain_a == plain_b and salted_a != salted_b
    print('Synthetic password:', password)
    print('Unsalted SHA-256 account A:', plain_a)
    print('Unsalted SHA-256 account B:', plain_b)
    print('Different random salts produce different salted SHA-256 hashes: PASS')
    print('Salt A:', salt_a.hex(), 'Salt B:', salt_b.hex())
    print('Salted SHA-256 A:', salted_a)
    print('Salted SHA-256 B:', salted_b)
    candidates = ['password', '123456', 'letmein', 'LabPassword123!', 'welcome']
    guesses = {}
    for label, test in [('unsalted SHA-256', lambda x: hashlib.sha256(x.encode()).hexdigest() == plain_a), ('salted SHA-256', lambda x: hashlib.sha256(salt_a + x.encode()).hexdigest() == salted_a)]:
        found = next((x for x in candidates if test(x)), None)
        assert found == password
        guesses[label] = found
        print(label + ': supplied dictionary recovered the weak password.')
    started = time.perf_counter()
    stored = derive(password, salt_a)
    hash_ms = (time.perf_counter() - started) * 1000
    assert hmac.compare_digest(stored, derive(password, salt_a))
    assert not hmac.compare_digest(stored, derive('wrong-password', salt_a))
    started = time.perf_counter()
    found = next((x for x in candidates if hmac.compare_digest(stored, derive(x, salt_a))), None)
    attack_ms = (time.perf_counter() - started) * 1000
    assert found == password
    print('scrypt: N=16384, r=8, p=1, salt=16 bytes, derived key=32 bytes')
    print(f'One scrypt derivation: {hash_ms:.2f} ms; dictionary search to match: {attack_ms:.2f} ms (this machine only)')
    print('scrypt correct password accepted; wrong password rejected: PASS')
    print('scrypt also recovered the dictionary password, but each guess has a higher cost.')
    strong = 'sample-only-W9q!v3#Ld7@z2'
    strong_hash = derive(strong, salt_b)
    matched = any(hmac.compare_digest(strong_hash, derive(x, salt_b)) for x in candidates)
    assert not matched
    print('Second sample was not in this five-entry dictionary; this does not prove it uncrackable.')
    return {'unsalted_equal_for_equal_passwords': True, 'different_salts_change_hash': True, 'dictionary_entries': len(candidates), 'weak_password_recovered_with_all_three_methods': True, 'scrypt_hash_ms': round(hash_ms, 2), 'scrypt_dictionary_ms': round(attack_ms, 2), 'wrong_password_rejected': True, 'second_sample_in_dictionary': False, 'scrypt_parameters': {'N': 16384, 'r': 8, 'p': 1}}


if __name__ == '__main__':
    record(__file__, experiment)
