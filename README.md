# MKCD - Linux Utilities for Windows

Have you ever typed `ps | grep edge` or `wget https://example.com` or some other command with Linux utilities, only to find out you are in windows and have to use the stupid PowerShell syntax that no one knows about? You may even be tricked into thinking the command exists because of PowerShell aliases that are nonfunctional. That's why MKCD exists. MKCD brings over 70\* essential Linux utilities directly to your Windows command line. No virtual machines, no containers, no hassle.

\*not all are available now

## Why MKCD?

Working on Windows but miss the power of Linux command-line tools? You're not alone. Whether you're a developer who needs `grep` for quick searches, a sysadmin who relies on `tail` for log monitoring, or anyone who finds Windows equivalents just don't cut it, MKCD has you covered.

MKCD provides native Windows executables for all your favorite Linux utilities:

- **Text processing**: `grep`, `sed`, `awk`, `cut`, `sort`, `uniq`,...
- **File operations**: `ls`, `cp`, `mv`, `rm`, `find`, `chmod`,...
- **System monitoring**: `ps`, `top`, `df`, `du`, `stat`,...
- **Archive handling**: `tar`, `gzip`, `gunzip`, `zip`,`xz`,...
- **And many more**: `head`, `tail`, `cat`, `wc`, `diff`, `which`, `whereis`,...

No learning curve. No compatibility issues. Just the Linux tools you know and love, running natively on Windows.

## Installation

Getting started with MKCD is straightforward, but there are a few important steps to follow:
> Note: `ls`, `cat`, `curl`, etc are mapped as aliases in PowerShell (which can cause confusion when you type something like `ls -la`), but they are removed and readded automatically on install/uninstall.

### Step 1: Install the Package

```bash
pip install mkcd
```

### Step 2: Run the Installer

```bash
mkcd-install
```

If Python scripts are not on PATH, you can run this:

```bash
python -c "import mkcd;mkcd.install()"
```

> **Important**: You must open a completely new terminal window for the changes to take effect. Simply opening a new tab in Windows Terminal may not work - you need to close and reopen the entire application.
> If commands still aren't recognized after opening a new terminal, a system restart may be required.

It will ask for permission to launch a UAC window. Type "y", hit enter, then click "Yes" in the window.

Example Output:

```plaintext
Installing mkcd utilities...
Found 61 executables and 20 DLL files
Checking for conflicting PowerShell aliases...
Found 9 conflicting aliases
Conflicting PowerShell aliases detected:
  cat -> Get-Content
  cp -> Copy-Item
  ls -> Get-ChildItem
  mv -> Move-Item
  pwd -> Get-Location
  rm -> Remove-Item
  rmdir -> Remove-Item
  sort -> Sort-Object
  tee -> Tee-Object
Removing 9 conflicting PowerShell aliases...
Updated PowerShell profile: C:\Users\hp\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
  Removed alias: cat -> Get-Content
  Removed alias: cp -> Copy-Item
  Removed alias: ls -> Get-ChildItem
  Removed alias: mv -> Move-Item
  Removed alias: pwd -> Get-Location
  Removed alias: rm -> Remove-Item
  Removed alias: rmdir -> Remove-Item
  Removed alias: sort -> Sort-Object
  Removed alias: tee -> Tee-Object
System PATH modification requires admin privileges.
System PATH modification requires administrator privileges.
This will spawn a new elevated command prompt window.
Would you like to request admin privileges? (Y/n): Y
Requesting administrator privileges...
Please click 'Yes' in the UAC dialog that appears.
Admin privileges granted. Operation running in elevated window...
Please check the elevated command window for results.
System PATH modification attempted in elevated window.
Falling back to user PATH for current session...
NOTE: To add manually, type in PowerShell: $env:Path += ';D:\SYSPY\Lib\site-packages\mkcd\_bin\windows_x86_64'
or in CMD: setx PATH "%PATH%;D:\SYSPY\Lib\site-packages\mkcd\_bin\windows_x86_64"
Successfully added to user PATH: D:\SYSPY\Lib\site-packages\mkcd\_bin\windows_x86_64
Note: You may need to restart your shell for changes to take effect. In tabbed terminal emulators like Windows Terminal, you will have to open and close the entire app, not just the tab.
Installation complete! Linux utilities are now available in your shell.
Available commands: ls, cat, grep, sed, gawk, tar, gzip, and many more.
Try running: ls --help
```

## Troubleshooting

### Commands Not Found After Installation

- Make sure you opened a completely new terminal (not just a new tab)
- Try restarting your computer
- Check if the installation succeeded by running `mkcd-install` again

### `ls` and `grep` not being colorized or not working

This may be because your python scripts are not in PATH. To add them to PATH, first type this in PowerShell/CMD to find your Python installation:

```bash
python -c "import sys; print(sys.executable)"
```

Your output should be like this: `C:\Python39\python.exe`, ending in `python.exe`. Remove the `python.exe` part, and add `Scripts\` to the end. In this example, it would be `C:\Python39\Scripts\`. Copy this new scripts path.

Search for `Edit the system environment variables` in your search bar, hit Enter, then click Environment Variables. In both the "User variables" and "System variables",  find where the variable name is Path, then click "Edit" > "New", then paste your copied path. Click "Ok" > "Ok".

You can also run the following command in PowerShell:

```pwsh
$env:Path += ';' + "<your script path>"
```

No matter which method you choose, make sure to restart your terminal for the changes to take effect.

## Uninstalling

To remove MKCD utilities from your PATH:

```bash
mkcd-uninstall
```

> Some utilities like `ls` and `grep` may stay. This is because they are linked as a script for colorization.
> Running the previous command will not delete the binaries from your computer.

You will need admin privileges.

To completely remove the package:

```bash
pip uninstall mkcd
```

## Requirements

- Windows 10 or later
- Python 3.9 or higher
- Administrator privileges (for installation only)

## License

MKCD is released under the MIT License. See the LICENSE file for details.

The MSYS2 project, which provides the underlying tools, is licensed under the GNU General Public License v3.0 (GPL-3.0). MKCD does not include any GPL-licensed code; it uses the MSYS2 environment to compile and run the utilities.
