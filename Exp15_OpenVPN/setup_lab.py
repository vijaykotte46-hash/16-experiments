"""Generate an isolated two-VM OpenVPN lab in .private; never publishes private keys."""
import argparse
import ipaddress
import shutil
import subprocess
from pathlib import Path


def run(args, cwd):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server-ip', required=True, help='IPv4 address of your own server VM on the host-only network')
    args = parser.parse_args()
    server_ip = str(ipaddress.IPv4Address(args.server_ip))
    if not shutil.which('openvpn') or not shutil.which('openssl'):
        parser.error('Install OpenVPN and OpenSSL in your Kali lab VM before running this script.')
    root = Path(__file__).resolve().parent / '.private'
    root.mkdir(mode=0o700, exist_ok=False)
    ca = root/'ca'; ca.mkdir(mode=0o700)
    run(['openssl','req','-x509','-newkey','rsa:3072','-nodes','-sha256','-days','30','-keyout','ca.key','-out','ca.crt','-subj','/CN=CSL0509 Lab CA','-addext','basicConstraints=critical,CA:TRUE','-addext','keyUsage=critical,keyCertSign,cRLSign'], ca)
    for role, usage in [('server','serverAuth'),('client','clientAuth')]:
        folder=root/role; folder.mkdir(mode=0o700)
        run(['openssl','req','-new','-newkey','rsa:3072','-nodes','-keyout',f'{role}.key','-out',f'{role}.csr','-subj',f'/CN=lab-{role}'], folder)
        (folder/'extensions.cnf').write_text(f'basicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature\nextendedKeyUsage={usage}\n')
        run(['openssl','x509','-req','-in',f'{role}.csr','-CA',str(ca/'ca.crt'),'-CAkey',str(ca/'ca.key'),'-CAcreateserial','-days','7','-sha256','-extfile','extensions.cnf','-out',f'{role}.crt'], folder)
        shutil.copyfile(ca/'ca.crt', folder/'ca.crt')
        run(['openssl','verify','-CAfile','ca.crt','-purpose','sslserver' if role=='server' else 'sslclient',f'{role}.crt'], folder)
    run(['openvpn','--genkey','secret','tls-crypt.key'], root/'server')
    shutil.copyfile(root/'server/tls-crypt.key', root/'client/tls-crypt.key')
    common='proto udp\ndev tun\nca ca.crt\ntls-crypt tls-crypt.key\ntls-version-min 1.2\ndata-ciphers AES-256-GCM:AES-128-GCM\nallow-compression no\npersist-key\npersist-tun\nverb 3\n'
    (root/'server/server.conf').write_text(common+'port 1194\nserver 10.8.0.0 255.255.255.0\ntopology subnet\ncert server.crt\nkey server.key\ndh none\nremote-cert-tls client\nkeepalive 10 60\n')
    (root/'client/client.conf').write_text(common+f'client\nremote {server_ip} 1194\nnobind\ncert client.crt\nkey client.key\nremote-cert-tls server\nverify-x509-name lab-server name\n')
    for path in root.rglob('*.key'):
        path.chmod(0o600)
    print('Created private lab configuration at', root)
    print('Copy ONLY the client directory to the client VM through your trusted lab transfer channel.')
    print('Server: cd .private/server && sudo openvpn --config server.conf')
    print('Client: cd client && sudo openvpn --config client.conf')
    print('This config tunnels the lab subnet only; it does not route all internet traffic.')


if __name__ == '__main__':
    main()
