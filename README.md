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

# 3. Run example
cd examples
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

# Run docking with automatic analysis
python screwvina.py dock --jobs 4

# Run analysis only
python screwvina.py analyze --out my_results.tsv

# Dock without analysis
python screwvina.py dock --no-analyze --jobs 4

# Help
python screwvina.py --help
```

### As Python Library
```python
from screwvina.docking import vina_docking
from screwvina.analysis import analyze_results

# Run docking
vina_docking(vina_exe="vina", num_jobs=4)

# Analyze results
analyze_results(output_filename="results.tsv")
```

## 📁 Project Structure
```
your_project/
├── screwvina/          # Package (put it here or in Python path)
├── receptors/          # Your receptor PDBQT files
├── ligands/            # Your ligand PDBQT files
├── configurations/     # Config files (one per receptor)
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
Receptor    Ligand      Avg_Affinity  Std_Dev_Affinity  Avg_RMSD_UB  Std_Dev_RMSD_UB
receptor_1  ligand_1    -8.500        0.300             1.500        0.400
receptor_1  ligand_2    -7.200        0.500             2.100        0.600
```

## 📖 Documentation

- [User Manual](docs/USER_MANUAL.md) - Complete guide
- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [API Reference](docs/API_REFERENCE.md) - Module documentation

## 🧪 Examples

See the [`examples/`](examples/) directory for working examples:
```bash
cd examples
bash run_example.sh
```

This will dock 30 example ligands against 2 example receptors.

## 🧩 Module Architecture
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

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

- **Author**: Serena Francisco
- **Email**: serena.francisco@unito.it
- **GitHub**: [@serenafrancisco](https://github.com/serenafrancisco)
- **Institution**: University of Turin

## 🙏 Acknowledgments

- AutoDock Vina team for the docking software
- [List other acknowledgments]

```

## ⭐ Star History

If you find this useful, please consider giving it a star! ⭐

