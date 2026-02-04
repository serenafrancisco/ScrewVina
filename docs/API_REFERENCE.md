# ScrewVina API Reference

Complete reference for all modules, functions, and classes in ScrewVina.

---

## Table of Contents

1. [Module Overview](#module-overview)
2. [config.py](#configpy)
3. [file_utils.py](#file_utilspy)
4. [cpu_utils.py](#cpu_utilspy)
5. [vina_execution.py](#vina_executionpy)
6. [docking.py](#dockingpy)
7. [log_reading.py](#log_readingpy)
8. [analysis.py](#analysispy)
9. [screwvina.py](#screwvinapy)
10. [Usage Examples](#usage-examples)

---

## Module Overview

### Architecture

```
screwvina/
├── config.py          # Configuration and paths
├── file_utils.py      # File discovery and management
├── cpu_utils.py       # CPU resource management
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
cpu_utils.py       (standalone)
    ↓
vina_execution.py  (standalone)
    ↓
docking.py         (uses config, file_utils, vina_execution, cpu_utils)

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

#### `find_configuration(receptor_name, global_config=None)`
```python
def find_configuration(
    receptor_name: str,
    global_config: Optional[str] = None
) -> Path
```

Find configuration file matching a receptor name, with optional global config fallback.

**Parameters:**
- `receptor_name` (str): Receptor name without extension
- `global_config` (Optional[str]): Path to global/master configuration file

**Returns:**
- `Path`: Path to configuration file

**Raises:**
- `FileNotFoundError`: If no matching configuration found

**Example:**
```python
from file_utils import find_configuration

# Try receptor-specific config first
config = find_configuration("protein_A")
print(config)  # configurations/protein_A.txt

# With global config fallback
config = find_configuration("nmr_conf_001", global_config="configurations/master.txt")
# If nmr_conf_001.txt doesn't exist, uses master.txt
```

**Priority:**
1. Receptor-specific config (e.g., `protein_A.txt`)
2. Global config (if provided)
3. Error if neither exists

**Notes:**
- Searches for extensions: `.txt`
- Must match receptor stem (filename without extension)
- Raises error with helpful message if not found

---

## cpu_utils.py

CPU resource management and validation module.

### Functions

#### `get_system_cores()`
```python
def get_system_cores() -> int
```

Get the number of CPU cores available on the system.

**Returns:**
- `int`: Number of CPU cores

**Example:**
```python
from cpu_utils import get_system_cores

cores = get_system_cores()
print(f"System has {cores} CPU cores")
```

---

#### `read_cpu_from_config(config_path)`
```python
def read_cpu_from_config(config_path: Path) -> int
```

Read the CPU value from a Vina configuration file.

**Parameters:**
- `config_path` (Path): Path to configuration file

**Returns:**
- `int`: Number of CPUs specified in config, or 1 if not found

**Example:**
```python
from pathlib import Path
from cpu_utils import read_cpu_from_config

config = Path("configurations/protein_A.txt")
cpu_value = read_cpu_from_config(config)
print(f"Config specifies {cpu_value} CPUs per job")
```

---

#### `check_cpu_usage(config_cpu, num_jobs, system_cores)`
```python
def check_cpu_usage(
    config_cpu: int, 
    num_jobs: int, 
    system_cores: int
) -> Tuple[bool, Optional[str]]
```

Check if the combination of config CPU and jobs would overload the system.

**Parameters:**
- `config_cpu` (int): CPUs per docking job (from config file)
- `num_jobs` (int): Number of parallel jobs
- `system_cores` (int): Total system cores available

**Returns:**
- `Tuple[bool, Optional[str]]`: (is_ok, warning_message)
  - `is_ok`: True if no overload, False if overload detected
  - `warning_message`: Warning text if overload, None otherwise

**Example:**
```python
from cpu_utils import get_system_cores, check_cpu_usage

system_cores = get_system_cores()  # e.g., 8
config_cpu = 4
num_jobs = 3

is_ok, warning = check_cpu_usage(config_cpu, num_jobs, system_cores)
if not is_ok:
    print(warning)
    # WARNING: Resource overload detected!
    # Config CPU: 4
    # Parallel jobs: 3
    # Total threads: 12
    # System cores: 8
    # ...
```

---

#### `calculate_optimal_jobs(config_cpu, system_cores)`
```python
def calculate_optimal_jobs(config_cpu: int, system_cores: int) -> int
```

Calculate the optimal number of parallel jobs based on config CPU and system cores.

**Parameters:**
- `config_cpu` (int): CPUs per docking job (from config file)
- `system_cores` (int): Total system cores available

**Returns:**
- `int`: Optimal number of parallel jobs (at least 1)

**Example:**
```python
from cpu_utils import get_system_cores, calculate_optimal_jobs

system_cores = get_system_cores()  # 8
config_cpu = 4

optimal = calculate_optimal_jobs(config_cpu, system_cores)
print(f"Optimal jobs: {optimal}")  # 2 (because 8 / 4 = 2)
```

**Algorithm:**
```python
optimal_jobs = system_cores // config_cpu
return max(1, optimal_jobs)  # At least 1 job
```

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

#### `filter_files(...)`
```python
def filter_files(
    files: List[Path],
    name_filter: Optional[List[str]],
    list_file: Optional[str],
    file_type: str
) -> List[Path]
```

Filter files based on name filter or list file.

**Parameters:**
- `files` (List[Path]): List of Path objects to filter
- `name_filter` (Optional[List[str]]): List of filenames (without extension) or None
- `list_file` (Optional[str]): Path to file containing list of names or None
- `file_type` (str): String describing file type (for messages)

**Returns:**
- `List[Path]`: Filtered list of Path objects

**Example:**
```python
from pathlib import Path
from docking import filter_files

all_ligands = [Path("ligands/a.pdbqt"), Path("ligands/b.pdbqt")]
selected = filter_files(all_ligands, ["a"], None, "ligands")
# Returns only ligands/a.pdbqt
```

---

#### `is_valid_output(output_pdbqt, output_log)`
```python
def is_valid_output(output_pdbqt: Path, output_log: Path) -> bool
```

Check if output files exist and are valid (not empty or corrupted).

**Parameters:**
- `output_pdbqt` (Path): Path to output PDBQT file
- `output_log` (Path): Path to output log file

**Returns:**
- `bool`: True if both files exist and are valid, False otherwise

**Example:**
```python
from pathlib import Path
from docking import is_valid_output

valid = is_valid_output(
    Path("vs_runs/vs_protein/ligand_out.pdbqt"),
    Path("vs_runs/vs_protein/logs/protein_ligand.log")
)

if valid:
    print("Output is valid")
else:
    print("Output is missing or corrupted, will re-dock")
```

**Checks:**
- Both files exist
- Both files have size > 0 bytes

---

#### `vina_docking(...)`
```python
def vina_docking(
    vina_exe: str = "vina",
    num_jobs: Optional[int] = None,
    receptor_filter: Optional[List[str]] = None,
    ligand_filter: Optional[List[str]] = None,
    receptor_list_file: Optional[str] = None,
    ligand_list_file: Optional[str] = None,
    global_config: Optional[str] = None
) -> None
```

Perform complete virtual screening workflow with smart resource management.

**Parameters:**
- `vina_exe` (str, optional): Vina executable. Default: `"vina"`
- `num_jobs` (Optional[int], optional): Number of parallel jobs. Default: `None` (auto-calculate)
- `receptor_filter` (Optional[List[str]], optional): List of specific receptor names
- `ligand_filter` (Optional[List[str]], optional): List of specific ligand names
- `receptor_list_file` (Optional[str], optional): File with receptor list
- `ligand_list_file` (Optional[str], optional): File with ligand list
- `global_config` (Optional[str], optional): Global configuration file path

**Returns:**
- `None`

**Example:**
```python
from docking import vina_docking

# Auto-calculate optimal jobs (recommended)
vina_docking()

# Manual jobs
vina_docking(num_jobs=4)

# With global config for ensemble docking
vina_docking(global_config="configurations/master.txt")

# Filter specific receptors/ligands
vina_docking(
    receptor_filter=["protein_A", "protein_B"],
    ligand_filter=["compound_1", "compound_5"],
    num_jobs=2
)

# Use list files
vina_docking(
    receptor_list_file="selected_receptors.txt",
    ligand_list_file="selected_ligands.txt"
)
```

**Process:**
1. Find all receptors and ligands (with optional filtering)
2. Check/calculate optimal CPU jobs
3. Match receptors with configuration files (receptor-specific or global)
4. Create list of docking tasks
5. Skip already-completed tasks (validates file integrity)
6. Execute tasks (serial or parallel)
7. Report progress and results

**Features:**
- **Auto-job calculation**: If `num_jobs=None`, calculates optimal value
- **CPU overload warning**: Warns if `config_cpu × num_jobs > system_cores`
- **Global config support**: Fallback to master config for ensemble docking
- **File validation**: Checks files exist and are not empty before skipping

**Notes:**
- Automatically skips completed dockings with valid outputs
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

Analyze all docking results and create summary report with best affinity tracking.

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
3. Extract best affinity (mode 1) and calculate statistics (mean, stdev)
4. Write TSV file with results including best affinity
5. Print summary

**Output TSV Columns:**
- `Receptor`: Receptor name
- `Ligand`: Ligand name
- **`Best_Affinity`**: Best binding energy from mode 1
- `Avg_Affinity`: Mean of all binding energies
- `Std_Dev_Affinity`: Standard deviation of binding energies
- `Avg_RMSD_UB`: Mean RMSD upper bound (excluding mode 1)
- `Std_Dev_RMSD_UB`: Standard deviation of RMSD values

**Example Output:**
```
Receptor    Ligand      Best_Affinity  Avg_Affinity  Std_Dev_Affinity  Avg_RMSD_UB  Std_Dev_RMSD_UB
protein_A   compound_1  -9.2           -8.500        0.300             1.500        0.400
protein_A   compound_2  -7.8           -7.200        0.500             2.100        0.600
```

**Notes:**
- Best_Affinity is always from mode 1 (top-ranked pose)
- RMSD statistics exclude mode 1 (which has RMSD=0.0)
- Empty log files are skipped
- Progress shown during analysis

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
python screwvina.py dock
python screwvina.py analyze --out results.tsv
python screwvina.py --help
```

**From Python:**
```python
from screwvina import main
import sys

# Simulate command-line arguments
sys.argv = ["screwvina.py", "dock"]
exit_code = main()
```

### Command-Line Interface

#### `dock` Command

```bash
python screwvina.py dock [OPTIONS]
```

**Options:**
- `--vina TEXT`: Vina executable (default: "vina")
- `--jobs INTEGER`: Number of parallel jobs (default: auto-calculated)
- `--no-analyze`: Skip automatic analysis
- `--receptors TEXT [TEXT ...]`: Specific receptors to dock
- `--ligands TEXT [TEXT ...]`: Specific ligands to dock
- `--receptors-list FILE`: File containing receptor list
- `--ligands-list FILE`: File containing ligand list
- `--global-config FILE`: Global configuration file
- `--help`: Show help message

**Examples:**
```bash
# Auto-calculate optimal jobs (recommended)
python screwvina.py dock

# Manual jobs
python screwvina.py dock --jobs 4

# With global config (ensemble docking)
python screwvina.py dock --global-config configurations/master.txt

# Filter specific receptors/ligands
python screwvina.py dock \
    --receptors protein_A protein_B \
    --ligands compound_1 compound_5 \
    --jobs 2

# Use list files
python screwvina.py dock \
    --receptors-list selected_receptors.txt \
    --ligands-list selected_ligands.txt

# Without analysis
python screwvina.py dock --no-analyze
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
vina_docking()

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

### Example 5: Ensemble Docking with Global Config

```python
# ensemble_docking.py
from docking import vina_docking
from analysis import analyze_results

# Dock multiple NMR conformers with single configuration
print("Starting ensemble docking...")
vina_docking(
    global_config="configurations/nmr_docking_box.txt",
    num_jobs=None  # Auto-calculate
)

# Analyze
print("Analyzing ensemble results...")
analyze_results(output_filename="nmr_ensemble_results.tsv")

print("Ensemble docking complete!")
```

### Example 6: CPU-Aware Docking

```python
# cpu_aware_docking.py
from cpu_utils import get_system_cores, calculate_optimal_jobs, read_cpu_from_config
from pathlib import Path
from docking import vina_docking

# Get system info
cores = get_system_cores()
config_cpu = read_cpu_from_config(Path("configurations/protein_A.txt"))
optimal_jobs = calculate_optimal_jobs(config_cpu, cores)

print(f"System cores: {cores}")
print(f"Config CPU: {config_cpu}")
print(f"Optimal jobs: {optimal_jobs}")

# Run with optimal settings
vina_docking(num_jobs=optimal_jobs)
```

### Example 7: Progress Tracking

```python
# progress_tracking.py
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
Optional[int]
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
    vina_docking(vina_exe="vina")
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

### 5. Let ScrewVina Manage Resources

```python
# ✅ Good - auto-calculate jobs
vina_docking()

# ⚠️ Okay - but may need adjustment
vina_docking(num_jobs=4)

# ❌ Risky - may overload system
vina_docking(num_jobs=16)  # Only if you know your system!
```

---

**Version**: 1.0.0

