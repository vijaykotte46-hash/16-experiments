import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from lab_support import record
from local_web_lab import demonstrate

if __name__ == '__main__':
    record(__file__, demonstrate)

