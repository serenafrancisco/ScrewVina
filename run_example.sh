#!/bin/bash
# run_example.sh - Run ScrewVina example

set -e  # Exit on error

echo "======================================"
echo "ScrewVina Example"
echo "======================================"

# Check if conda environment is activated
if [[ -z "${CONDA_DEFAULT_ENV}" ]]; then
    echo "Warning: Conda environment not detected"
    echo "Recommended: conda activate screwvina"
    echo ""
fi

# Check if Vina is available
if ! command -v vina &> /dev/null; then
    echo "ERROR: Vina not found in PATH"
    echo "Please install: conda install -c conda-forge vina"
    exit 1
fi

echo "Running example docking..."
echo ""

# Navigate to screwvina package
cd ./screwvina

# Run docking with 2 parallel jobs (small example)
python screwvina.py dock --jobs 2

echo ""
echo "======================================"
echo "Example completed!"
echo "======================================"
echo "Results in: examples/vs_runs/"
echo "Summary in: examples/vina_results.tsv"
echo ""
