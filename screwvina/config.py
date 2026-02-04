"""
config.py - Configuration Module

Contains all folder paths and global variables.

"""

from pathlib import Path


script_folder = Path(__file__).resolve().parent     # → /path/to/screwvina_modular_Claude_easier/

project_folder = script_folder.parent               # → /path/to/package_folder/

receptors_folder = project_folder / "receptors"
ligands_folder = project_folder / "ligands"
configurations_folder = project_folder / "configurations"
results_folder = project_folder / "vs_runs"
