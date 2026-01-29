"""
file_utils.py - File Utilities Module

Contains functions for finding files and configurations.
"""

from config import configurations_folder

# ==========================================================================================================================================================================
# ==========================================================================================================================================================================

def find_pdbqt(folder):

    if not folder.exists():
        return []
    
    files = sorted(folder.glob("*.pdbqt"))  # find all PDBQT files and sort them
    return files

# ==========================================================================================================================================================================
# ==========================================================================================================================================================================

def find_configuration(receptor_name):

    configs = [configurations_folder / f"{receptor_name}.txt"]     # configuration files have TXT estension

    for config in configs:
        if config.exists():
            return config
    
    raise FileNotFoundError(f"Error: Configuration for '{receptor_name}' not found.")
