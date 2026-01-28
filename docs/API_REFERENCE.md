# ScrewVina API Reference

Complete reference for all modules, functions, and classes in ScrewVina.

---

## Table of Contents

1. [Module Overview](#module-overview)
2. [config.py](#configpy)
3. [file_utils.py](#file_utilspy)
4. [vina_execution.py](#vina_executionpy)
5. [docking.py](#dockingpy)
6. [log_reading.py](#log_readingpy)
7. [analysis.py](#analysispy)
8. [screwvina.py](#screwvinapy)
9. [Usage Examples](#usage-examples)

---

## Module Overview

### Architecture

```
screwvina/
├── config.py          # Configuration and paths
├── file_utils.py      # File discovery and management
├── vina_execution.py  # Vina execution
├── docking.py         # Docking workflow
├── log_reading.py     # Log file parsing
├── analysis.py        # Results analysis
└── screwvina.py       # CLI interface
```

### Dependencies

```
config.py           (no dependencies)
    ↓
file_utils.py      (uses config)
    ↓
vina_execution.py  (standalone)
    ↓
docking.py         (uses config, file_utils, vina_execution)

log_reading.py     (standalone)
    ↓
analysis.py        (uses config, log_reading)

screwvina.py       (uses docking, analysis)
```

---

## config.py

Configuration module containing all folder paths and global variables.

### Variables

#### `script_folder`
```python
script_folder: Path
```
Path to the directory containing the screwvina package.

**Example:**
```python
from config import script_folder
print(script_folder)  # /path/to/screwvina_modular_exact/
```

#### `project_folder`
```python
project_folder: Path
```
Parent directory of script_folder (where user data is stored).

**Example:**
```python
from config import project_folder
print(project_folder)  # /path/to/your_project/
```

#### `receptors_folder`
```python
receptors_folder: Path
```
Path to receptors directory.

**Default:** `project_folder / "receptors"`

#### `ligands_folder`
```python
ligands_folder: Path
```
Path to ligands directory.

**Default:** `project_folder / "ligands"`

#### `configurations_folder`
```python
configurations_folder: Path
```
Path to configurations directory.

**Default:** `project_folder / "configurations"`

#### `results_folder`
```python
results_folder: Path
```
Path to results directory.

**Default:** `project_folder / "vs_runs"`

### Usage

```python
from config import receptors_folder, ligands_folder

# Use paths
print(f"Looking for receptors in: {receptors_folder}")
print(f"Looking for ligands in: {ligands_folder}")
```

---

## file_utils.py

File discovery and management utilities.

### Functions

#### `find_pdbqt(folder)`
```python
def find_pdbqt(folder: Path) -> List[Path]
```

Find all PDBQT files in a directory.

**Parameters:**
- `folder` (Path): Directory to search

**Returns:**
- `List[Path]`: Sorted list of PDBQT file paths

**Example:**
```python
from pathlib import Path
from file_utils import find_pdbqt

ligands = find_pdbqt(Path("ligands"))
print(f"Found {len(ligands)} ligands")
for lig in ligands:
    print(f"  - {lig.name}")
```

**Notes:**
- Returns empty list if folder doesn't exist
- Files are sorted alphabetically
- Only finds `.pdbqt` extension (case-sensitive)

---

#### `find_configuration(receptor_name)`
```python
def find_configuration(receptor_name: str) -> Path
```

Find configuration file matching a receptor name.

**Parameters:**
- `receptor_name` (str): Receptor name without extension

**Returns:**
- `Path`: Path to configuration file

**Raises:**
- `FileNotFoundError`: If no matching configuration found

**Example:**
```python
from file_utils import find_configuration

# For receptor: receptors/protein_A.pdbqt
config = find_configuration("protein_A")
print(config)  # configurations/protein_A.txt
```

**Notes:**
- Searches for extensions: `.txt`, `.conf`, `.vina.conf`
- Must match receptor stem (filename without extension)
- Raises error with list of attempted paths if not found

---

## vina_execution.py

Vina execution module.

### Functions

#### `vina_execution(...)`
```python
def vina_execution(
    receptor_path: Path,
    ligand_path: Path,
    config_path: Path,
    output_pdbqt: Path,
    output_log: Path,
    vina_exe: str
) -> int
```

Execute a single AutoDock Vina docking.

**Parameters:**
- `receptor_path` (Path): Path to receptor PDBQT file
- `ligand_path` (Path): Path to ligand PDBQT file
- `config_path` (Path): Path to configuration file
- `output_pdbqt` (Path): Where to save docked poses
- `output_log` (Path): Where to save log file
- `vina_exe` (str): Vina executable name or path

**Returns:**
- `int`: Return code (0 = success, non-zero = error)

**Example:**
```python
from pathlib import Path
from vina_execution import vina_execution

return_code = vina_execution(
    receptor_path=Path("receptors/protein.pdbqt"),
    ligand_path=Path("ligands/ligand1.pdbqt"),
    config_path=Path("configurations/protein.txt"),
    output_pdbqt=Path("output/ligand1_out.pdbqt"),
    output_log=Path("output/logs/protein_ligand1.log"),
    vina_exe="vina"
)

if return_code == 0:
    print("Docking successful!")
else:
    print(f"Docking failed with code {return_code}")
```

**Notes:**
- Creates output directories if they don't exist
- Captures both stdout and stderr to log file
- Runs synchronously (blocks until complete)

---

## docking.py

Main docking workflow coordination.

### Functions

#### `vina_docking(...)`
```python
def vina_docking(
    vina_exe: str = "vina",
    num_jobs: int = 4
) -> None
```

Perform complete virtual screening workflow.

**Parameters:**
- `vina_exe` (str, optional): Vina executable. Default: `"vina"`
- `num_jobs` (int, optional): Number of parallel jobs. Default: `4`

**Returns:**
- `None`

**Example:**
```python
from docking import vina_docking

# Standard usage
vina_docking(vina_exe="vina", num_jobs=4)

# Custom Vina path
vina_docking(vina_exe="/usr/local/bin/vina", num_jobs=8)

# Serial execution
vina_docking(vina_exe="vina", num_jobs=1)
```

**Process:**
1. Find all receptors and ligands
2. Match receptors with configuration files
3. Create list of docking tasks
4. Skip already-completed tasks
5. Execute tasks (serial or parallel)
6. Report progress and results

**Notes:**
- Automatically skips completed dockings
- Progress reported every 25 tasks
- Serial mode if `num_jobs == 1`, otherwise parallel
- Returns early if no tasks to perform

---

## log_reading.py

Vina log file parsing module.

### Functions

#### `read_vina_log(log_path)`
```python
def read_vina_log(log_path: Path) -> Tuple[List[float], List[float]]
```

Parse a Vina log file to extract results.

**Parameters:**
- `log_path` (Path): Path to Vina log file

**Returns:**
- `Tuple[List[float], List[float]]`: (affinities, rmsd_values)
  - `affinities`: List of binding affinities (kcal/mol)
  - `rmsd_values`: List of RMSD upper bound values (Angstroms)

**Example:**
```python
from pathlib import Path
from log_reading import read_vina_log

affinities, rmsds = read_vina_log(
    Path("vs_runs/vs_protein/logs/protein_ligand1.log")
)

print(f"Number of poses: {len(affinities)}")
print(f"Best affinity: {min(affinities):.2f} kcal/mol")
print(f"Affinities: {affinities}")
print(f"RMSDs: {rmsds}")
```

**Output Format:**
```python
# Example output:
affinities = [-8.5, -8.2, -7.9, -7.5, ...]  # 10 values
rmsds = [0.0, 1.5, 2.3, 3.1, ...]           # 10 values
```

**Notes:**
- Returns empty lists if log parsing fails
- Affinities: more negative = better binding
- First RMSD value is always 0.0 (reference pose)
- Parses Vina output table format

---

## analysis.py

Results analysis and statistical processing.

### Functions

#### `analyze_results(...)`
```python
def analyze_results(output_filename: str = "vina_results.tsv") -> None
```

Analyze all docking results and create summary report.

**Parameters:**
- `output_filename` (str, optional): Output TSV filename. Default: `"vina_results.tsv"`

**Returns:**
- `None`

**Example:**
```python
from analysis import analyze_results

# Standard analysis
analyze_results()

# Custom output name
analyze_results(output_filename="my_results.tsv")
```

**Process:**
1. Find all `vs_*` directories in results folder
2. Parse all log files using `read_vina_log()`
3. Calculate statistics (mean, stdev) for each pair
4. Write TSV file with results
5. Print summary

**Output Format:**
```
Receptor    Ligand      Avg_Affinity  Std_Dev_Affinity  Avg_RMSD_UB  Std_Dev_RMSD_UB
protein_A   ligand_1    -8.500        0.300             1.500        0.400
protein_A   ligand_2    -7.200        0.500             2.100        0.600
```

**Statistics Calculated:**
- **Avg_Affinity**: Mean of all affinity values
- **Std_Dev_Affinity**: Standard deviation of affinities
- **Avg_RMSD_UB**: Mean RMSD (excluding first pose)
- **Std_Dev_RMSD_UB**: Standard deviation of RMSDs

**Notes:**
- Creates file in `project_folder`
- Tab-separated values (TSV) format
- Skips pairs with no valid data
- Values formatted to 3 decimal places

---

## screwvina.py

Command-line interface module.

### Functions

#### `main()`
```python
def main() -> int
```

Main entry point for CLI.

**Parameters:**
- None (uses `sys.argv`)

**Returns:**
- `int`: Exit code (0 = success, 1 = error)

**Usage:**
```bash
# From command line:
python screwvina.py dock --jobs 4
python screwvina.py analyze --out results.tsv
python screwvina.py --help
```

**From Python:**
```python
from screwvina import main
import sys

# Simulate command-line arguments
sys.argv = ["screwvina.py", "dock", "--jobs", "4"]
exit_code = main()
```

### Command-Line Interface

#### `dock` Command

```bash
python screwvina.py dock [OPTIONS]
```

**Options:**
- `--vina TEXT`: Vina executable (default: "vina")
- `--jobs INTEGER`: Number of parallel jobs (default: 4)
- `--no-analyze`: Skip automatic analysis
- `--help`: Show help message

**Examples:**
```bash
# Standard docking
python screwvina.py dock --jobs 4

# Custom Vina path
python screwvina.py dock --vina /usr/local/bin/vina

# Without analysis
python screwvina.py dock --no-analyze --jobs 8
```

#### `analyze` Command

```bash
python screwvina.py analyze [OPTIONS]
```

**Options:**
- `--out TEXT`: Output filename (default: "vina_results.tsv")
- `--help`: Show help message

**Examples:**
```bash
# Standard analysis
python screwvina.py analyze

# Custom output
python screwvina.py analyze --out my_results.tsv
```

---

## Usage Examples

### Example 1: Simple Docking

```python
# simple_docking.py
from docking import vina_docking
from analysis import analyze_results

# Run docking
print("Starting docking...")
vina_docking(vina_exe="vina", num_jobs=4)

# Analyze
print("Analyzing results...")
analyze_results(output_filename="results.tsv")

print("Done!")
```

### Example 2: Custom File Discovery

```python
# custom_discovery.py
from pathlib import Path
from file_utils import find_pdbqt, find_configuration

# Find all ligands
ligands_dir = Path("my_ligands")
ligands = find_pdbqt(ligands_dir)

print(f"Found {len(ligands)} ligands:")
for lig in ligands:
    print(f"  - {lig.name}")

# Find configurations
receptors_dir = Path("my_receptors")
receptors = find_pdbqt(receptors_dir)

for rec in receptors:
    try:
        config = find_configuration(rec.stem)
        print(f"{rec.name} → {config.name}")
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
```

### Example 3: Manual Single Docking

```python
# manual_docking.py
from pathlib import Path
from vina_execution import vina_execution

# Setup paths
receptor = Path("receptors/protein_A.pdbqt")
ligand = Path("ligands/compound_1.pdbqt")
config = Path("configurations/protein_A.txt")
output = Path("output/compound_1_out.pdbqt")
log = Path("output/logs/protein_A_compound_1.log")

# Execute docking
print("Running docking...")
return_code = vina_execution(
    receptor_path=receptor,
    ligand_path=ligand,
    config_path=config,
    output_pdbqt=output,
    output_log=log,
    vina_exe="vina"
)

if return_code == 0:
    print("✅ Docking successful!")
    print(f"Output: {output}")
    print(f"Log: {log}")
else:
    print(f"❌ Docking failed with code {return_code}")
```

### Example 4: Parse and Filter Results

```python
# filter_results.py
from pathlib import Path
from log_reading import read_vina_log

# Find all log files
logs_dir = Path("vs_runs/vs_protein_A/logs")

strong_binders = []

for log_file in logs_dir.glob("*.log"):
    affinities, rmsds = read_vina_log(log_file)
    
    if not affinities:
        continue
    
    best_affinity = min(affinities)
    
    # Filter: affinity < -8.0 kcal/mol
    if best_affinity < -8.0:
        ligand_name = log_file.stem.split("_")[-1]
        strong_binders.append({
            "ligand": ligand_name,
            "affinity": best_affinity
        })

# Sort by affinity
strong_binders.sort(key=lambda x: x["affinity"])

# Print results
print(f"Found {len(strong_binders)} strong binders:")
for item in strong_binders:
    print(f"  {item['ligand']}: {item['affinity']:.2f} kcal/mol")
```

### Example 5: Batch Processing

```python
# batch_processing.py
import subprocess
from pathlib import Path

# Define multiple receptor sets
receptor_sets = [
    {"name": "kinases", "path": "data/kinases"},
    {"name": "proteases", "path": "data/proteases"},
    {"name": "gpcrs", "path": "data/gpcrs"}
]

for rset in receptor_sets:
    print(f"\n{'='*60}")
    print(f"Processing: {rset['name']}")
    print('='*60)
    
    # Change to set directory
    work_dir = Path(rset['path'])
    
    # Run docking
    cmd = [
        "python", 
        "../screwvina/screwvina.py",
        "dock",
        "--jobs", "4"
    ]
    
    result = subprocess.run(
        cmd,
        cwd=work_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ {rset['name']} completed successfully")
    else:
        print(f"❌ {rset['name']} failed")
        print(result.stderr)

print("\n" + "="*60)
print("All sets completed!")
print("="*60)
```

### Example 6: Progress Callback

```python
# progress_callback.py
from pathlib import Path
from file_utils import find_pdbqt, find_configuration
from vina_execution import vina_execution

# Setup
receptors = find_pdbqt(Path("receptors"))
ligands = find_pdbqt(Path("ligands"))

total = len(receptors) * len(ligands)
completed = 0

print(f"Total dockings: {total}")

for receptor in receptors:
    config = find_configuration(receptor.stem)
    
    for ligand in ligands:
        # Setup output paths
        output_dir = Path(f"output/vs_{receptor.stem}")
        output_pdbqt = output_dir / f"{ligand.stem}_out.pdbqt"
        output_log = output_dir / "logs" / f"{receptor.stem}_{ligand.stem}.log"
        
        # Skip if exists
        if output_pdbqt.exists() and output_log.exists():
            completed += 1
            continue
        
        # Execute
        code = vina_execution(
            receptor, ligand, config,
            output_pdbqt, output_log,
            "vina"
        )
        
        completed += 1
        
        # Progress
        progress = (completed / total) * 100
        print(f"Progress: {completed}/{total} ({progress:.1f}%)")

print("Complete!")
```

---

## Type Hints Reference

### Common Types

```python
from pathlib import Path
from typing import List, Tuple, Dict, Optional

# Path to file or directory
Path

# List of paths
List[Path]

# Tuple of two lists
Tuple[List[float], List[float]]

# Dictionary
Dict[str, any]

# Optional value
Optional[str]
```

---

## Error Handling

### Common Exceptions

```python
# FileNotFoundError
try:
    config = find_configuration("nonexistent")
except FileNotFoundError as e:
    print(f"Config not found: {e}")

# General exceptions
try:
    vina_docking(vina_exe="vina", num_jobs=4)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

---

## Best Practices

### 1. Always Use Path Objects

```python
# ✅ Good
from pathlib import Path
receptor = Path("receptors/protein.pdbqt")

# ❌ Avoid
receptor = "receptors/protein.pdbqt"
```

### 2. Check File Existence

```python
from pathlib import Path

ligands_dir = Path("ligands")
if not ligands_dir.exists():
    print(f"ERROR: {ligands_dir} does not exist")
    exit(1)
```

### 3. Handle Errors Gracefully

```python
try:
    config = find_configuration(receptor_name)
except FileNotFoundError:
    print(f"Skipping {receptor_name}: no config found")
    continue
```

### 4. Use Context Managers

```python
# ✅ Good (automatic file closing)
with open(log_file, "w") as f:
    f.write("data")

# ❌ Avoid (manual closing)
f = open(log_file, "w")
f.write("data")
f.close()
```

---

**Last Updated**: January 2025  
**Version**: 1.0.0
