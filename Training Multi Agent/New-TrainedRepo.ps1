<#
.SYNOPSIS
    Initialize a new git repo with EMADS-PR copilot-instructions.md auto-included.
    
.USAGE
    # Create new repo with training context:
    D:\active-projects\Training Multi Agent\New-TrainedRepo.ps1 "D:\my-new-project"
    
    # Or add alias to PowerShell profile:
    Set-Alias git-new "D:\active-projects\Training Multi Agent\New-TrainedRepo.ps1"
    git-new "D:\my-new-project"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoPath
)

$templateSource = Join-Path $PSScriptRoot ".github\copilot-instructions.md"

# Create directory if not exists
if (!(Test-Path $RepoPath)) {
    New-Item -ItemType Directory -Path $RepoPath -Force | Out-Null
}

# Git init
git init $RepoPath

# Copy copilot-instructions.md
$destDir = Join-Path $RepoPath ".github"
New-Item -ItemType Directory -Path $destDir -Force | Out-Null
Copy-Item $templateSource (Join-Path $destDir "copilot-instructions.md") -Force

Write-Host ""
Write-Host "✅ Repo initialized with EMADS-PR training context!" -ForegroundColor Green
Write-Host "   Path: $RepoPath" -ForegroundColor Cyan
Write-Host "   File: .github/copilot-instructions.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "Copilot will now auto-apply EMADS-PR rules in this repo." -ForegroundColor Yellow
