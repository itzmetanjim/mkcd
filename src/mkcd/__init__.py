"""
MKCD - Linux utilities for Windows without WSL

This package provides common Linux command-line utilities (ls, cat, grep, etc.) 
as native Windows executables, making them available in any Windows shell.
"""

import os
import sys
from pathlib import Path
import subprocess
import ctypes

# Import Windows-specific modules only on Windows
if sys.platform == "win32":
    try:
        import winreg
    except ImportError:
        winreg = None
else:
    winreg = None

__version__ = "1.0.6"

def is_admin():
    """Check if the current process is running with administrator privileges."""
    if sys.platform != "win32":
        return False
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def request_admin():
    """Request administrator privileges by re-running the script with UAC elevation."""
    if sys.platform != "win32":
        print("Admin privilege elevation only supported on Windows")
        return False
    
    if is_admin():
        return True
    
    try:
        print("System PATH modification requires administrator privileges.")
        print("This will spawn a new elevated command prompt window.")
        user_input = input("Would you like to request admin privileges? (Y/n): ").lower().strip()

        if user_input not in ['y', 'yes', '']:
            return False
          # Create a temporary script to run the command with elevation
        import tempfile
        import time
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as f:
            # Determine which command was being run - fix the logic to prevent uninstall being detected as install
            is_install = any("install" in arg and "uninstall" not in arg for arg in sys.argv) or ("install" in sys.argv[0] and "uninstall" not in sys.argv[0])
            cmd_name = "mkcd-install" if is_install else "mkcd-uninstall"
            f.write(f'@echo off\n')
            f.write(f'echo Running {cmd_name} with administrator privileges...\n')
            f.write(f'"{sys.executable}" -c "import mkcd; ')
            if is_install:
                f.write('mkcd.install()"')
            else:
                f.write('mkcd.uninstall()"')
            f.write('\n')
            f.write('echo.\n')
            f.write('echo Operation completed. Press any key to close this window...\n')
            f.write('pause > nul\n')
            f.write(f'del "{f.name}"\n')
            temp_script = f.name
        
        print("Requesting administrator privileges...")
        print("Please click 'Yes' in the UAC dialog that appears.")
        
        # Use ShellExecuteW to run with elevated privileges
        result = ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            temp_script,
            None,
            None, 
            1  # SW_SHOWNORMAL
        )
        
        if result > 32:  # Success
            print("Admin privileges granted. Operation running in elevated window...")
            print("Please check the elevated command window for results.")
            return True
        else:
            print("Failed to request admin privileges or user declined.")
            try:
                os.unlink(temp_script)
            except:
                pass
            return False
            
    except Exception as e:
        print(f"Error requesting admin privileges: {e}")
        return False

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

def get_available_utilities():
    """Get list of available utility executables from the binary directory."""
    bin_dir = get_bin_directory()
    if not os.path.exists(bin_dir):
        return []
    
    utilities = []
    for exe_file in Path(bin_dir).glob("*.exe"):
        utility_name = exe_file.stem  # Remove .exe extension
        utilities.append(utility_name)
    
    return utilities

def detect_powershell_aliases():
    """Detect PowerShell aliases that conflict with our utilities."""
    try:
        utilities = get_available_utilities()
        if not utilities:
            return {}
        
        print("Checking for conflicting PowerShell aliases...")
        
        # Get all PowerShell aliases with shorter timeout and simpler command
        result = subprocess.run(
            ["powershell", "-Command", "Get-Alias | ForEach-Object { $_.Name + ':' + $_.Definition }"],
            capture_output=True,
            text=True,
            timeout=5  # Reduced timeout from 10 to 5 seconds
        )
        
        if result.returncode != 0:
            print(f"Warning: Could not detect PowerShell aliases (timeout or error): {result.stderr}")
            print("Skipping alias conflict detection - continuing with installation...")
            return {}
        
        aliases = {}
        for line in result.stdout.strip().split('\n'):
            if line and ':' in line:
                alias_name, definition = line.split(':', 1)
                aliases[alias_name.strip()] = definition.strip()
        
        # Find conflicting aliases
        conflicting_aliases = {}
        for utility in utilities:
            if utility in aliases:
                conflicting_aliases[utility] = aliases[utility]
        
        print(f"Found {len(conflicting_aliases)} conflicting aliases")
        return conflicting_aliases
        
    except subprocess.TimeoutExpired:
        print("Warning: PowerShell alias detection timed out - skipping conflict detection")
        return {}
    except Exception as e:
        print(f"Warning: Error detecting PowerShell aliases: {e}")
        print("Skipping alias conflict detection - continuing with installation...")
        return {}

def remove_powershell_aliases(aliases_to_remove):
    """Remove conflicting PowerShell aliases by modifying the PowerShell profile."""
    if not aliases_to_remove:
        return True
    
    try:
        print(f"Removing {len(aliases_to_remove)} conflicting PowerShell aliases...")
        
        # Get PowerShell profile path
        result = subprocess.run(
            ["powershell", "-Command", "$PROFILE"],
            capture_output=True,
            text=True,
            timeout=5  # Reduced timeout
        )
        
        if result.returncode != 0:
            print("Warning: Could not get PowerShell profile path")
            return False
        
        profile_path = result.stdout.strip()
        
        # Create profile directory if it doesn't exist
        profile_dir = os.path.dirname(profile_path)
        os.makedirs(profile_dir, exist_ok=True)
        
        # Read existing profile content
        profile_content = ""
        if os.path.exists(profile_path):
            with open(profile_path, 'r', encoding='utf-8') as f:
                profile_content = f.read()
        
        # Add commands to remove aliases
        mkcd_section_start = "# MKCD - Remove conflicting aliases (auto-generated)\n"
        mkcd_section_end = "# End MKCD section\n"
        
        # Remove existing MKCD section if present
        start_idx = profile_content.find(mkcd_section_start)
        if start_idx != -1:
            end_idx = profile_content.find(mkcd_section_end, start_idx)
            if end_idx != -1:
                profile_content = profile_content[:start_idx] + profile_content[end_idx + len(mkcd_section_end):]
        
        # Add new MKCD section
        mkcd_commands = [mkcd_section_start]
        for alias_name, original_def in aliases_to_remove.items():
            mkcd_commands.append(f"if (Get-Alias {alias_name} -ErrorAction SilentlyContinue) {{ Remove-Item alias:{alias_name} -Force }}\n")
        mkcd_commands.append(mkcd_section_end)
        
        # Write updated profile
        updated_content = profile_content + "\n" + "".join(mkcd_commands)
        with open(profile_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Updated PowerShell profile: {profile_path}")
        for alias_name, original_def in aliases_to_remove.items():
            print(f"  Removed alias: {alias_name} -> {original_def}")
        
        return True
        
    except Exception as e:
        print(f"Warning: Failed to remove PowerShell aliases: {e}")
        return False

def restore_powershell_aliases():
    """Restore PowerShell aliases by removing MKCD modifications from the profile."""
    try:
        # Get PowerShell profile path
        result = subprocess.run(
            ["powershell", "-Command", "$PROFILE"],
            capture_output=True,
            text=True,
            timeout=5  # Reduced timeout
        )
        
        if result.returncode != 0:
            print("Warning: Could not get PowerShell profile path")
            return False
        
        profile_path = result.stdout.strip()
        
        if not os.path.exists(profile_path):
            print("No PowerShell profile found to restore")
            return True
        
        # Read existing profile content
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile_content = f.read()
        
        # Remove MKCD section
        mkcd_section_start = "# MKCD - Remove conflicting aliases (auto-generated)\n"
        mkcd_section_end = "# End MKCD section\n"
        
        start_idx = profile_content.find(mkcd_section_start)
        if start_idx != -1:
            end_idx = profile_content.find(mkcd_section_end, start_idx)
            if end_idx != -1:
                updated_content = profile_content[:start_idx] + profile_content[end_idx + len(mkcd_section_end):]
                
                # Write updated profile
                with open(profile_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print("Restored PowerShell aliases by removing MKCD modifications")
                return True
        
        print("No MKCD modifications found in PowerShell profile")
        return True
        
    except Exception as e:
        print(f"Warning: Failed to restore PowerShell aliases: {e}")
        return False

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
            if not is_admin():
                print("System PATH modification requires admin privileges.")
                if request_admin():
                    print("System PATH modification attempted in elevated window.")
                    print("Falling back to user PATH for current session...")
                else:
                    print("Falling back to user PATH...")
            else:
                print("Running as admin but still got PermissionError. Falling back to user PATH...")
            
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
        if not is_admin():
            print("System PATH modification requires admin privileges.")
            if request_admin():
                print("System PATH modification attempted in elevated window.")
                print("Continuing with user PATH cleanup...")
            else:
                print("Checking user PATH only...")
        else:
            print("Running as admin but still got PermissionError. Checking user PATH...")
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
    
    # Detect and handle PowerShell aliases (optional, don't fail installation if this fails)
    try:
        conflicting_aliases = detect_powershell_aliases()
        if conflicting_aliases:
            print("Conflicting PowerShell aliases detected:")
            for alias, definition in conflicting_aliases.items():
                print(f"  {alias} -> {definition}")
            remove_powershell_aliases(conflicting_aliases)
        else:
            print("No conflicting PowerShell aliases found")
    except Exception as e:
        print(f"Warning: Alias detection failed: {e}")
        print("Continuing with installation...")
    
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
    
    # Restore PowerShell aliases
    restore_powershell_aliases()
    
    success = remove_from_path()
    if success:
        print("Uninstallation complete!")
    else:
        print("Uninstallation completed but failed to remove from PATH.")
    print("Use pip to uninstall the package completely. The binaries are still in the package, just not in PATH.")
    print("Run: pip uninstall mkcd")
    print("You can also type mkcd-install to reinstall the utilities.")
