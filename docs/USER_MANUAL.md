# ScrewVina User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Project Setup](#project-setup)
5. [Configuration Files](#configuration-files)
6. [Running Docking](#running-docking)
7. [Analyzing Results](#analyzing-results)
8. [Understanding Output](#understanding-output)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)

---

## Introduction

ScrewVina is a modular Python package for automated high-throughput molecular docking using AutoDock Vina. It simplifies the process of docking multiple ligands against multiple receptors and provides automatic statistical analysis of results.

### Key Features

- **Automated workflow** - Set up once, run everything
- **Parallel execution** - Utilize multiple CPU cores efficiently
- **Automatic analysis** - Statistical summaries generated automatically
- **Modular design** - Easy to customize and extend
- **Production-ready** - Robust error handling and progress tracking

### System Requirements

- **Operating System**: Linux, macOS, or Windows (with WSL2)
- **Python**: 3.9 or higher
- **AutoDock Vina**: Latest version
- **RAM**: Minimum 4 GB (8 GB recommended)
- **Disk Space**: Depends on number of dockings (estimate ~1 MB per docking)

---

## Installation

### Step 1: Install Prerequisites

#### Install Miniconda (if not already installed)

```bash
# Linux/macOS
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Follow prompts and restart terminal
```

#### Clone ScrewVina Repository

```bash
git clone https://github.com/yourusername/ScrewVina.git
cd ScrewVina
```

### Step 2: Create Environment

#### Option A: Using environment.yml (Recommended)

```bash
conda env create -f environment.yml
conda activate screwvina
```

#### Option B: Manual Installation

```bash
# Create environment
conda create -n screwvina python=3.11

# Activate
conda activate screwvina

# Install Vina
conda install -c conda-forge vina
```

### Step 3: Verify Installation

```bash
# Check Python
python --version  # Should show 3.9+

# Check Vina
vina --version    # Should show Vina version

# Test ScrewVina
python screwvina/screwvina.py --help
```

If all commands work, you're ready to go! ✅

---

## Quick Start

### 1. Prepare Your Project Directory

```bash
# Create project structure
mkdir my_docking_project
cd my_docking_project

# Create required directories
mkdir receptors ligands configurations

# Copy or link to ScrewVina
ln -s /path/to/ScrewVina/screwvina screwvina
```

Your structure should look like:
```
my_docking_project/
├── screwvina/          # Symlink or copy of package
├── receptors/          # Your receptor files
├── ligands/            # Your ligand files
└── configurations/     # Your config files
```

### 2. Add Your Files

```bash
# Add receptors (PDBQT format required)
cp /path/to/your/protein.pdbqt receptors/

# Add ligands (PDBQT format required)
cp /path/to/your/ligands/*.pdbqt ligands/

# Create configuration file
cat > configurations/protein.txt << EOF
cpu = 4
scoring = vina
exhaustiveness = 32
seed = 12345
num_modes = 10
energy_range = 3
center_x = 15.0
center_y = 20.0
center_z = 10.0
size_x = 20
size_y = 20
size_z = 20
EOF
```

### 3. Run Docking

```bash
cd screwvina
python screwvina.py dock --jobs 4
```

### 4. View Results

```bash
# Results are in:
ls ../vs_runs/              # Docked structures
cat ../vina_results.tsv     # Analysis summary
```

That's it! 🎉

---

## Project Setup

### Directory Structure

```
your_project/
│
├── screwvina/              # The package (symlink or copy)
│   ├── __init__.py
│   ├── config.py
│   ├── screwvina.py
│   └── ...
│
├── receptors/              # Your receptor structures
│   ├── protein_A.pdbqt
│   ├── protein_B.pdbqt
│   └── ...
│
├── ligands/                # Your ligand structures
│   ├── compound_001.pdbqt
│   ├── compound_002.pdbqt
│   └── ...
│
├── configurations/         # Configuration files
│   ├── protein_A.txt       # Must match receptor name!
│   ├── protein_B.txt
│   └── ...
│
└── vs_runs/                # Output (auto-created)
    ├── vs_protein_A/
    │   ├── compound_001_out.pdbqt
    │   └── logs/
    └── vs_protein_B/
```

### File Naming Convention

**IMPORTANT:** Configuration files must match receptor names!

```
✅ CORRECT:
receptors/my_protein.pdbqt  →  configurations/my_protein.txt

❌ WRONG:
receptors/my_protein.pdbqt  →  configurations/config.txt
```

### File Format Requirements

#### Receptors
- Format: **PDBQT** (prepared for docking)
- Must include hydrogen atoms
- Must have charges assigned
- Use AutoDock Tools or similar to prepare

#### Ligands
- Format: **PDBQT** (prepared for docking)
- Must include hydrogen atoms
- Must have rotatable bonds defined
- Use AutoDock Tools or similar to prepare

#### Configurations
- Format: Plain text (`.txt`, `.conf`, or `.vina.conf`)
- One file per receptor
- Contains docking box parameters

---

## Configuration Files

### Required Parameters

```
# Computational settings
cpu = 4                    # Number of CPU cores (recommended: 2-8)
scoring = vina             # Scoring function (usually "vina")
exhaustiveness = 32        # Search effort (8=fast, 32=thorough, 64=very thorough)
seed = 12345               # Random seed (for reproducibility)

# Output settings
num_modes = 10             # Number of poses to generate (typically 10-20)
energy_range = 3           # Max energy difference from best pose (kcal/mol)

# Docking box (Angstroms)
center_x = 15.0            # X coordinate of box center
center_y = 20.0            # Y coordinate of box center
center_z = 10.0            # Z coordinate of box center
size_x = 20                # Box size in X dimension
size_y = 20                # Box size in Y dimension
size_z = 20                # Box size in Z dimension
```

### Parameter Guidelines

#### CPU Cores
```
cpu = 4                    # Good for most cases
cpu = 8                    # Better for difficult systems
cpu = 2                    # Use if running many parallel jobs
```

**Tip:** `cpu × jobs` should not exceed your total CPU cores.

Example: 8-core system
- Option 1: `cpu = 4`, `--jobs 2` (2 × 4 = 8 cores used)
- Option 2: `cpu = 2`, `--jobs 4` (4 × 2 = 8 cores used)

#### Exhaustiveness
```
exhaustiveness = 8         # Quick test (~5 min per ligand)
exhaustiveness = 32        # Standard (recommended) (~15 min per ligand)
exhaustiveness = 64        # Thorough (~30 min per ligand)
```

Higher = more accurate but slower.

#### Box Size
```
# General guidelines:
size = 20-25               # Small binding site
size = 25-30               # Medium binding site
size = 30-40               # Large binding site or flexible docking
```

**Tip:** Box should encompass the entire binding site plus ~5-10 Å margin.

### Finding Box Parameters

You can use tools like:
- **PyMOL** - Measure distances, find center
- **Chimera/ChimeraX** - Define box visually
- **AutoDock Tools** - Grid box calculation

Example in PyMOL:
```python
# In PyMOL
select binding_site, resi 100-150
center binding_site
# Note the coordinates shown
```

---

## Running Docking

### Basic Usage

#### Standard Docking (with automatic analysis)
```bash
cd screwvina
python screwvina.py dock --jobs 4
```

This will:
1. ✅ Find all receptors and ligands
2. ✅ Execute docking (4 parallel jobs)
3. ✅ Automatically analyze results
4. ✅ Create `vina_results.tsv`

#### Docking Without Analysis
```bash
python screwvina.py dock --no-analyze --jobs 4
```

Run analysis later:
```bash
python screwvina.py analyze
```

### Command-Line Options

#### `dock` Command

```bash
python screwvina.py dock [OPTIONS]

OPTIONS:
  --vina TEXT        Name or path of Vina executable (default: "vina")
  --jobs INTEGER     Number of parallel jobs (default: 4)
  --no-analyze       Skip automatic analysis after docking
  --help             Show help message
```

**Examples:**

```bash
# Use 8 parallel jobs
python screwvina.py dock --jobs 8

# Specify Vina path
python screwvina.py dock --vina /usr/local/bin/vina --jobs 4

# Dock without analysis
python screwvina.py dock --no-analyze --jobs 4
```

#### `analyze` Command

```bash
python screwvina.py analyze [OPTIONS]

OPTIONS:
  --out TEXT         Output filename (default: "vina_results.tsv")
  --help             Show help message
```

**Examples:**

```bash
# Standard analysis
python screwvina.py analyze

# Custom output name
python screwvina.py analyze --out my_results.tsv
```

### Progress Monitoring

During docking, you'll see:

```
======================================================================
STARTING DOCKING...
======================================================================
Receptors: 3
Ligands: 50
Dockings to perform: 150
Parallel jobs: 4
Output folder: /path/to/vs_runs
======================================================================

Executing 4 docking processes at a time...
Progress: 25/150 (ok=25, errors=0)
Progress: 50/150 (ok=50, errors=0)
Progress: 75/150 (ok=75, errors=0)
...
```

---

## Analyzing Results

### Automatic Analysis

By default, analysis runs automatically after docking:

```bash
python screwvina.py dock --jobs 4
# → Docking runs
# → Analysis runs automatically
# → vina_results.tsv created
```

### Manual Analysis

To analyze existing results:

```bash
python screwvina.py analyze
```

Or with custom output:

```bash
python screwvina.py analyze --out my_analysis.tsv
```

### What Gets Analyzed

For each receptor-ligand pair, ScrewVina calculates:

1. **Average Affinity** - Mean binding energy across all poses
2. **StdDev Affinity** - Standard deviation of binding energies
3. **Average RMSD** - Mean structural deviation between poses
4. **StdDev RMSD** - Standard deviation of RMSD values

---

## Understanding Output

### Output Structure

```
your_project/
├── vs_runs/                          # All docking results
│   ├── vs_protein_A/                 # Results for protein_A
│   │   ├── compound_001_out.pdbqt    # Docked poses
│   │   ├── compound_002_out.pdbqt
│   │   └── logs/                     # Log files
│   │       ├── protein_A_compound_001.log
│   │       └── protein_A_compound_002.log
│   └── vs_protein_B/                 # Results for protein_B
│       └── ...
└── vina_results.tsv                  # Analysis summary
```

### PDBQT Output Files

Each `*_out.pdbqt` file contains:
- Multiple docking poses (typically 10)
- Ranked by binding affinity (best first)
- Each pose is a MODEL in the file

**View with:**
- PyMOL: `load compound_001_out.pdbqt`
- Chimera: File → Open → select file
- Text editor: See coordinates and energies

### Log Files

Each log file contains:
- Docking parameters used
- Binding affinities for all poses
- RMSD values between poses
- Timing information

**Example log excerpt:**
```
mode |   affinity | dist from best mode
     | (kcal/mol) | rmsd l.b.| rmsd u.b.
-----+------------+----------+----------
   1 |       -8.5 |      0.0 |      0.0
   2 |       -8.2 |      1.5 |      2.3
   3 |       -7.9 |      2.1 |      3.5
```

### TSV Analysis File

**Format:**
```
Receptor    Ligand        Avg_Affinity  Std_Dev_Affinity  Avg_RMSD_UB  Std_Dev_RMSD_UB
protein_A   compound_001  -8.500        0.300             1.500        0.400
protein_A   compound_002  -7.200        0.500             2.100        0.600
protein_B   compound_001  -9.100        0.200             1.200        0.300
```

**Interpretation:**

| Column | Meaning | Good Value |
|--------|---------|------------|
| Avg_Affinity | Mean binding energy | More negative = better (e.g., < -8.0) |
| Std_Dev_Affinity | Consistency of binding | Lower = more consistent (< 1.0 good) |
| Avg_RMSD_UB | Pose similarity | Lower = similar poses (< 2.0 good) |
| Std_Dev_RMSD_UB | Variability in poses | Lower = consistent (< 1.0 good) |

**Example interpretation:**
```
protein_A   compound_001  -8.5   0.3   1.5   0.4
```
- ✅ Strong binding (-8.5 kcal/mol)
- ✅ Consistent affinities (StdDev = 0.3)
- ✅ Similar poses (RMSD = 1.5 Å)
- ✅ Good result!

### Opening TSV Files

**Excel:**
1. Open Excel
2. File → Open
3. Select `vina_results.tsv`
4. Data will be in columns

**LibreOffice Calc:**
1. Open Calc
2. File → Open
3. Select `vina_results.tsv`
4. Set delimiter to "Tab"

**Python/Pandas:**
```python
import pandas as pd
df = pd.read_csv("vina_results.tsv", sep="\t")
print(df.head())
```

---

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'config'"

**Problem:** Running from wrong directory

**Solution:**
```bash
cd screwvina
python screwvina.py dock --jobs 4
```

#### 2. "ERROR: No ligand found in /path/to/ligands"

**Problem:** Ligands folder empty or wrong location

**Solution:**
```bash
# Check ligands folder
ls ../ligands/

# Should see .pdbqt files
# If not, add your ligands
```

#### 3. "ERROR: Configuration for 'protein_A' not found"

**Problem:** Configuration file missing or misnamed

**Solution:**
```bash
# Check receptor name
ls ../receptors/
# protein_A.pdbqt

# Configuration must match (without .pdbqt)
ls ../configurations/
# protein_A.txt  ✅

# If missing, create it
nano ../configurations/protein_A.txt
```

#### 4. "ERROR: No vs_* directory found"

**Problem:** Trying to analyze before docking

**Solution:**
```bash
# Run docking first
python screwvina.py dock --jobs 4

# Then analysis will work
python screwvina.py analyze
```

#### 5. Vina Not Found

**Problem:** Vina not in PATH

**Solution:**
```bash
# Activate conda environment
conda activate screwvina

# Verify Vina
which vina

# If not found, install
conda install -c conda-forge vina

# Or specify full path
python screwvina.py dock --vina /full/path/to/vina --jobs 4
```

#### 6. "WARNING: Possible oversubscription"

**Problem:** Requesting more CPU cores than available

**Solution:**
```bash
# Check your CPU cores
nproc  # Linux
sysctl -n hw.ncpu  # macOS

# If you have 8 cores and config has cpu=4:
python screwvina.py dock --jobs 2  # 2×4 = 8 cores ✅

# Not:
python screwvina.py dock --jobs 4  # 4×4 = 16 cores ❌
```

### Performance Issues

#### Docking Too Slow

**Possible causes & solutions:**

1. **Exhaustiveness too high**
   ```
   # In config file, try lower value
   exhaustiveness = 8   # Fast (for testing)
   exhaustiveness = 16  # Medium
   exhaustiveness = 32  # Thorough (default)
   ```

2. **Box too large**
   ```
   # Reduce box size if possible
   size_x = 20  # Instead of 30
   size_y = 20
   size_z = 20
   ```

3. **Not enough parallelism**
   ```bash
   # Use more parallel jobs
   python screwvina.py dock --jobs 8
   ```

#### Out of Memory

**Solutions:**

1. **Reduce parallel jobs**
   ```bash
   python screwvina.py dock --jobs 2
   ```

2. **Reduce CPU per job**
   ```
   # In config file
   cpu = 2  # Instead of 4 or 8
   ```

### Debug Mode

To see more details:

```bash
# Add print statements to code
# Or check log files for errors

# View a log file
cat vs_runs/vs_protein_A/logs/protein_A_ligand1.log
```

---

## FAQ

### General Questions

**Q: How long does docking take?**

A: Depends on:
- Exhaustiveness (8=~5min, 32=~15min, 64=~30min per ligand)
- System size (ligand + box size)
- CPU speed
- Parallel jobs

Typical: 10-20 minutes per ligand with exhaustiveness=32

**Q: Can I stop and resume docking?**

A: Yes! ScrewVina skips already-completed dockings. Just run the same command again.

**Q: How many ligands can I dock?**

A: No limit! Tested with 10,000+ ligands. Just ensure enough disk space (~1 MB per docking).

**Q: Do I need to prepare my structures?**

A: Yes! Receptors and ligands must be in PDBQT format with hydrogens and charges. Use AutoDock Tools or MGLTools.

### Technical Questions

**Q: What Vina parameters does ScrewVina use?**

A: All parameters come from your configuration files. ScrewVina passes:
```bash
vina --receptor X --ligand Y --config Z --out OUT
```

**Q: Can I use different scoring functions?**

A: Yes! In config file:
```
scoring = vina      # Default
scoring = vinardo   # Alternative
scoring = ad4       # AutoDock4 scoring
```

**Q: Can I customize the code?**

A: Absolutely! The modular design makes it easy. See the User Manual section on customization.

**Q: Does it work with Vina 1.2.x?**

A: Yes! Compatible with Vina 1.1.2, 1.2.0, 1.2.3, and later.

**Q: Can I dock covalent ligands?**

A: No, standard Vina doesn't support covalent docking. Consider CovDock or other specialized tools.

### Results Questions

**Q: What's a good binding affinity?**

A: Generally:
- < -7.0 kcal/mol: Promising
- < -8.0 kcal/mol: Good
- < -9.0 kcal/mol: Very good
- < -10.0 kcal/mol: Excellent

But depends on target and context!

**Q: How many poses should I generate?**

A: 
- `num_modes = 10`: Standard (recommended)
- `num_modes = 20`: More thorough
- `num_modes = 3-5`: Quick screening

**Q: What does RMSD mean?**

A: RMSD (Root Mean Square Deviation) measures structural difference between poses. Lower = more similar = more confident in binding mode.

**Q: Should I always take the top-ranked pose?**

A: Usually yes, but always visually inspect! Sometimes pose 2 or 3 makes more chemical sense.

---

## Additional Resources

### Learning Materials

- [AutoDock Vina Documentation](http://vina.scripps.edu/)
- [AutoDock Tools Tutorial](http://autodock.scripps.edu/faqs-help/tutorial)
- [Molecular Docking Guide](https://www.nature.com/articles/nprot.2016.051)

### File Preparation

- [Open Babel](http://openbabel.org/) - Format conversion
- [AutoDock Tools](http://autodock.scripps.edu/resources/adt) - PDBQT preparation
- [PyMOL](https://pymol.org/) - Visualization
- [Chimera](https://www.cgl.ucsf.edu/chimera/) - Structure preparation

### Getting Help

- **Issues**: https://github.com/yourusername/ScrewVina/issues
- **Email**: your.email@domain.com
- **Documentation**: https://github.com/yourusername/ScrewVina/docs

---

**Last Updated**: January 2025  
**Version**: 1.0.0

