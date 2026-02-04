"""
docking.py - Docking Module

Contains the main docking workflow function.
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import receptors_folder, ligands_folder, results_folder
from file_utils import find_pdbqt, find_configuration
from vina_execution import vina_execution
from cpu_utils import get_system_cores, read_cpu_from_config, check_cpu_usage, calculate_optimal_jobs



def filter_files(files, name_filter, list_file, file_type):
    """
    Filter files based on name filter or list file.
    
    Args:
        files: List of Path objects
        name_filter: List of filenames (without extension) or None
        ligand_filter: List of filenames (without extension) or None
        list_file: Path to file containing list of names or None
        file_type: String describing file type (for messages)
    
    Returns:
        Filtered list of Path objects
    """
    # If no filter, return all
    if name_filter is None and list_file is None:
        return files
    
    # Create set of names to include
    include_names = set()
    
    # From direct arguments
    if name_filter:
        include_names.update(name_filter)
        print(f"Filtering {file_type}: {', '.join(name_filter)}")
    
    # From list file
    if list_file:
        try:
            from pathlib import Path
            list_path = Path(list_file)
            with open(list_path, 'r') as f:
                names_from_file = [
                    line.strip() 
                    for line in f 
                    if line.strip() and not line.strip().startswith('#')
                ]
                include_names.update(names_from_file)
                print(f"Loaded {len(names_from_file)} {file_type} from {list_file}")
        except FileNotFoundError:
            print(f"WARNING: List file {list_file} not found, ignoring")
    
    # Filter the files
    filtered = [f for f in files if f.stem in include_names]
    
    print(f"Selected {len(filtered)} {file_type} out of {len(files)} available")
    
    return filtered


def is_valid_output(output_pdbqt, output_log):
    """
    Check if output files exist and are valid (not empty or corrupted).
    
    Args:
        output_pdbqt: Path to output PDBQT file
        output_log: Path to output log file
        
    Returns:
        True if both files exist and are valid, False otherwise
    """
    # Check if both files exist
    if not output_pdbqt.exists() or not output_log.exists():
        return False
    
    # Check if files are not empty
    try:
        if output_pdbqt.stat().st_size == 0:
            return False
        if output_log.stat().st_size == 0:
            return False
    except:
        return False
    
    return True



def vina_docking(vina_exe="vina", num_jobs=None,
                 receptor_filter=None, ligand_filter=None,
                 receptor_list_file=None, ligand_list_file=None,
                 global_config=None):

    # Some fancy display messages and appearance settings:
    print("=" * 70)
    print("STARTING DOCKING...")
    print("=" * 70)


    # Step 1: Find all ligands using the previously defined function find_pdbqt() and folder with ligands:

    ligands = find_pdbqt(ligands_folder)
    if not ligands:
        print(f"ERROR: No ligand found in {ligands_folder}")
        return
    
    # Step 1.1: Ligands filtering
    ligands = filter_files(ligands, ligand_filter, ligand_list_file, "ligands")
    if not ligands:
        print(f"ERROR: No ligands match the specified filter")
        return
    

    # Step 2: Find all receptors using the same find_pdbqt() function and the receptor folder:

    receptors = find_pdbqt(receptors_folder)
    if not receptors:
        print(f"ERROR: No receptor found in {receptors_folder}")
        return
    
    # Step 2.1: Receptors filtering
    receptors = filter_files(receptors, receptor_filter, receptor_list_file, "receptors")
    if not receptors:
        print(f"ERROR: No receptors match the specified filter")
        return
    

    # Step 3: Create output folder (vs_runs):

    results_folder.mkdir(parents=True, exist_ok=True)


    # Step 4: Prepare the list of all docking operations to carry out:

    tasks = [] # list initialization (now empty)
    
    # Get system cores for CPU check
    system_cores = get_system_cores()

    for receptor in receptors:
        rec_name = receptor.stem    # name without extension
        
        try: 
            config = find_configuration(rec_name, global_config)
        except FileNotFoundError as e:
            print(e)
            continue

        rec_folder = results_folder / f"vs_{rec_name}"      # creates subfolder with receptor-specific results
        log_folder = rec_folder / "logs"                    # creates subsubfolder for log files of the given receptor


        for ligand in ligands:
            lig_name = ligand.stem

            output_pdbqt = rec_folder / f"{lig_name}_out.pdbqt"
            output_log = log_folder / f"{rec_name}_{lig_name}.log"

            # Check if output is valid (exists and not empty/corrupted)
            if is_valid_output(output_pdbqt, output_log):
                continue
                
            tasks.append({
                "receptor": receptor, 
                "ligand": ligand, 
                "config": config, 
                "output_pdbqt": output_pdbqt, 
                "output_log": output_log
            })


    # Step 5: Verifies if there is something to do

    if not tasks:
        print("It seems like all dockings have already been executed.")
        print("=" * 70)
        return
    

    # Step 6: CPU resource check and automatic job calculation
    
    # Read CPU from first config file
    first_config = tasks[0]["config"]
    config_cpu = read_cpu_from_config(first_config)
    
    # If num_jobs not specified, calculate optimal value
    if num_jobs is None:
        num_jobs = calculate_optimal_jobs(config_cpu, system_cores)
        print(f"Auto-detected optimal parallel jobs: {num_jobs} (based on {system_cores} cores and config CPU={config_cpu})")
    else:
        # Check if user-specified num_jobs would cause overload
        is_ok, warning = check_cpu_usage(config_cpu, num_jobs, system_cores)
        if not is_ok:
            print(warning)
            print("Do you want to continue anyway? (yes/no): ", end="")
            response = input().strip().lower()
            if response not in ['yes', 'y']:
                print("Aborted by user.")
                return


    # Step 7: Display summary

    print(f"Receptors: {len(receptors)}")
    print(f"Ligands: {len(ligands)}")
    print(f"Dockings to perform: {len(tasks)}")
    print(f"Parallel jobs: {num_jobs}")
    print(f"Config CPU per job: {config_cpu}")
    print(f"Output folder: {results_folder}")
    print("=" * 70)


    # Step 8: Docking execution

    start = time.time()
    success = 0
    failed = 0

    if num_jobs == 1:
        print("\nExecuting one docking at a time...")       # serial mode
        for i, task in enumerate(tasks, 1):
            code = vina_execution(
                task["receptor"],
                task["ligand"],
                task["config"],
                task["output_pdbqt"],
                task["output_log"],
                vina_exe
            )

            if code == 0:
                success += 1
            else:
                failed += 1

            if i % 25 == 0 or i == len(tasks):
                print(f"Progress: {i}/{len(tasks)} (ok={success}, errors={failed})")        # showing profress every 25 docking processes and at the end
    
    else:
        print(f"\nExecuting {num_jobs} docking processes at a time...")      # parallel mode

        with ThreadPoolExecutor(max_workers=num_jobs) as executor:      # send all dockings to the executor function

            futures = []
            for task in tasks:
                future = executor.submit(
                    vina_execution,
                    task["receptor"],
                    task["ligand"],
                    task["config"],
                    task["output_pdbqt"],
                    task["output_log"],
                    vina_exe
                )
                futures.append(future)

            completed = 0   # initializing list of results as they are collected
            for future in as_completed(futures):
                code = future.result()
                completed += 1

                if code == 0:
                    success += 1
                else:
                    failed += 1

                if completed % 25 == 0 or completed == len(futures):
                    print(f"Progress: {completed}/{len(futures)} (ok={success}, errors={failed})")


    # Step 9: Show final results

    total_time = time.time() - start
    print("=" * 70)
    print("DOCKING COMPLETED")
    print("=" * 70)
    print(f"Successful: {success}")
    print(f"Failed: {failed}")
    print(f"Time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    print("=" * 70)
