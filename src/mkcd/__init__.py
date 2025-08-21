"""
MKCD - Linux utilities for Windows without WSL

This package provides common Linux command-line utilities (ls, cat, grep, etc.) 
as native Windows executables, making them available in any Windows shell.
"""

import os
import sys
from pathlib import Path
import subprocess

# Import Windows-specific modules only on Windows
if sys.platform == "win32":
    try:
        import winreg
    except ImportError:
        winreg = None
else:
    winreg = None

__version__ = "1.0.2"

def get_bin_directory():
    """Get the absolute path to the bundled binary directory."""
    package_dir = Path(__file__).parent
    bin_dir = package_dir / "_bin" / "windows_x86_64"
    bin_path = str(bin_dir.absolute())
    
    # Debug information
    if not bin_dir.exists():
        print(f"Debug: Binary directory not found at: {bin_path}")
        print(f"Debug: Package directory: {package_dir}")
        print(f"Debug: Directory contents: {list(package_dir.iterdir()) if package_dir.exists() else 'Package dir does not exist'}")
    
    return bin_path

def add_to_path():
    """Add the binary directory to the system PATH."""
    if sys.platform != "win32":
        print("Warning: PATH modification only supported on Windows")
        return False
    
    if winreg is None:
        print("Error: winreg module not available")
        return False
    
    bin_dir = get_bin_directory()
    if not os.path.exists(bin_dir):
        print(f"Error: Binary directory not found: {bin_dir}")
        return False
    
    # Try system PATH first (requires admin), fall back to user PATH
    try:
        # First try system PATH (HKEY_LOCAL_MACHINE)
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    current_path, _ = winreg.QueryValueEx(key, "PATH")
                except FileNotFoundError:
                    current_path = ""
                
                # Check if already in system PATH
                if bin_dir.lower() in current_path.lower():
                    print(f"Binary directory already in system PATH: {bin_dir}")
                    return True
                
                # Add to system PATH
                new_path = f"{current_path};{bin_dir}" if current_path else bin_dir
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                
                print(f"Successfully added to system PATH: {bin_dir}")
                print("Note: You may need to restart your shell for changes to take effect. In tabbed terminal emulators like Windows Terminal, you will have to open and close the entire app, not just the tab.")
                print(f"NOTE: To add manually, type in PowerShell: $env:Path += ';{bin_dir}'")
                print(f"or in CMD: setx PATH \"%PATH%;{bin_dir}\"")
                return True
                
        except PermissionError:
            print("System PATH modification requires admin privileges. Falling back to user PATH...")
            print(f"NOTE: To add manually, type in PowerShell: $env:Path += ';{bin_dir}'")
            print(f"or in CMD: setx PATH \"%PATH%;{bin_dir}\"")
            # Fall back to user PATH
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
                try:
                    current_path, _ = winreg.QueryValueEx(key, "PATH")
                except FileNotFoundError:
                    current_path = ""
                
                # Check if already in user PATH
                if bin_dir.lower() in current_path.lower():
                    print(f"Binary directory already in user PATH: {bin_dir}")
                    return True
                
                # Add to user PATH
                new_path = f"{current_path};{bin_dir}" if current_path else bin_dir
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                
                print(f"Successfully added to user PATH: {bin_dir}")
                print("Note: You may need to restart your shell for changes to take effect. In tabbed terminal emulators like Windows Terminal, you will have to open and close the entire app, not just the tab.")
                return True
            
    except Exception as e:
        print(f"Error adding to PATH: {e}")
        print(f"NOTE: To add manually, type in PowerShell: $env:Path += ';{bin_dir}'")
        print(f"or in CMD: setx PATH \"%PATH%;{bin_dir}\"")
        print(f"Attempting to run the CMD command as fallback...")
        code = os.system(f'setx PATH "%PATH%;{bin_dir}"')
        if code == 0:
            print("Successfully added to PATH using CMD command. You may need to restart your shell.")
            return True
        else:
            print("Failed to add to PATH using CMD command.")
            print("You can manually run: mkcd-install")
            print("Error code from CMD command:", code)
        return False

def remove_from_path():
    """Remove the binary directory from the system and user PATH."""
    if sys.platform != "win32":
        print("Warning: PATH modification only supported on Windows")
        return False
    
    if winreg is None:
        print("Error: winreg module not available")
        return False
    
    bin_dir = get_bin_directory()
    success = False
    
    # Try to remove from system PATH first
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, winreg.KEY_ALL_ACCESS) as key:
            try:
                current_path, _ = winreg.QueryValueEx(key, "PATH")
                path_entries = [p.strip() for p in current_path.split(";") if p.strip()]
                new_entries = [p for p in path_entries if p.lower() != bin_dir.lower()]
                
                if len(new_entries) != len(path_entries):
                    new_path = ";".join(new_entries)
                    winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                    print(f"Successfully removed from system PATH: {bin_dir}")
                    success = True
                    
            except FileNotFoundError:
                pass  # No system PATH variable
                
    except PermissionError:
        print("System PATH modification requires admin privileges. Checking user PATH...")
    except Exception as e:
        print(f"Error checking system PATH: {e}")
    
    # Also try to remove from user PATH
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:
            try:
                current_path, _ = winreg.QueryValueEx(key, "PATH")
                path_entries = [p.strip() for p in current_path.split(";") if p.strip()]
                new_entries = [p for p in path_entries if p.lower() != bin_dir.lower()]
                
                if len(new_entries) != len(path_entries):
                    new_path = ";".join(new_entries)
                    winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                    print(f"Successfully removed from user PATH: {bin_dir}")
                    success = True
                else:
                    if not success:
                        print(f"Binary directory not found in user PATH: {bin_dir}")
                        
            except FileNotFoundError:
                if not success:
                    print("No user PATH environment variable found")
                    
    except Exception as e:
        print(f"Error removing from user PATH: {e}")
        
    return success

def install():
    """Install mkcd and add binaries to PATH."""
    print("Installing mkcd utilities...")
    
    # First check if binaries are available
    bin_dir = get_bin_directory()
    if not os.path.exists(bin_dir):
        print(f"Error: Binary directory not found: {bin_dir}")
        print("The package may not have been built correctly.")
        return False
        
    # Count available binaries
    exe_files = list(Path(bin_dir).glob("*.exe"))
    dll_files = list(Path(bin_dir).glob("*.dll"))
    print(f"Found {len(exe_files)} executables and {len(dll_files)} DLL files")
    
    success = add_to_path()
    if success:
        print("Installation complete! Linux utilities are now available in your shell.")
        print("Available commands: ls, cat, grep, sed, gawk, tar, gzip, and many more.")
        print("Try running: ls --help")
        return True
    else:
        print("Installation completed but failed to add to PATH.")
        print("You may need to manually add the binary directory to your PATH:")
        print(f"  {bin_dir}")
        return False

def uninstall():
    """Uninstall mkcd and remove binaries from PATH."""
    print("Uninstalling mkcd utilities...")
    success = remove_from_path()
    if success:
        print("Uninstallation complete!")
    else:
        print("Uninstallation completed but failed to remove from PATH.")
    print("Use pip to uninstall the package completely. The binaries are still in the package, just not in PATH.")
    print("Run: pip uninstall mkcd")
    print("You can also type mkcd-install to reinstall the utilities.")
