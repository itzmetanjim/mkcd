"""
Colorized wrappers for ls and grep commands.

This module provides Python wrappers that automatically add --color=auto
to ls and grep commands for colorized output.
"""

import os
import sys
import subprocess
from pathlib import Path

def get_bin_directory():
    """Get the absolute path to the bundled binary directory."""
    package_dir = Path(__file__).parent
    bin_dir = package_dir / "_bin" / "windows_x86_64"
    return str(bin_dir.absolute())

def ls_color():
    """Colorized ls wrapper that automatically adds --color=auto."""
    bin_dir = get_bin_directory()
    ls_exe = os.path.join(bin_dir, "ls.exe")
    
    if not os.path.exists(ls_exe):
        print(f"Error: ls.exe not found at {ls_exe}")
        sys.exit(1)
    
    # Build command with --color=auto automatically added
    args = sys.argv[1:]  # Get all arguments except script name
    
    # Check if color option is already specified
    has_color_option = any(arg.startswith('--color') for arg in args)
    
    if not has_color_option:
        # Add --color=auto if not already specified
        args.insert(0, '--color=auto')
    
    # Execute ls with all arguments
    try:
        result = subprocess.run([ls_exe] + args, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running ls: {e}")
        sys.exit(1)

def grep_color():
    """Colorized grep wrapper that automatically adds --color=auto."""
    bin_dir = get_bin_directory()
    grep_exe = os.path.join(bin_dir, "grep.exe")
    
    if not os.path.exists(grep_exe):
        print(f"Error: grep.exe not found at {grep_exe}")
        sys.exit(1)
    
    # Build command with --color=auto automatically added
    args = sys.argv[1:]  # Get all arguments except script name
    
    # Check if color option is already specified
    has_color_option = any(arg.startswith('--color') or arg.startswith('--colour') for arg in args)
    
    if not has_color_option:
        # Add --color=auto if not already specified
        args.insert(0, '--color=auto')
    
    # Execute grep with all arguments
    try:
        result = subprocess.run([grep_exe] + args, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running grep: {e}")
        sys.exit(1)
