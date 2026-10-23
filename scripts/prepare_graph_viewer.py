"""Prepare a curated viewer directory and fresh aggregate, excluding audit/raw files."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/derived'
FINALS = ['num.jsonl.gz', 'verb_compound.jsonl', 'verb_pfx.jsonl',
          'verb_sfx.jsonl', 'verb_complex.jsonl', 'adv.rare.verified.jsonl',
          'adv_pfx.final.clean.jsonl', 'adv_sfx.clean.jsonl',
          'adv_g1.final.clean.jsonl', 'adv_g2.final.clean.jsonl',
          'adv_g5.clean.jsonl', 'adv_ymx.clean.jsonl']


def prepare():
    destination = DATA / 'viewer'
    destination.mkdir(exist_ok=True)
    inputs = []
    for name in FINALS:
        source = DATA / name
        if not source.exists():
            continue
        link = destination / name
        if link.is_symlink():
            link.unlink()
        elif link.exists():
            raise ValueError('Refusing to replace regular file: ' + str(link))
        link.symlink_to(Path('..') / name)
        inputs.extend(['--input', str(source)])
    if not inputs:
        raise ValueError('No final datasets')
    subprocess.run([sys.executable, str(ROOT / 'scripts/build_unified.py'),
                    *inputs, '--out', str(destination / 'unified.jsonl.gz')], check=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/build_components.py'),
                    *inputs, '--out-dir', str(destination)], check=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/build_components.py'),
                    '--input', str(destination / 'unified.jsonl.gz'),
                    '--aggregate', '--out-dir', str(destination)], check=True)
    (destination / 'viewer_manifest.json').write_text(json.dumps({
        'inputs': [inputs[i] for i in range(1, len(inputs), 2)],
        'aggregate': str(destination / 'unified.jsonl.gz'),
        'command': 'node graph_service/server.js --port 8791 --data ../data/derived/viewer --max-bytes 67108864',
    }, ensure_ascii=False, indent=2) + '\n')
    print('Viewer data:', destination)


if __name__ == '__main__':
    prepare()
