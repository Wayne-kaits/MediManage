# Hospital Management System - Professional EXE Installer Builder
# Publisher: Kaitsnet IT Solutions
# PowerShell Build Script

param(
    [switch]$Clean,
    [switch]$Verbose,
    [switch]$Sign,
    [string]$OutputDir = "dist"
)

# Script configuration
$AppName = "Hospital Management System"
$AppVersion = "1.0.0"
$Publisher = "Kaitsnet IT Solutions"
$InstallerName = "HospitalManagementSystem_v${AppVersion}_Setup.exe"

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " $AppName - Professional EXE Installer Builder" -ForegroundColor White
Write-Host " Publisher: $Publisher" -ForegroundColor White
Write-Host " Version: $AppVersion" -ForegroundColor White
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Function to install Python package
function Install-PythonPackage {
    param($Package)
    Write-Host "Installing $Package..." -ForegroundColor Yellow
    $result = & python -m pip install $Package 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $Package installed successfully" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ Failed to install $Package" -ForegroundColor Red
        Write-Host $result -ForegroundColor Red
        return $false
    }
}

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
if (-not (Test-Command "python")) {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7+ from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    exit 1
}

$pythonVersion = & python --version 2>&1
Write-Host "✓ $pythonVersion detected" -ForegroundColor Green

# Check required packages
Write-Host "Checking build dependencies..." -ForegroundColor Yellow

$requiredPackages = @("PyInstaller", "Pillow")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    $checkResult = & python -c "import $package" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $package found" -ForegroundColor Green
    } else {
        Write-Host "✗ $package not found" -ForegroundColor Red
        $missingPackages += $package
    }
}

# Install missing packages
if ($missingPackages.Count -gt 0) {
    Write-Host "Installing missing packages..." -ForegroundColor Yellow
    foreach ($package in $missingPackages) {
        if (-not (Install-PythonPackage $package)) {
            Write-Host "Build failed due to missing dependencies" -ForegroundColor Red
            exit 1
        }
    }
}

# Clean build directories if requested
if ($Clean) {
    Write-Host "Cleaning build directories..." -ForegroundColor Yellow
    if (Test-Path "build") {
        Remove-Item "build" -Recurse -Force
        Write-Host "✓ Cleaned build directory" -ForegroundColor Green
    }
    if (Test-Path $OutputDir) {
        Remove-Item $OutputDir -Recurse -Force
        Write-Host "✓ Cleaned output directory" -ForegroundColor Green
    }
}

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
    Write-Host "✓ Created output directory: $OutputDir" -ForegroundColor Green
}

# Run the build process
Write-Host "Starting build process..." -ForegroundColor Yellow
Write-Host ""

$buildArgs = @()
if ($Verbose) {
    $buildArgs += "--verbose"
}

try {
    $buildResult = & python build_installer.py @buildArgs 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Build completed successfully!" -ForegroundColor Green
        
        # Check if installer was created
        $installerPath = Join-Path $OutputDir $InstallerName
        if (Test-Path $installerPath) {
            $fileSize = (Get-Item $installerPath).Length / 1MB
            Write-Host "✓ Installer created: $installerPath" -ForegroundColor Green
            Write-Host "  Size: $([math]::Round($fileSize, 1)) MB" -ForegroundColor Green
            
            # Digital signing (if requested and certificate available)
            if ($Sign) {
                Write-Host "Checking for code signing certificate..." -ForegroundColor Yellow
                # Add your code signing logic here
                Write-Host "! Code signing not configured" -ForegroundColor Yellow
            }
            
            # Generate checksums
            Write-Host "Generating checksums..." -ForegroundColor Yellow
            $md5Hash = Get-FileHash $installerPath -Algorithm MD5
            $sha256Hash = Get-FileHash $installerPath -Algorithm SHA256
            
            $checksumFile = Join-Path $OutputDir "checksums.txt"
            @"
$AppName v$AppVersion - Installer Checksums
Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Publisher: $Publisher

File: $InstallerName
Size: $([math]::Round($fileSize, 1)) MB

MD5:    $($md5Hash.Hash)
SHA256: $($sha256Hash.Hash)
"@ | Out-File $checksumFile -Encoding UTF8
            
            Write-Host "✓ Checksums saved to: $checksumFile" -ForegroundColor Green
            
            # Create distribution package info
            $packageInfo = @{
                name = $AppName
                version = $AppVersion
                publisher = $Publisher
                installer = $InstallerName
                size_mb = [math]::Round($fileSize, 1)
                build_date = Get-Date -Format 'yyyy-MM-dd'
                build_time = Get-Date -Format 'HH:mm:ss'
                checksums = @{
                    md5 = $md5Hash.Hash
                    sha256 = $sha256Hash.Hash
                }
                system_requirements = @{
                    os = "Windows 10 or higher"
                    python = "3.7+ (included)"
                    ram = "4GB minimum"
                    disk = "100MB"
                }
            }
            
            $packageInfoFile = Join-Path $OutputDir "package_info.json"
            $packageInfo | ConvertTo-Json -Depth 3 | Out-File $packageInfoFile -Encoding UTF8
            Write-Host "✓ Package info saved to: $packageInfoFile" -ForegroundColor Green
            
        } else {
            Write-Host "✗ Installer file not found after build" -ForegroundColor Red
            exit 1
        }
        
    } else {
        Write-Host "✗ Build failed!" -ForegroundColor Red
        Write-Host $buildResult -ForegroundColor Red
        exit 1
    }
    
} catch {
    Write-Host "✗ Build process failed with exception:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Summary
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host " BUILD SUMMARY" -ForegroundColor White
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Application: $AppName" -ForegroundColor White
Write-Host "Version: $AppVersion" -ForegroundColor White
Write-Host "Publisher: $Publisher" -ForegroundColor White
Write-Host "Installer: $installerPath" -ForegroundColor White
Write-Host "Size: $([math]::Round($fileSize, 1)) MB" -ForegroundColor White
Write-Host ""
Write-Host "Distribution Package Contents:" -ForegroundColor Yellow
Write-Host "• Professional Windows executable installer" -ForegroundColor White
Write-Host "• Complete application with all modules" -ForegroundColor White
Write-Host "• Automatic dependency installation" -ForegroundColor White
Write-Host "• Desktop and Start Menu shortcuts" -ForegroundColor White
Write-Host "• Windows Programs & Features integration" -ForegroundColor White
Write-Host "• Professional uninstaller" -ForegroundColor White
Write-Host "• End User License Agreement" -ForegroundColor White
Write-Host "• Version information and branding" -ForegroundColor White
Write-Host ""
Write-Host "Ready for Distribution:" -ForegroundColor Green
Write-Host "• Users can run directly on any Windows 10+ system" -ForegroundColor White
Write-Host "• No Python installation required by end users" -ForegroundColor White
Write-Host "• Professional installation experience" -ForegroundColor White
Write-Host "• Publisher: $Publisher branding throughout" -ForegroundColor White
Write-Host ""

# Offer to open output directory
$openDir = Read-Host "Open output directory? (y/n)"
if ($openDir -eq 'y' -or $openDir -eq 'Y') {
    Invoke-Item $OutputDir
}

Write-Host "Build completed successfully! 🎉" -ForegroundColor Green