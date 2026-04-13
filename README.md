# Claude Code - Windows Setup Guide

## Prerequisites

- Windows 10 (1809+) or Windows 11
- PowerShell **run as Administrator**
- winget available (comes built into Windows 10/11)

For full official requirements, see: https://code.claude.com/docs/en/setup#winget

---

## Steps

### 1. Open PowerShell as Administrator

Right-click the Start menu → **Windows PowerShell (Admin)** or search for PowerShell, right-click → **Run as Administrator**.

---

### 2. Set Execution Policy ⚠️ Manual Step

Run this manually in your admin PowerShell window before anything else:

```powershell
Set-ExecutionPolicy Unrestricted -Scope LocalMachine
```

This allows PowerShell scripts to run on the machine.

---

### 3. Install Git ⚠️ Manual Step

Run this manually:

```powershell
winget install Git.Git --silent --accept-package-agreements --accept-source-agreements
```

Git includes **Git Bash**, which is required for Claude Code.

---

### 4. Run the Install Script

Download `install.ps1` and run it from your admin PowerShell window:

```powershell
.\install.ps1
```

The script will automatically:

- Install **Claude Code** (if not already installed)
- Install **VS Code** (if not already installed)
- Skip anything that is already present
- Open a fresh PowerShell window when done

---

## What the Script Checks & Installs

| Tool | Command Checked | winget Package |
|---|---|---|
| Claude Code | `claude` | `Anthropic.ClaudeCode` |
| VS Code | `code` | `Microsoft.VisualStudioCode` |

Git is excluded from the script as it must be installed manually first (see Step 3).

---

## Troubleshooting

**"Running scripts is disabled on this system"**
Make sure you completed Step 2 (Set Execution Policy) in an admin PowerShell window.

**winget not found**
Update the App Installer from the Microsoft Store, or update Windows to a recent version.

**claude command not found after install**
Close and reopen PowerShell — the script will do this automatically, but if you run commands manually the PATH won't refresh until a new session starts.