# ScrewVina: Automated ensemble docking and virtual screening with AutoDock-Vina

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- 🔓 **Easy to access** - Extremely simplified code architecture and syntax for everyone
- ⚡ **Highly versatile** - Test as many compounds and receptors as you like
- 📊 **Automatic analysis** - Statistical summary with TSV output

## 🎯 Quick Start
```bash
# 1. Clone repository
git clone https://github.com/yourusername/ScrewVina.git
cd ScrewVina

# 2. Setup environment
conda env create -f environment.yml
conda activate screwvina

# 3. Run example (Required directories: configurations/, receptors/, ligands/)
bash run_example.sh

# 4. Check results
cat vina_results.tsv
```

## 📦 Installation

### Prerequisites
- Python 3.9+
- AutoDock Vina
- Conda (recommended)

### Option 1: Conda (Recommended)
```bash
conda env create -f environment.yml
conda activate screwvina
```

### Option 2: Pip + Manual Vina Installation
```bash
pip install -r requirements.txt
# Then install Vina separately:
# conda install -c conda-forge vina
```

## 🚀 Usage

### As Command-Line Tool
```bash
cd screwvina

# Run docking with automatic analysis (auto-detects optimal parallel jobs)
python screwvina.py dock

# Run docking with specific number of jobs
python screwvina.py dock --jobs 4

# Run analysis only
python screwvina.py analyze --out my_results.tsv

# Dock without analysis
python screwvina.py dock --no-analyze --jobs 4

# Use a global configuration file (useful for ensemble docking)
python screwvina.py dock --global-config configurations/global.txt

# Help
python screwvina.py --help
```

### As Python Library
```python
from screwvina.docking import vina_docking
from screwvina.analysis import analyze_results

# Run docking (automatically calculates optimal jobs)
vina_docking(vina_exe="vina")

# Run docking with specific settings
vina_docking(vina_exe="vina", num_jobs=4, global_config="configurations/global.txt")

# Analyze results
analyze_results(output_filename="results.tsv")
```

## 📁 Project Structure
```
your_project/
├── screwvina/          # Package (put it here or in Python path)
├── receptors/          # Your receptor PDBQT files
├── ligands/            # Your ligand PDBQT files
├── configurations/     # Config files (one per receptor), or global file for multiple conformations
└── vs_runs/            # Output directory (auto-created)
```

### Configuration File Format

Each receptor needs a matching configuration file:
```
# example_receptor_1.txt

cpu = 4
scoring = vina
exhaustiveness = 32
seed = 12345
num_modes = 10
energy_range = 3

# Docking box
center_x = 15.0
center_y = 20.0
center_z = 10.0
size_x = 20
size_y = 20
size_z = 20
```

### Global Configuration 

For ensemble docking with multiple receptor conformers sharing the same docking box, you can use a global configuration file:

```bash
# Use the same config for all receptors that don't have a specific config
python screwvina.py dock --global-config configurations/default_box.txt
```

The priority is: receptor-specific config → global config → error if neither exists.

### Smart Resource Management

ScrewVina automatically manages CPU resources to prevent system overload:

- **Automatic job calculation**: If you don't specify `--jobs`, the optimal number is calculated based on your system cores and the CPU setting in your config files
- **Overload warning**: If you manually set `--jobs` too high, you'll get a warning about potential thrashing
- **Example**: On an 8-core system with `cpu = 4` in config:
  - Auto-calculated jobs: 2 (using all 8 cores efficiently)
  - Setting `--jobs 8` would create 32 threads (overload warning)

## 📊 Output

### Docked Structures
```
vs_runs/
├── vs_receptor_1/
│   ├── ligand_1_out.pdbqt
│   ├── ligand_2_out.pdbqt
│   └── logs/
│       ├── receptor_1_ligand_1.log
│       └── receptor_1_ligand_2.log
```

### Analysis Report (TSV)
```
Receptor    Ligand      Best_Affinity  Avg_Affinity  Std_Dev_Affinity  Avg_RMSD_UB  Std_Dev_RMSD_UB
receptor_1  ligand_1    -9.2           -8.500        0.300             1.500        0.400
receptor_1  ligand_2    -7.8           -7.200        0.500             2.100        0.600
```

The analysis includes:
- **Best_Affinity**: The best (most negative) binding affinity from mode 1
- **Avg_Affinity**: Average binding affinity across all modes
- **Std_Dev_Affinity**: Standard deviation of binding affinities
- **Avg_RMSD_UB**: Average RMSD upper bound (excluding mode 1)
- **Std_Dev_RMSD_UB**: Standard deviation of RMSD values

## 📖 Documentation

- [User Manual](docs/USER_MANUAL.md) - Complete guide
- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [API Reference](docs/API_REFERENCE.md) - Module documentation

# 🧩 Module Architecture
```
┌─────────────┐
│screwvina.py │  ← CLI Interface
└──────┬──────┘
       │
   ┌───┴────┐
   ↓        ↓
┌─────┐  ┌────────┐
│dock │  │analysis│  ← Coordinators
└──┬──┘  └───┬────┘
   │         │
   ↓         ↓
 [file_utils, vina_execution, log_reading]  ← Workers
   │
   ↓
 [config]  ← Base configuration
```

Each module has a single, clear responsibility. See [docs/USER_MANUAL.md](docs/USER_MANUAL.md) for details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

- **Author**: Serena Francisco
- **Email**: serena.francisco@unito.it
- **GitHub**: [@serenafrancisco](https://github.com/serenafrancisco)
- **Institution**: University of Turin

## 🙏 Acknowledgments

- [J. Eberhardt, D. Santos-Martins, A. F. Tillack, and S. Forli. (2021). AutoDock Vina 1.2.0: New Docking Methods, Expanded Force Field, and Python Bindings. Journal of Chemical Information and Modeling.](https://pubs.acs.org/doi/10.1021/acs.jcim.1c00203)
- [MedChemBeyond Lab](https://www.cassmedchem.unito.it/node/1) at the University of Turin 
