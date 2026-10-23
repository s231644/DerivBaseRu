"""Install the graph viewer as a per-user macOS launchd service."""
import argparse
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LABEL = 'ai.openclaw.derivbase-graphview'


def configuration(node, port):
    logs = ROOT / 'graph_service/logs'
    return {
        'Label': LABEL,
        'ProgramArguments': [node, str(ROOT / 'graph_service/server.js'),
                             '--host', '127.0.0.1', '--port', str(port),
                             '--data', str(ROOT / 'data/derived/viewer'),
                             '--max-bytes', '67108864'],
        'WorkingDirectory': str(ROOT / 'graph_service'),
        'RunAtLoad': True, 'KeepAlive': True, 'ThrottleInterval': 3,
        'ExitTimeOut': 5,
        'StandardOutPath': str(logs / 'out.log'),
        'StandardErrorPath': str(logs / 'err.log'),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8792)
    parser.add_argument('--install', action='store_true', help='install and start; otherwise print plist')
    args = parser.parse_args()
    node = shutil.which('node')
    if not node:
        raise SystemExit('Node.js is not available')
    if not 1 <= args.port <= 65535:
        raise SystemExit('Invalid port')
    contents = plistlib.dumps(configuration(node, args.port))
    if not args.install:
        sys.stdout.buffer.write(contents)
        return
    if not (ROOT / 'data/derived/viewer/unified.jsonl.gz').exists():
        raise SystemExit('Prepare data first: python scripts/prepare_graph_viewer.py')
    folder = Path.home() / 'Library/LaunchAgents'
    folder.mkdir(parents=True, exist_ok=True)
    (ROOT / 'graph_service/logs').mkdir(exist_ok=True)
    path = folder / (LABEL + '.plist')
    domain = 'gui/' + str(os.getuid())
    service = domain + '/' + LABEL
    loaded = subprocess.run(['launchctl', 'print', service],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    if path.exists():
        shutil.copy2(path, path.with_suffix('.plist.previous'))
    temporary = path.with_suffix('.plist.tmp')
    temporary.write_bytes(contents)
    subprocess.run(['plutil', '-lint', str(temporary)], check=True)
    if loaded:
        subprocess.run(['launchctl', 'bootout', service], check=True)
    temporary.replace(path)
    subprocess.run(['launchctl', 'enable', service], check=True)
    subprocess.run(['launchctl', 'bootstrap', domain, str(path)], check=True)
    subprocess.run(['launchctl', 'kickstart', service], check=True)
    print('Service:', service)
    print('URL: http://127.0.0.1:' + str(args.port))
    print('Configuration:', path)


if __name__ == '__main__':
    main()
