"""
cpu_utils.py - CPU Resource Management Module

Contains functions for CPU and resource checks.
"""

import os


def get_system_cores():
    """
    Get the number of CPU cores available on the system.
    
    Returns:
        Number of CPU cores
    """
    try:
        return os.cpu_count() or 1
    except:
        return 1


def read_cpu_from_config(config_path):
    """
    Read the CPU value from a Vina configuration file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Number of CPUs specified in config, or 1 if not found
    """
    try:
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('cpu'):
                    parts = line.split('=')
                    if len(parts) >= 2:
                        return int(parts[1].strip())
    except:
        pass
    return 1


def check_cpu_usage(config_cpu, num_jobs, system_cores):
    """
    Check if the combination of config CPU and jobs would overload the system.
    
    Args:
        config_cpu: CPUs per docking job (from config file)
        num_jobs: Number of parallel jobs
        system_cores: Total system cores available
        
    Returns:
        (is_ok, warning_message)
    """
    total_threads = config_cpu * num_jobs
    
    if total_threads > system_cores:
        warning = (
            f"\nWARNING: Resource overload detected!\n"
            f"  Config CPU: {config_cpu}\n"
            f"  Parallel jobs: {num_jobs}\n"
            f"  Total threads: {total_threads}\n"
            f"  System cores: {system_cores}\n"
            f"  This may cause severe slowdown (thrashing).\n"
            f"  Recommended: Set --jobs to {system_cores // config_cpu} or lower.\n"
        )
        return False, warning
    
    return True, None


def calculate_optimal_jobs(config_cpu, system_cores):
    """
    Calculate the optimal number of parallel jobs based on config CPU and system cores.
    
    Args:
        config_cpu: CPUs per docking job (from config file)
        system_cores: Total system cores available
        
    Returns:
        Optimal number of parallel jobs
    """
    if config_cpu <= 0:
        return 1
    
    optimal = system_cores // config_cpu
    return max(1, optimal)  # At least 1 job
