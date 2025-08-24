# MKCD - Linux Utilities for Windows

Have you ever typed `ps | grep edge` or `wget https://example.com` or some other command with Linux utilities, only to find out you are in windows and have to use the stupid PowerShell syntax that no one knows about? You may even be tricked into thinking the command exists because of PowerShell aliases that are nonfunctional. That's why MKCD exists. MKCD brings over 70 essential Linux utilities directly to your Windows command line. No virtual machines, no containers, no hassle.

## Why MKCD?

Working on Windows but miss the power of Linux command-line tools? You're not alone. Whether you're a developer who needs `grep` for quick searches, a sysadmin who relies on `tail` for log monitoring, or anyone who finds Windows equivalents just don't cut it, MKCD has you covered.

MKCD provides native Windows executables for all your favorite Linux utilities:

- **Text processing**: `grep`, `sed`, `awk`, `cut`, `sort`, `uniq`
- **File operations**: `ls`, `cp`, `mv`, `rm`, `find`, `chmod`
- **System monitoring**: `ps`, `top`, `df`, `du`, `stat`
- **Archive handling**: `tar`, `gzip`, `gunzip`, `zip`
- **And many more**: `head`, `tail`, `cat`, `wc`, `diff`, `which`, `whereis`

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

This will:

1. Launch a User Account Control (UAC) dialog asking for administrator privileges
2. You will have to click "Yes" to grant permission (required to modify system PATH)
3. Open a new elevated command window
4. After the installation completes and shows "Operation completed. Press any key to close this window...", press Enter
5. The elevated window will close automatically

### Step 3: Open a New Terminal

> **Important**: You must open a completely new terminal window for the changes to take effect. Simply opening a new tab in Windows Terminal may not work - you need to close and reopen the entire application.
> If commands still aren't recognized after opening a new terminal, a system restart may be required.

## Colorized Output

MKCD automatically enables colorized output for `ls` and `grep` commands, making your terminal experience more pleasant and easier to read.

## Troubleshooting

### Commands Not Found After Installation

- Make sure you opened a completely new terminal (not just a new tab)
- Try restarting your computer
- Check if the installation succeeded by running `mkcd-install` again

### UAC Prompts

The installer needs administrator privileges to modify your system PATH. This is normal and safe - we only modify environment variables to make the Linux utilities available system-wide.

### Uninstalling

To remove MKCD utilities from your PATH:

```bash
mkcd-uninstall
```

To completely remove the package:

```bash
pip uninstall mkcd
```

## What's Included

MKCD includes over 70 Linux utilities compiled for Windows, including:

| Category | Commands |
|----------|----------|
| **File Operations** | `cp`, `mv`, `rm`, `mkdir`, `rmdir`, `ls`, `chmod`, `chown` |
| **Text Processing** | `grep`, `sed`, `gawk`, `cut`, `sort`, `uniq`, `tr`, `wc` |
| **File Viewing** | `cat`, `head`, `tail`, `less`, `more` |
| **Archive Tools** | `tar`, `gzip`, `gunzip`, `bzip2`, `bunzip2`, `xz`, `unxz` |
| **System Info** | `ps`, `top`, `df`, `du`, `stat`, `uname`, `whoami`, `which` |
| **Text Utilities** | `diff`, `comm`, `join`, `paste`, `column`, `fmt`, `fold` |

And many more! Each command works just like its Linux counterpart, with the same options and behavior you expect.

## Requirements

- Windows 10 or later
- Python 3.9 or higher
- Administrator privileges (for installation only)

## License

MKCD is released under the MIT License. See the LICENSE file for details.
The MSYS2 project, which provides the underlying tools, is licensed under the GNU General Public License v3.0 (GPL-3.0). MKCD does not include any GPL-licensed code; it simply uses the MSYS2 environment to compile and run the utilities.
