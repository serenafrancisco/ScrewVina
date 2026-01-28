# ScrewVina Installation Guide

Complete installation instructions for ScrewVina on different platforms.

---

## Table of Contents

1. [Quick Install](#quick-install)
2. [Detailed Installation](#detailed-installation)
3. [Platform-Specific Instructions](#platform-specific-instructions)
4. [Troubleshooting Installation](#troubleshooting-installation)
5. [Verification](#verification)
6. [Updating](#updating)

---

## Quick Install

### For Linux/macOS Users

```bash
# 1. Clone repository
git clone https://github.com/yourusername/ScrewVina.git
cd ScrewVina

# 2. Create conda environment
conda env create -f environment.yml

# 3. Activate environment
conda activate screwvina

# 4. Test
cd screwvina
python screwvina.py --help
```

Done! ✅

---

## Detailed Installation

### Prerequisites

Before installing ScrewVina, ensure you have:

- **Git** (to clone repository)
- **Conda** or **Miniconda** (to manage environment)
- **5 GB disk space** (for conda environment)
- **Internet connection** (for downloading packages)

### Step 1: Install Conda (if needed)

#### Linux

```bash
# Download Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install
bash Miniconda3-latest-Linux-x86_64.sh

# Follow prompts:
# - Accept license: yes
# - Install location: default
# - Initialize conda: yes

# Restart terminal
source ~/.bashrc

# Verify
conda --version
```

#### macOS

```bash
# Download Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

# Install
bash Miniconda3-latest-MacOSX-x86_64.sh

# Follow prompts (same as Linux)

# Restart terminal
source ~/.bash_profile  # or ~/.zshrc for zsh

# Verify
conda --version
```

#### Windows

1. Download: https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
2. Run installer
3. Follow prompts (accept defaults)
4. Open "Anaconda Prompt" from Start Menu

### Step 2: Install Git (if needed)

#### Linux

```bash
# Ubuntu/Debian
sudo apt-get install git

# Fedora/RHEL
sudo dnf install git

# Verify
git --version
```

#### macOS

```bash
# Using Homebrew (install Homebrew first if needed)
brew install git

# Or download from: https://git-scm.com/download/mac

# Verify
git --version
```

#### Windows

Download and install from: https://git-scm.com/download/win

### Step 3: Clone ScrewVina

```bash
# Navigate to where you want to install
cd ~/Projects  # or any directory

# Clone repository
git clone https://github.com/yourusername/ScrewVina.git

# Enter directory
cd ScrewVina

# Check contents
ls -la
```

You should see:
```
.
├── README.md
├── environment.yml
├── screwvina/
├── examples/
└── docs/
```

### Step 4: Create Conda Environment

#### Option A: Using environment.yml (Recommended)

```bash
# Create environment from file
conda env create -f environment.yml

# This will:
# - Create environment named "screwvina"
# - Install Python 3.11
# - Install AutoDock Vina
# - Install all dependencies
```

#### Option B: Manual Creation

```bash
# Create environment
conda create -n screwvina python=3.11 -y

# Activate
conda activate screwvina

# Install Vina
conda install -c conda-forge vina -y
```

### Step 5: Activate Environment

```bash
conda activate screwvina

# Your prompt should change to show (screwvina)
# Example: (screwvina) user@computer:~$
```

**Important:** Always activate this environment before using ScrewVina!

### Step 6: Verify Installation

```bash
# Check Python
python --version
# Expected: Python 3.11.x or 3.9+

# Check Vina
vina --version
# Expected: AutoDock Vina v1.2.x

# Check ScrewVina
cd screwvina
python screwvina.py --help
# Expected: Help message displayed
```

If all commands work without errors, installation is complete! ✅

---

## Platform-Specific Instructions

### Linux

#### Ubuntu/Debian

```bash
# 1. Install prerequisites
sudo apt-get update
sudo apt-get install -y git wget

# 2. Install Miniconda (if not installed)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 3. Install ScrewVina
git clone https://github.com/yourusername/ScrewVina.git
cd ScrewVina
conda env create -f environment.yml
conda activate screwvina
```

#### Fedora/RHEL/CentOS

```bash
# 1. Install prerequisites
sudo dnf install -y git wget

# 2. Install Miniconda (if not installed)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 3. Install ScrewVina
git clone https://github.com/yourusername/ScrewVina.git
cd ScrewVina
conda env create -f environment.yml
conda activate screwvina
```

### macOS

#### Intel Macs

```bash
# 1. Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Git
brew install git

# 3. Install Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh -b -p $HOME/miniconda3
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 4. Install ScrewVina
git clone https://github.com/yourusername/ScrewVina.git
cd ScrewVina
conda env create -f environment.yml
conda activate screwvina
```

#### Apple Silicon (M1/M2) Macs

```bash
# Same as Intel, but ensure you have Rosetta 2 installed
# Or use native ARM build of Miniconda:
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh -b -p $HOME/miniconda3

# Continue with same steps as Intel
```

### Windows (WSL2)

**Recommended:** Use WSL2 (Windows Subsystem for Linux)

```bash
# 1. Install WSL2 (in PowerShell as Administrator)
wsl --install

# 2. Restart computer

# 3. Open Ubuntu (from Start Menu)

# 4. Inside Ubuntu, follow Linux instructions:
sudo apt-get update
sudo apt-get install -y git wget
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# ... continue with Linux steps
```

### Windows (Native - Not Recommended)

While possible, native Windows installation has limitations. WSL2 is strongly recommended.

If you must use native Windows:

```powershell
# 1. Install Git for Windows
# Download from: https://git-scm.com/download/win

# 2. Install Miniconda
# Download from: https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
# Run installer

# 3. Open "Anaconda Prompt"
# Clone and install
git clone https://github.com/yourusername/ScrewVina.git
cd ScrewVina
conda env create -f environment.yml
conda activate screwvina
```

---

## Troubleshooting Installation

### Issue: "conda: command not found"

**Problem:** Conda not in PATH

**Solution:**

```bash
# Find conda installation
find ~ -name "conda" 2>/dev/null

# Add to PATH (adjust path as needed)
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: "git: command not found"

**Problem:** Git not installed

**Solution:**

```bash
# Linux
sudo apt-get install git   # Ubuntu/Debian
sudo dnf install git        # Fedora/RHEL

# macOS
brew install git

# Windows
# Download from: https://git-scm.com/download/win
```

### Issue: "Solving environment: failed"

**Problem:** Conda package conflicts

**Solution:**

```bash
# Update conda
conda update -n base conda

# Clear cache
conda clean --all

# Try again
conda env create -f environment.yml
```

### Issue: "CondaHTTPError"

**Problem:** Network/proxy issues

**Solution:**

```bash
# Configure proxy (if behind firewall)
conda config --set proxy_servers.http http://proxy.example.com:8080
conda config --set proxy_servers.https https://proxy.example.com:8080

# Or use different channel
conda config --add channels conda-forge
conda config --set channel_priority strict
```

### Issue: "Package not found: vina"

**Problem:** Vina not available in default channels

**Solution:**

```bash
# Explicitly add conda-forge channel
conda install -c conda-forge vina

# Or update environment.yml to specify:
channels:
  - conda-forge
  - defaults
```

### Issue: Environment already exists

**Problem:** Trying to create environment that exists

**Solution:**

```bash
# Remove old environment
conda env remove -n screwvina

# Create fresh
conda env create -f environment.yml
```

---

## Verification

### Complete Verification Checklist

Run these commands to verify everything works:

```bash
# 1. Activate environment
conda activate screwvina

# 2. Check Python
python --version
# Expected: Python 3.11.x or 3.9+

# 3. Check Vina
vina --version
# Expected: AutoDock Vina v1.2.x

which vina
# Expected: /path/to/miniconda3/envs/screwvina/bin/vina

# 4. Test Python imports
python -c "import sys; print(sys.version)"
python -c "from pathlib import Path; print('pathlib ok')"
python -c "import subprocess; print('subprocess ok')"

# 5. Test ScrewVina
cd screwvina
python screwvina.py --help
# Expected: Help message

python screwvina.py dock --help
# Expected: Dock command help

python screwvina.py analyze --help
# Expected: Analyze command help

# 6. Run example (if available)
cd ../examples
bash run_example.sh
# Expected: Example runs without errors
```

### Expected Output Summary

If installation is successful:

```
✅ conda activate screwvina        → (screwvina) prompt
✅ python --version                → Python 3.11.x
✅ vina --version                  → AutoDock Vina v1.2.x
✅ python screwvina.py --help      → Help message
✅ Example runs                     → Completes without error
```

---

## Updating

### Update ScrewVina Code

```bash
cd ScrewVina
git pull origin main
```

### Update Conda Environment

```bash
# Activate environment
conda activate screwvina

# Update packages
conda update --all

# Or recreate environment
conda deactivate
conda env remove -n screwvina
conda env create -f environment.yml
```

### Update Vina

```bash
conda activate screwvina
conda update -c conda-forge vina
```

---

## Uninstallation

### Remove ScrewVina

```bash
# Remove conda environment
conda env remove -n screwvina

# Remove files
rm -rf ~/path/to/ScrewVina
```

### Complete Removal (Including Conda)

```bash
# Remove all conda environments
conda env list  # See all environments
conda env remove -n screwvina
conda env remove -n other_env  # Repeat for all

# Remove Miniconda
rm -rf ~/miniconda3

# Remove from PATH (edit ~/.bashrc or ~/.zshrc)
# Remove line: export PATH="$HOME/miniconda3/bin:$PATH"
```

---

## Advanced Installation Options

### Install in Custom Location

```bash
# Create environment in specific location
conda create --prefix /custom/path/screwvina python=3.11
conda activate /custom/path/screwvina
conda install -c conda-forge vina
```

### Install Without Conda

**Not recommended**, but possible:

```bash
# Ensure Python 3.9+ installed
python3 --version

# Install Vina manually
# Download from: https://github.com/ccsb-scripps/AutoDock-Vina/releases
# Add to PATH

# Clone ScrewVina
git clone https://github.com/yourusername/ScrewVina.git
cd ScrewVina/screwvina

# Use directly
python screwvina.py --help
```

### Development Installation

For development/contribution:

```bash
# Clone repository
git clone https://github.com/yourusername/ScrewVina.git
cd ScrewVina

# Create environment
conda env create -f environment.yml
conda activate screwvina

# Install additional dev tools
conda install pytest black flake8

# Install in editable mode (if using setup.py)
pip install -e .
```

---

## Next Steps

After successful installation:

1. ✅ Read [User Manual](USER_MANUAL.md)
2. ✅ Try examples: `cd examples && bash run_example.sh`
3. ✅ Prepare your data (receptors, ligands, configs)
4. ✅ Run your first docking!

---

## Support

If you encounter issues:

1. Check [Troubleshooting](#troubleshooting-installation)
2. Search [Issues](https://github.com/yourusername/ScrewVina/issues)
3. Create new issue with:
   - Operating system
   - Error message
   - Steps to reproduce

---

**Last Updated**: January 2025  
**Version**: 1.0.0

