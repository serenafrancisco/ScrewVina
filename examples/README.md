# ScrewVina Examples

This directory contains example files for testing ScrewVina.

## Contents

- **receptors/** - 2 example receptor structures
- **ligands/** - 3 example ligand structures (from DrugBank)
- **configurations/** - Configuration files for each receptor
- **run_example.sh** - Script to run the example

## Quick Run
```bash
# From the examples/ directory
bash run_example.sh
```

This will:
1. Run docking (2 receptors × 3 ligands = 6 dockings)
2. Generate analysis report
3. Create `vina_results.tsv`

## Expected Output
```
examples/
├── vs_runs/                      # Docking results
│   ├── vs_example_receptor_1/
│   │   ├── example_ligand_1_out.pdbqt
│   │   ├── example_ligand_2_out.pdbqt
│   │   ├── example_ligand_3_out.pdbqt
│   │   └── logs/
│   └── vs_example_receptor_2/
│       └── ...
└── vina_results.tsv             # Analysis summary
```

## Using Your Own Data

1. Replace files in `receptors/` with your receptors
2. Replace files in `ligands/` with your ligands
3. Update/create config files in `configurations/`
4. Run: `bash run_example.sh`

## Notes

- Example files are small for quick testing
- Real docking may take longer depending on:
  - Number of ligands
  - Exhaustiveness setting
  - CPU cores available
