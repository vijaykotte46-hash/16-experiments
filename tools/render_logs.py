"""Render actual log extracts as labeled evidence images, never as fake app screenshots.

Optional dependency: pip install Pillow
"""
import re
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
try:
    font = ImageFont.truetype('DejaVuSansMono.ttf', 18)
    heading = ImageFont.truetype('DejaVuSans.ttf', 27)
except OSError:
    font = ImageFont.load_default(size=18)
    heading = ImageFont.load_default(size=27)
for path in root.glob('Exp*/results/execution.txt'):
    raw = re.sub(r'\x1b\[[0-9;]*m', '', path.read_text())
    lines = raw.splitlines()
    # Long public modulus/signature hex dumps add little to the overview image.
    lines = [line for line in lines if not re.match(r'^\s+(?:[0-9a-f]{2}:){3}', line)]
    # Avoid unsupported glyphs in this portable image font; full UTF-8 remains in the text file.
    lines = [line for line in lines if not line.startswith(('Original:', 'Recovered:')) or line.isascii()]
    if len(lines) > 65:
        lines = lines[:9] + ['[... middle omitted; full unedited log is in execution.txt ...]'] + lines[-45:]
    wrapped = []
    for line in lines:
        wrapped.extend(textwrap.wrap(line, width=112, replace_whitespace=False, drop_whitespace=False) or [''])
    width, height = 1360, 150 + 26 * len(wrapped)
    canvas = Image.new('RGB', (width, height), '#f5f7fb')
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, width, 106), fill='#132b45')
    draw.text((28, 17), path.parents[1].name, font=heading, fill='white')
    draw.text((28, 58), 'RENDERED EXECUTION LOG EXTRACT — NOT AN APPLICATION SCREENSHOT', font=font, fill='#b7dcff')
    for i, line in enumerate(wrapped):
        draw.text((28, 125 + 26*i), line, font=font, fill='#172d42')
    canvas.save(path.with_name('execution_log.png'))
    print(path.with_name('execution_log.png').relative_to(root))
