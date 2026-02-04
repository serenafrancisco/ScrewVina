"""
screwvina.py - Main Script

Contains the main function and command-line interface.
"""

import argparse
import sys

from docking import vina_docking
from analysis import analyze_results



def main():

    parser = argparse.ArgumentParser(
        description="ScrewVina: Automatized molecular docking with AutoDock-Vina"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)


    # DOCK command:

    dock_parser = subparsers.add_parser("dock", help="Execute docking and analysis")

    dock_parser.add_argument(
        "--vina",
        default = "vina",
        help = "Name or path of the vina executable (default: vina)"
    )
    dock_parser.add_argument(
        "--jobs",
        type = int,
        default = None,
        help = "Number of parallel docking jobs (default: auto-calculated based on system cores)"
    )
    dock_parser.add_argument(
        "--no-analyze",
        action = "store_true",
        help = "Do not execute the automatic analysis after docking"    # here, the user has to explicitly add the --no-analysis argument to avoid analysis
    )

    dock_parser.add_argument(
        "--receptors",
        nargs = "+",   # lists are accepted
        default = None,
        help = "Specific receptor files to use without extension (default: all)"
    )

    dock_parser.add_argument(
        "--ligands",
        nargs = "+",
        default = None,
        help = "Specific ligand files to use without extension (default: all)"
    )

    dock_parser.add_argument(
        "--receptors-list",
        type = str,
        default = None,
        help = "File containing list of receptors (one per line)"
    )

    dock_parser.add_argument(
        "--ligands-list",
        type = str,
        default = None,
        help = "File containing list of ligands (one per line)"
    )

    dock_parser.add_argument(
        "--global-config",
        type = str,
        default = None,
        help = "Path to a global/master configuration file to use when receptor-specific config is not found"
    )


    # ANALYZE command:
    analyze_parser = subparsers.add_parser("analyze", help="Analyze docking results only")

    analyze_parser.add_argument(
        "--out",
        default = "vina_results.tsv",
        help = "Output filename (default: vina_results.tsv)"
    )


    # Read arguments
    args = parser.parse_args()


    # Execute the requested command

    try:
        if args.command == "dock":
            vina_docking(
                vina_exe=args.vina, 
                num_jobs=args.jobs,
                receptor_filter=args.receptors,
                ligand_filter=args.ligands,
                receptor_list_file=args.receptors_list,
                ligand_list_file=args.ligands_list,
                global_config=args.global_config
            )
    
            if not args.no_analyze:     # does everything, unless analysis is disabled with --no-analyze
                print()
                analyze_results()
            
        elif args.command == "analyze":
            analyze_results(output_filename=args.out)   # just perform final analysis
    
    except Exception as e:
        print(f"ERROR: {e}")
        return 1
    
    return 0



if __name__ == "__main__":
    sys.exit(main())
