"""RSA and finite-field DH: textbook arithmetic plus library-based cryptography."""
import os
import sys
from pathlib import Path
import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from lab_support import record

# RFC 3526, 2048-bit MODP Group 14. A known group avoids custom prime generation.
GROUP14 = int('''FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1
29024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD
3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44
C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B
1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163
FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966
D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C
180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF695581718
3995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF'''.replace('\n', ''), 16)


def experiment(results):
    print('cryptography:', cryptography.__version__)
    # Tiny integers teach the arithmetic only; these keys are not secure.
    p, q, e, m = 61, 53, 17, 65
    n = p * q
    d = pow(e, -1, (p - 1) * (q - 1))
    c = pow(m, e, n)
    assert pow(c, d, n) == m
    print(f'Textbook RSA (INSECURE teaching example): n={n}, e={e}, d={d}, message={m}, ciphertext={c}, recovered={pow(c,d,n)}')
    small_p, g, a, b = 23, 5, 6, 15
    A, B = pow(g, a, small_p), pow(g, b, small_p)
    shared = pow(B, a, small_p)
    assert shared == pow(A, b, small_p)
    print(f'Textbook DH (INSECURE teaching example): p=23, g=5, A={A}, B={B}, shared={shared}')
    key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    oaep = padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    plaintext = b'RSA library demonstration'
    encrypted = key.public_key().encrypt(plaintext, oaep)
    assert key.decrypt(encrypted, oaep) == plaintext
    print('RSA-3072 / OAEP SHA-256 round trip: PASS')
    assert GROUP14.bit_length() == 2048
    parameters = dh.DHParameterNumbers(GROUP14, 2).parameters()
    alice, bob = parameters.generate_private_key(), parameters.generate_private_key()
    secret_a = alice.exchange(bob.public_key())
    secret_b = bob.exchange(alice.public_key())
    assert secret_a == secret_b
    salt = os.urandom(16)
    def derive(secret):
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b'CSL0509-DH-demo').derive(secret)
    ka, kb = derive(secret_a), derive(secret_b)
    assert ka == kb
    nonce = os.urandom(12)
    message = b'Alice and Bob derived the same encryption key.'
    ciphertext = AESGCM(ka).encrypt(nonce, message, b'exp07')
    assert AESGCM(kb).decrypt(nonce, ciphertext, b'exp07') == message
    print('DH 2048-bit group: shared secrets match; HKDF keys match; AES-GCM round trip PASS')
    print('No real private key, shared secret, or derived AES key is printed.')
    print('DH alone does not authenticate the peer; signatures/certificates are needed against MITM.')
    return {'toy_rsa_ciphertext': c, 'toy_dh_shared': shared, 'rsa_oaep_round_trip': True, 'dh_group_bits': 2048, 'dh_shared_secret_matches': True, 'hkdf_keys_match': True, 'aes_gcm_round_trip': True, 'peer_authentication_implemented': False}


if __name__ == '__main__':
    record(__file__, experiment)

