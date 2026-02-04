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

def find_configuration(receptor_name, global_config=None):
    """
    Find configuration file for a receptor.
    First tries receptor-specific config, then falls back to global config if provided.
    
    Args:
        receptor_name: Name of the receptor (without extension)
        global_config: Optional path to a global/master configuration file
        
    Returns:
        Path to configuration file
        
    Raises:
        FileNotFoundError: If no configuration is found
    """

    # Try receptor-specific config first
    specific_config = configurations_folder / f"{receptor_name}.txt"
    if specific_config.exists():
        return specific_config
    
    # Fall back to global config if provided
    if global_config is not None:
        from pathlib import Path
        global_path = Path(global_config)
        if global_path.exists():
            return global_path
        else:
            raise FileNotFoundError(f"Error: Global configuration file '{global_config}' not found.")
    
    # No config found
    raise FileNotFoundError(
        f"Error: Configuration for '{receptor_name}' not found. "
        f"Expected: {specific_config} or use --global-config option."
    )
