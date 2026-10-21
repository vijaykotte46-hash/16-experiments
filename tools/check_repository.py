"""Check all 16 experiment folders, local Markdown images and result JSON."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
folders = sorted(root.glob('Exp[0-9][0-9]_*'))
assert len(folders) == 16, f'Expected 16 experiment folders, found {len(folders)}'
image_count = 0
for folder in folders:
    assert (folder / 'README.md').is_file(), folder
for readme in root.rglob('*.md'):
    if '.git' in readme.parts or '.venv' in readme.parts:
        continue
    markdown = re.sub(r'```.*?```', '', readme.read_text(encoding='utf-8'), flags=re.S)
    for link in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', markdown):
        if not link.startswith(('http:', 'https:', 'data:')):
            assert (readme.parent / link).is_file(), f'Broken image: {readme}: {link}'
            image_count += 1
for path in root.glob('Exp*/results/summary.json'):
    json.loads(path.read_text())
print(f'PASS: {len(folders)} experiment READMEs; {image_count} local image references resolve; result JSON is valid.')
print('This structural check does not establish completion of pending GUI/network experiments.')

