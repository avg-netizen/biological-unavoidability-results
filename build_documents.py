"""Rebuild the author note and optional supplement with Pandoc and Tectonic."""
import argparse
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--allow-downloads', action='store_true')
args = parser.parse_args()
root = Path(__file__).resolve().parent
for stem in ['results', 'additional-results']:
    subprocess.run(['pandoc', stem + '.md', '-s', '--mathml', '--metadata', 'lang=en', '-o', stem + '.html'], cwd=root, check=True)
    subprocess.run(['pandoc', stem + '.md', '-s', '-o', stem + '.tex'], cwd=root, check=True)
    command = ['tectonic', '--keep-logs']
    if not args.allow_downloads:
        command.append('--only-cached')
    subprocess.run(command + [stem + '.tex'], cwd=root, check=True)
