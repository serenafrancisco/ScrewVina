"""
docking.py - Docking Module

Contains the main docking workflow function.
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import receptors_folder, ligands_folder, results_folder
from file_utils import find_pdbqt, find_configuration
from vina_execution import vina_execution

# ==========================================================================================================================================================================
# ==========================================================================================================================================================================

def vina_docking(vina_exe="vina", num_jobs=4):

    # Some fancy display messages and appearance settings:
    print("=" * 70)
    print("STARTING DOCKING...")
    print("=" * 70)


    # Step 1: Find all ligands using the previously defined function find_pdbqt() and folder with ligands:

    ligands = find_pdbqt(ligands_folder)
    if not ligands:
        print(f"ERROR: No ligand found in {ligands_folder}")
        return
    

    # Step 2: Find all receptors using the same find_pdbqt() function and the receptor folder:

    receptors = find_pdbqt(receptors_folder)
    if not receptors:
        print(f"ERROR: No receptor found in {receptors_folder}")
        return
    

    # Step 3: Create output folder (vs_runs):

    results_folder.mkdir(parents=True, exist_ok=True)


    # Step 4: Prepare the list of all docking operations to carry out:

    tasks = [] # list initialization (now empty)

    for receptor in receptors:
        rec_name = receptor.stem    # name without extension
        
        try: 
            config = find_configuration(rec_name)
        except FileNotFoundError as e:
            print(e)
            continue

        rec_folder = results_folder / f"vs_{rec_name}"      # creates subfolder with receptor-specific results
        log_folder = rec_folder / "logs"                    # creates subsubfolder for log files of the given receptor


        for ligand in ligands:
            lig_name = ligand.stem

            output_pdbqt = rec_folder / f"{lig_name}_out.pdbqt"
            output_log = log_folder / f"{rec_name}_{lig_name}.log"

            if output_pdbqt.exists() and output_log.exists():
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
    

    # Step 6: Display summary

    print(f"Receptors: {len(receptors)}")
    print(f"Ligands: {len(ligands)}")
    print(f"Dockings to perform: {len(tasks)}")
    print(f"Parallel jobs: {num_jobs}")
    print(f"Output folder: {results_folder}")
    print("=" * 70)


    # Step 7: Docking execution

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


    # Step 8: Show final results

    total_time = time.time() - start
    print("=" * 70)
    print("DOCKING COMPLETED")
    print("=" * 70)
    print(f"Successful: {success}")
    print(f"Failed: {failed}")
    print(f"Time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    print("=" * 70)
