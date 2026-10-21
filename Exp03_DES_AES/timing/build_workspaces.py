"""Build matched timing drafts from supplied CrypTool workspaces; does not run CrypTool."""
from pathlib import Path
import base64
import copy
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
SIZE = 8 * 1024 * 1024
PATTERN = 'HELLO WORLD - CSL0509\n'
INPUT = (PATTERN * (SIZE // len(PATTERN) + 1))[:SIZE]

def load(name):
    return ET.fromstring(gzip.decompress((LAB / name).read_bytes()))

def objects(root):
    return {o.findtext('id'): o for o in root.findall('object')}

def member(obj, name):
    return next(m for m in obj.findall('members/member') if m.findtext('name') == name)

def value(obj, name):
    m = member(obj, name)
    text = m.findtext('value') or ''
    return base64.b64decode(text).decode() if m.find('B64Encoded') is not None else text

def set_value(obj, name, text):
    m = member(obj, name)
    m.find('value').text = base64.b64encode(str(text).encode()).decode() if m.find('B64Encoded') is not None else str(text)

def setting(obj, text):
    set_value(obj, '&lt;Value&gtk__BackingField', text)

def validate(root):
    obs = objects(root)
    assert len(obs) == len(root.findall('object')), 'Duplicate object ID'
    assert all(r.text in obs for r in root.iter('reference')), 'Dangling object reference'
    for o in root:
        for m in o.findall('members/member'):
            if m.find('B64Encoded') is not None:
                base64.b64decode(m.findtext('value') or '', validate=True)
    assert len(value(obs['53'], '&lt;Value&gtk__BackingField').encode('ascii')) == SIZE

manifest = {'status': 'prepared; not executed in CrypTool', 'input_bytes': SIZE,
            'input_sha256': hashlib.sha256(INPUT.encode('ascii')).hexdigest(),
            'mode': 'ECB', 'padding': 'PKCS#7', 'encoding': 'ASCII',
            'scope': 'whole workflow including conversion and limited output preview; not isolated cipher time',
            'files': []}
for cipher in ['DES', 'AES256']:
    root = load('DES_ECB_Demo.cwm')
    obs = objects(root)
    setting(obs['53'], INPUT)
    setting(obs['69'], '0')  # Message Decoder: text
    setting(obs['70'], '4')  # ASCII
    setting(obs['73'], '4')  # Message Encoder: hex preview
    setting(obs['75'], '512')
    setting(obs['42'], '2048')
    setting(obs['76'], '0')  # Encrypt
    set_value(obs['11'], 'RepeatStart', 'False')
    set_value(obs['10'], 'Name', 'Input: 8 MiB ASCII (8388608 bytes)')
    set_value(obs['9'], 'Name', 'Ciphertext preview only')
    # Remove the old instructional annotation, which described the original short demo.
    member(obs['1'], 'AllTextModels').find('list').clear()
    if cipher == 'AES256':
        aesroot = load('AES_CBC_Demo.cwm')
        aes = objects(aesroot)
        set_value(obs['15'], 'PluginTypeName', value(aes['29'], 'PluginTypeName'))
        set_value(obs['15'], 'PluginTypeAssemblyName', value(aes['29'], 'PluginTypeAssemblyName'))
        set_value(obs['15'], 'Name', 'AES-256')
        set_value(obs['11'], 'Name', 'AES key: 32 bytes, public test key')
        setting(obs['59'], ' '.join(f'{n:02X}' for n in range(32)))
        # Replace the DES-specific setting list with settings copied from the user's AES file.
        settings_list = member(obs['8'], 'PersistantSettingsList').find('list')
        settings_list.clear()
        next_id = max(map(int, obs)) + 1
        expected = {'CryptoAlgorithm': '0', 'Action': '0', 'Keysize': '2',
                    'Blocksize': '0', 'Mode': '0', 'Padding': '2'}
        for ref in member(aes['5'], 'PersistantSettingsList').findall('list/entry/reference'):
            clone = copy.deepcopy(aes[ref.text])
            clone.find('id').text = str(next_id)
            setting(clone, expected[value(clone, '&lt;Name&gtk__BackingField')])
            root.append(clone)
            entry = ET.SubElement(settings_list, 'entry')
            ET.SubElement(entry, 'type').text = 'WorkspaceManager.Model.PersistantSetting'
            ET.SubElement(entry, 'reference').text = str(next_id)
            next_id += 1
        # Match connector metadata to the real AES component, retaining the existing wires.
        for des_id, aes_id in [('28', '56'), ('29', '57'), ('30', '59'), ('31', '60'), ('33', '58')]:
            for key in ['ConnectorTypeName', 'ConnectorTypeAssemblyName', 'Index', 'Orientation',
                        '&lt;PropertyName&gtk__BackingField', '&lt;ToolTip&gtk__BackingField', 'Name']:
                set_value(obs[des_id], key, value(aes[aes_id], key))
        # AES has no DES cube-attack connector; it was unused in the source graph.
        for listing in root.iter('list'):
            for entry in list(listing):
                if entry.findtext('reference') == '32':
                    listing.remove(entry)
        root.remove(obs['32'])
    else:
        set_value(obs['11'], 'Name', 'DES key: 8 bytes, public test key')
    validate(root)
    data = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    path = HERE / f'{cipher}_ECB_Timing_8MiB.cwm'
    path.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    validate(ET.fromstring(gzip.decompress(path.read_bytes())))
    manifest['files'].append({'name': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                              'bytes': path.stat().st_size})
(HERE / 'preparation_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))
