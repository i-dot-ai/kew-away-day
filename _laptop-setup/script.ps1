# Run as Administrator

function Check-Installed($command) {
    return [bool](Get-Command $command -ErrorAction SilentlyContinue)
}

# Git
if (Check-Installed "git") {
    Write-Host "Git already installed, skipping." -ForegroundColor Green
} else {
    Write-Host "Installing Git..." -ForegroundColor Yellow
    winget install Git.Git --silent --accept-package-agreements --accept-source-agreements
}

# Claude Code
if (Check-Installed "claude") {
    Write-Host "Claude Code already installed, skipping." -ForegroundColor Green
} else {
    Write-Host "Installing Claude Code..." -ForegroundColor Yellow
    winget install Anthropic.ClaudeCode --silent --accept-package-agreements --accept-source-agreements
}

# VS Code
if (Check-Installed "code") {
    Write-Host "VS Code already installed, skipping." -ForegroundColor Green
} else {
    Write-Host "Installing VS Code..." -ForegroundColor Yellow
    winget install Microsoft.VisualStudioCode --silent --accept-package-agreements --accept-source-agreements
}

Write-Host "Done - please restart PowerShell to pick up changes..." -ForegroundColor Green
