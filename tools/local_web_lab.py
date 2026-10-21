"""Local HTTP/HTTPS fixture for Wireshark experiments. Uses only 127.0.0.1."""
import argparse
import contextlib
import http.client
import http.server
import ssl
import subprocess
import tempfile
import threading
import time
from pathlib import Path

MARKER = b'CSL0509_LOCAL_LAB_ONLY'


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', str(len(MARKER)))
        self.end_headers()
        self.wfile.write(MARKER)

    def log_message(self, *args):
        pass


@contextlib.contextmanager
def servers(tls13=False, fixed_ports=False):
    with tempfile.TemporaryDirectory(prefix='csl0509-web-') as work:
        work = Path(work)
        subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-sha256', '-nodes', '-days', '1', '-keyout', str(work/'key.pem'), '-out', str(work/'cert.pem'), '-subj', '/CN=localhost', '-addext', 'subjectAltName=DNS:localhost,IP:127.0.0.1'], check=True, capture_output=True)
        plain_server = http.server.ThreadingHTTPServer(('127.0.0.1', 8000 if fixed_ports else 0), Handler)
        https = http.server.ThreadingHTTPServer(('127.0.0.1', 8443 if fixed_ports else 0), Handler)
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.minimum_version = ctx.maximum_version = ssl.TLSVersion.TLSv1_3 if tls13 else ssl.TLSVersion.TLSv1_2
        ctx.load_cert_chain(work/'cert.pem', work/'key.pem')
        https.socket = ctx.wrap_socket(https.socket, server_side=True)
        threads = []
        for server in [plain_server, https]:
            t = threading.Thread(target=server.serve_forever, daemon=True)
            t.start(); threads.append(t)
        try:
            yield plain_server.server_address[1], https.server_address[1], work/'cert.pem'
        finally:
            for server in [plain_server, https]:
                server.shutdown(); server.server_close()
            for t in threads:
                t.join(timeout=3)


def demonstrate(results):
    details = []
    print('Local application exchanges only. No packet capture was performed.')
    for tls13 in [False, True]:
        with servers(tls13) as (http_port, https_port, cert):
            plain = http.client.HTTPConnection('127.0.0.1', http_port, timeout=5)
            plain.request('GET', '/CSL0509_LOCAL_LAB_ONLY')
            r = plain.getresponse(); body = r.read(); plain.close()
            assert r.status == 200 and body == MARKER
            context = ssl.create_default_context(cafile=str(cert))
            secure = http.client.HTTPSConnection('127.0.0.1', https_port, context=context, timeout=5)
            secure.connect()
            negotiated = secure.sock.version()
            cipher = secure.sock.cipher()
            peer = secure.sock.getpeercert()
            secure.request('GET', '/CSL0509_LOCAL_LAB_ONLY')
            r = secure.getresponse(); body = r.read(); secure.close()
            assert r.status == 200 and body == MARKER
            data = {'version': negotiated, 'cipher': cipher[0], 'cipher_secret_bits': cipher[2], 'http_status': 200, 'https_status': 200, 'hostname_and_cert_verified': True, 'subject': peer['subject']}
            details.append(data)
            print(data)
    print('HTTP and HTTPS returned the same marker; visibility on the wire still requires Wireshark capture.')
    return {'exchanges': details, 'packet_capture_performed': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--tls13', action='store_true', help='Use TLS 1.3 instead of the TLS 1.2 teaching capture')
    args = p.parse_args()
    with servers(args.tls13, fixed_ports=True) as (http_port, https_port, cert):
        print('HTTP: http://127.0.0.1:8000/CSL0509_LOCAL_LAB_ONLY', flush=True)
        print('HTTPS: https://127.0.0.1:8443/CSL0509_LOCAL_LAB_ONLY', flush=True)
        print('Temporary lab certificate:', cert, flush=True)
        print('Use curl --cacert with that file for HTTPS. Capture the loopback adapter in Wireshark.', flush=True)
        print('Ctrl+C stops both servers and removes the temporary key.', flush=True)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
