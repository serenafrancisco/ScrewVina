"""
analysis.py - Analysis Module

Contains the function to analyze docking results.

"""

from statistics import mean, stdev

from config import results_folder, project_folder  
from log_reading import read_vina_log



def analyze_results(output_filename="vina_results.tsv"):

    print("=" * 70)
    print("STARTING ANALYSIS...")
    print("=" * 70)


    # Step 1: check the output folder exists ---------------------------------------------------------------------------------------------------
    if not results_folder.exists():
        print(f"ERROR: Output folder {results_folder} does not exist")      # though it should be created by the script at the beginning
        return
    

    # Step 2: Find all vs_* directories --------------------------------------------------------------------------------------------------------
    vs_directories = [
        d for d in results_folder.iterdir()
        if d.is_dir() and d.name.startswith("vs_")
    ]

    if not vs_directories:
        print (f"ERROR: No vs_* directory found in {results_folder}")
        return
    
    print(f"{len(vs_directories)} directories found")


    # Step 3: Collect all results -------------------------------------------------------------------------------------------------------------

    results = []        # initializing list of results

    for directory in vs_directories:
        rec_name = directory.name.replace("vs_", "")    # receptor name (e.g. vs_proteinA -> proteinA)
        
        log_folder = directory / "logs"     # directory with log files
        if not log_folder.exists():
            continue

        for log_file in log_folder.glob("*.log"):
            lig_name = log_file.stem.split("_")[-1]     # ligand name from filename (e.g. proteinA_ligand1.log -> ligand1)

            affinity, rmsd = read_vina_log(log_file)        # reads the log file

            if not affinity:
                continue        # skip where there is no data

            best_aff = affinity[0]      # best affinity is always the first mode

            if len(affinity) == 1:          # calculates statistics for affinity values
                mean_aff = affinity[0]
                dev_aff = 0.0
            else:
                mean_aff = mean(affinity)
                dev_aff = stdev(affinity)

            rmsd_from_pose2 = rmsd[1:] if len(rmsd) > 1 else []     # statistics for RMSD (first pose skipped, always 0)
            if not rmsd_from_pose2:
                mean_rmsd = 0.0
                dev_rmsd = 0.0
            elif len(rmsd_from_pose2) == 1:
                mean_rmsd = rmsd_from_pose2[0]
                dev_rmsd = 0.0
            else:
                mean_rmsd = mean(rmsd_from_pose2)
                dev_rmsd = stdev(rmsd_from_pose2)
            
            results.append({            # appending results to the results list
                "receptor": rec_name,
                "ligand": lig_name,
                "best_affinity": best_aff,
                "mean_affinity": mean_aff,
                "stdev_affinity": dev_aff,
                "mean_rmsd": mean_rmsd,
                "stdev_rmsd": dev_rmsd
            })
    

    # Step 4: Write TSV file -----------------------------------------------------------------------------------------------------------------

    out_file = project_folder / output_filename

    with open(out_file, "w") as f:          # write header
        f.write(
            "Receptor\tLigand\tBest_Affinity\tAvg_Affinity\tStd_Dev_Affinity\tAvg_RMSD_UB\tStd_Dev_RMSD_UB\n"
        )

        for r in results:               # write results
            f.write(
                f"{r['receptor']}\t"
                f"{r['ligand']}\t"
                f"{r['best_affinity']:.3f}\t"   # display 3 significative digits
                f"{r['mean_affinity']:.3f}\t"
                f"{r['stdev_affinity']:.3f}\t"
                f"{r['mean_rmsd']:.3f}\t"
                f"{r['stdev_rmsd']:.3f}\n"
            )

    
    # Step 5: Show final result -----------------------------------------------------------------------------------------------------------------
    print(f"Analysis completed: {len(results)} receptor-ligand pairs")
    print(f"Results saved to {out_file}")
    print("=" * 70)
