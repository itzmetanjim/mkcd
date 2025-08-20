#!/usr/bin/env python3
# Standalone helper: fetch MSYS2 (mingw-w64) binaries and copy them to a target folder.
# Usage: python scripts/fetch_msys2_binaries.py --target ./binaries/windows_x86_64 --install

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_MSYS2_ROOTS = [Path("C:/msys64"), Path("C:/msys32")]

DEFAULT_BINS = [
    'ls.exe','cp.exe','mv.exe','rm.exe','rmdir.exe','mkdir.exe','install.exe','ln.exe',
    'readlink.exe','realpath.exe','stat.exe','touch.exe','chmod.exe','chown.exe','pwd.exe',
    'du.exe','df.exe','sync.exe','truncate.exe','cat.exe','head.exe','tail.exe','nl.exe','wc.exe',
    'cut.exe','paste.exe','join.exe','sort.exe','uniq.exe','tr.exe','od.exe','fold.exe','fmt.exe',
    'column.exe','expand.exe','unexpand.exe','sed.exe','gawk.exe','grep.exe','xargs.exe','tee.exe',
    'split.exe','csplit.exe','comm.exe','find.exe','which.exe','tar.exe','gzip.exe','gunzip.exe',
    'bzip2.exe','bunzip2.exe','xz.exe','unxz.exe','zip.exe','unzip.exe','md5sum.exe','sha1sum.exe',
    'sha256sum.exe','base64.exe','uname.exe','hostname.exe','whoami.exe','id.exe','date.exe'
]

DEFAULT_PACKAGES = [
    'mingw-w64-x86_64-coreutils', 'mingw-w64-x86_64-grep', 'mingw-w64-x86_64-sed',
    'mingw-w64-x86_64-gawk', 'mingw-w64-x86_64-findutils', 'mingw-w64-x86_64-diffutils',
    'mingw-w64-x86_64-file', 'mingw-w64-x86_64-which', 'mingw-w64-x86_64-tar',
    'mingw-w64-x86_64-zip', 'mingw-w64-x86_64-unzip', 'mingw-w64-x86_64-gzip',
    'mingw-w64-x86_64-bzip2', 'mingw-w64-x86_64-xz'
]


def is_windows():
    return platform.system().lower().startswith('windows')


def find_msys2_root(explicit_root: Path | None = None) -> Path | None:
    if explicit_root:
        if explicit_root.exists():
            return explicit_root
        return None
    # Check environment variables
    for key in ('MSYS2_ROOT', 'MSYS2_HOME', 'MSYS2_PATH'):
        val = os.environ.get(key)
        if val:
            p = Path(val)
            if p.exists():
                return p
    # Common locations
    for p in DEFAULT_MSYS2_ROOTS:
        if p.exists():
            return p
    return None


def run_pacman(msys2_root: Path, packages: list[str], no_update: bool = False) -> int:
    bash = msys2_root / 'usr' / 'bin' / 'bash.exe'
    if not bash.exists():
        print(f"ERROR: bash not found under {msys2_root / 'usr' / 'bin'}. Is MSYS2 installed here?", file=sys.stderr)
        return 2

    # Build pacman commands. Use --noconfirm to avoid interactive prompts.
    cmds = []
    if not no_update:
        # Full update can require restart; attempt a safe update first
        cmds.append('pacman -Syu --noconfirm')
    pkgs = ' '.join(packages)
    if pkgs:
        cmds.append(f'pacman -S --noconfirm {pkgs}')

    full_cmd = ' && '.join(cmds)
    print(f"Running in MSYS2: {full_cmd}")
    try:
        proc = subprocess.run([str(bash), '-lc', full_cmd], check=False)
        return proc.returncode
    except Exception as e:
        print(f"Failed to run pacman: {e}", file=sys.stderr)
        return 3


def copy_binaries(msys2_root: Path, target_dir: Path, bins: list[str], arch: str = 'x86_64') -> tuple[int, int]:
    mingw_dir = msys2_root / ('mingw64' if arch in ('x86_64','amd64') else 'mingw32') / 'bin'
    if not mingw_dir.exists():
        print(f"ERROR: mingw bin directory not found at {mingw_dir}", file=sys.stderr)
        return (0, 0)

    target_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    missing = 0
    for name in bins:
        src = mingw_dir / name
        dst = target_dir / name
        if src.exists():
            try:
                shutil.copy2(src, dst)
                copied += 1
                print(f"Copied: {name}")
            except Exception as e:
                print(f"Failed to copy {name}: {e}", file=sys.stderr)
        else:
            print(f"Missing in mingw bin, skipping: {name}")
            missing += 1
    return (copied, missing)


def parse_args():
    p = argparse.ArgumentParser(description='Fetch MSYS2 mingw-w64 binaries and copy them to a target folder.')
    p.add_argument('--msys2-root', type=Path, default=None, help='Path to MSYS2 root (default: detect C:\\msys64)')
    p.add_argument('--target', type=Path, default=Path('binaries/windows_x86_64'), help='Target directory to copy EXEs into')
    p.add_argument('--arch', choices=['x86_64','arm64','i686'], default='x86_64', help='Target architecture to use (mingw64/mingw32)')
    p.add_argument('--install', action='store_true', help='Run pacman to install required mingw packages before copying')
    p.add_argument('--no-update', action='store_true', help='Do not run pacman -Syu (skip full update)')
    p.add_argument('--bins-file', type=Path, default=None, help='Path to a newline-separated file listing binary filenames to copy')
    return p.parse_args()


def main():
    if not is_windows():
        print('This helper script is intended to run on Windows where MSYS2 is available.', file=sys.stderr)
        sys.exit(1)

    args = parse_args()

    msys2_root = find_msys2_root(args.msys2_root)
    if not msys2_root:
        print('MSYS2 installation not found. Please install MSYS2 from https://www.msys2.org/ and re-run or supply --msys2-root.', file=sys.stderr)
        sys.exit(2)

    print(f'Using MSYS2 root: {msys2_root}')

    # Determine which binaries to copy
    if args.bins_file:
        if not args.bins_file.exists():
            print(f'Bins file {args.bins_file} not found', file=sys.stderr)
            sys.exit(3)
        bins = [line.strip() for line in args.bins_file.read_text(encoding='utf-8').splitlines() if line.strip()]
    else:
        bins = DEFAULT_BINS

    if args.install:
        print('Installing packages via pacman...')
        rc = run_pacman(msys2_root, DEFAULT_PACKAGES, no_update=args.no_update)
        if rc != 0:
            print(f'pacman returned non-zero exit code: {rc}. You may need to run MSYS2 shell and update manually.', file=sys.stderr)

    target = args.target
    print(f'Copying binaries to target: {target}')
    copied, missing = copy_binaries(msys2_root, target, bins, arch=args.arch)
    print(f'Copy complete. Copied: {copied}, Missing: {missing}')
    if copied == 0:
        print('No files copied. Check that MSYS2 mingw packages are installed and the mingw bin folder contains executables.', file=sys.stderr)
        sys.exit(4)

if __name__ == '__main__':
    main()
