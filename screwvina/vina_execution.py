"""
vina_execution.py - Vina Execution Module

Contains the function to execute a single Vina docking.

"""

import subprocess


def vina_execution(receptor_path, ligand_path, config_path, output_pdbqt, output_log, vina_exe):

    # Command definition:

    cmd = [
        vina_exe,
        "--receptor", str(receptor_path),
        "--ligand", str(ligand_path),
        "--config", str(config_path),
        "--out", str(output_pdbqt)
    ]

    output_pdbqt.parent.mkdir(parents=True, exist_ok=True)
    output_log.parent.mkdir(parents=True, exist_ok=True)

    # Vina execution and log saving:

    with open(output_log, "w") as f:
        result = subprocess.run(cmd, stdout=f, stderr=f)

    return result.returncode
