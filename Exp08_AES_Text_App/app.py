"""Small AES-256-GCM text-file application with SHA-256 comparison."""
import argparse
import base64
import hashlib
import json
import os
import sys
from pathlib import Path
import cryptography
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from lab_support import record

AAD = b'CSL0509-AES-text-v1'


def encrypt(key, plaintext):
    nonce = os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, AAD)
    return {'version': 1, 'algorithm': 'AES-256-GCM', 'nonce': base64.b64encode(nonce).decode(), 'ciphertext_and_tag': base64.b64encode(ciphertext).decode()}


def decrypt(key, envelope):
    if envelope.get('version') != 1 or envelope.get('algorithm') != 'AES-256-GCM':
        raise ValueError('Unsupported encrypted-message format')
    return AESGCM(key).decrypt(base64.b64decode(envelope['nonce'], validate=True), base64.b64decode(envelope['ciphertext_and_tag'], validate=True), AAD)


def demo(results):
    print('cryptography:', cryptography.__version__)
    message = 'Hello Ganesh — నమస్తే! Secure message for CSL0509.'.encode('utf-8')
    key = AESGCM.generate_key(bit_length=256)
    envelope = encrypt(key, message)
    recovered = decrypt(key, envelope)
    assert recovered == message
    repeat = encrypt(key, message)
    assert repeat['nonce'] != envelope['nonce']
    print('Algorithm: AES-256-GCM; nonce: 12 random bytes; authentication tag: 16 bytes')
    print('Original:', message.decode())
    print('Recovered:', recovered.decode())
    print('SHA-256 original:', hashlib.sha256(message).hexdigest())
    print('SHA-256 recovered:', hashlib.sha256(recovered).hexdigest())
    print('Exact bytes match: PASS; repeated encryption uses a fresh nonce: PASS')
    for label, badkey, badenv in [('wrong key', AESGCM.generate_key(bit_length=256), envelope)]:
        try:
            decrypt(badkey, badenv)
        except InvalidTag:
            print(label + ' rejected: PASS')
        else:
            raise AssertionError('Wrong key was accepted')
    tampered = dict(envelope)
    data = bytearray(base64.b64decode(tampered['ciphertext_and_tag']))
    data[0] ^= 1
    tampered['ciphertext_and_tag'] = base64.b64encode(data).decode()
    try:
        decrypt(key, tampered)
    except InvalidTag:
        print('Modified ciphertext rejected: PASS')
    else:
        raise AssertionError('Tampered ciphertext was accepted')
    assert decrypt(key, encrypt(key, b'')) == b''
    (results / 'encrypted_message.json').write_text(json.dumps(envelope, indent=2))
    (results / 'recovered.txt').write_bytes(recovered)
    return {'algorithm': 'AES-256-GCM', 'unicode_round_trip': True, 'empty_message_round_trip': True, 'sha256': hashlib.sha256(message).hexdigest(), 'tamper_rejected': True, 'wrong_key_rejected': True, 'fresh_nonce_verified': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('demo')
    keygen = sub.add_parser('keygen')
    keygen.add_argument('--key', required=True)
    for action in ['encrypt', 'decrypt']:
        p = sub.add_parser(action)
        p.add_argument('--key', required=True)
        p.add_argument('--input', required=True)
        p.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.action == 'demo':
        record(__file__, demo)
        return
    if args.action == 'keygen':
        fd = os.open(args.key, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(AESGCM.generate_key(bit_length=256))
        print('Created private key file. Keep it out of GitHub.')
        return
    key = Path(args.key).read_bytes()
    if len(key) != 32:
        parser.error('AES-256 requires a 32-byte key file')
    try:
        if args.action == 'encrypt':
            original = Path(args.input).read_bytes()
            payload = json.dumps(encrypt(key, original), indent=2).encode()
            print('Plaintext SHA-256:', hashlib.sha256(original).hexdigest())
        else:
            payload = decrypt(key, json.loads(Path(args.input).read_text()))
            print('Recovered SHA-256:', hashlib.sha256(payload).hexdigest())
        with open(args.output, 'xb') as stream:
            stream.write(payload)
        print('Saved:', args.output)
    except (InvalidTag, ValueError, KeyError) as error:
        parser.exit(1, 'Decryption/format validation failed; no plaintext written.\n')


if __name__ == '__main__':
    main()

