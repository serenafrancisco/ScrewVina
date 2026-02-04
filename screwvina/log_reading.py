"""
log_reading.py - Log Reading Module

Contains the function to read and parse Vina log files.
"""


def read_vina_log(log_path):

    affinity = []
    rmsd = []
    in_table = False

    with open(log_path, "r") as f:
        for row in f:
            row = row.strip()

            if "mode" in row.lower() and "affinity" in row.lower():   # finding the begininng of the table 
                in_table = True
                continue

            if in_table:                # if we are inside the table, then read data
                parts = row.split()

                if not parts:       # empty row = end of the table
                    if affinity:    # if we already have data, stop
                        break
                    continue
                if not parts[0].isdigit():  # skip rows that do not start with number
                    if affinity:            # if we already have data, stop
                        break
                    continue

                try:                                      # extract affinity (second column: [1])
                    affinity.append(float(parts[1]))
                except:
                    continue

                if len(parts) >= 4:                     # extract RMSD upper bound (fourth column)
                    try:
                        rmsd.append(float(parts[3]))
                    except:
                        pass

    return affinity, rmsd
