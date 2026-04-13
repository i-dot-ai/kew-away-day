# Run as Administrator

# Git
winget install Git.Git --silent --accept-package-agreements --accept-source-agreements

# Claude Code
winget install Anthropic.ClaudeCode --silent --accept-package-agreements --accept-source-agreements

# VS Code - only install if not already present
if (-not (Get-Command code -ErrorAction SilentlyContinue)) {
    Write-Host "VS Code not found, installing..." -ForegroundColor Yellow
    winget install Microsoft.VisualStudioCode --silent --accept-package-agreements --accept-source-agreements
} else {
    Write-Host "VS Code already installed, skipping." -ForegroundColor Green
}

Write-Host "Done" -ForegroundColor Green