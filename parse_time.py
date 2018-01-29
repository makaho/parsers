#!/usr/bin/python
# command = "Command being timed"
# #"bowtie -m 1 -p 16 --best --strata -v 2 /index/hg19 -q /hosthome/bowtie/SRR949076_1.fastq -S /hosthome/bowtie/Sample.sam"
# user_time = "User time (seconds)"
# system_time = "System time (seconds)"
# cpu = "Percent of CPU this job got"
# wall_time = "Elapsed (wall clock) time (h:mm:ss or m:ss)"
# avg_shared_txt = "Average shared text size (kbytes)"
# avg_unshared_txt = "Average unshared data size (kbytes)"
# avg_stack = "Average stack size (kbytes)"
# avg_total_stack = "Average total size (kbytes)"
# max_res_size = "Maximum resident set size (kbytes)"
# avg_res_size = "Average resident set size (kbytes)"
# maj_page_faults = "Major (requiring I/O) page faults"
# min_page_faults = "Minor (reclaiming a frame) page faults"
# vol_ctx_switch = "Voluntary context switches"
# invol_ctx_switch = "Involuntary context switches"
# swaps = "Swaps"
# fs_in = "File system inputs"
# fs_out = "File system outputs"
# smsg_sent = "Socket messages sent"
# smsg_rcvd = "Socket messages received"
# sig_dlvrd = "Signals delivered"
# page_size = "Page size (bytes)"
# exit_val = "Exit status"

import os.path
import csv
import sys
from math import floor

possible_entries = {"Aligner", "Threads", "Sample", "Command being timed", "User time (seconds)", "System time (seconds)",
                    "Percent of CPU this job got",
                    "Elapsed (wall clock) time (h:mm:ss or m:ss)", "Average shared text size (kbytes)",
                    "Average unshared data size (kbytes)", "Average stack size (kbytes)",
                    "Average total size (kbytes)",
                    "Maximum resident set size (kbytes)", "Average resident set size (kbytes)",
                    "Major (requiring I/O) page faults",
                    "Minor (reclaiming a frame) page faults",
                    "Voluntary context switches", "Involuntary context switches", "Swaps",
                    "File system inputs",
                    "File system outputs", "Socket messages sent",
                    "Socket messages received", "Signals delivered", "Page size (bytes)", "Exit status"}
possible_entries = sorted(possible_entries)

def parseLogFileAndWriteToCSV(csvFileName, logFile):
    entry = dict()
    # Parse file name
    filename = os.path.basename(logFile)
    pos = filename.rfind("_")
    filename = filename[:pos]
    pos = filename.rfind("_")
    entry["Threads"] = filename[pos+1:]
    filename = filename[:pos]
    pos = filename.rfind("_")
    entry["Aligner"] = filename[pos+1:]
    filename = filename[:pos]
    entry["Sample"] = filename
    # Parse file
    with open(logFile) as f:
        for line in f:
            line = line.strip()
            pos = line.find(":")
            if pos == -1:
                continue
            if line.startswith("Elapsed (wall clock) time (h:"):
                midpos = line.find(":ss):")
                pos = midpos + 4
            cmd = line[:pos]
            val = line[pos + 1:]
            cmd = cmd.strip()
            val = val.strip()
            val = val.strip()
            for option in possible_entries:
                if cmd == option:
                    entry[cmd] = val
                    if (cmd == "Elapsed (wall clock) time (h:mm:ss or m:ss)"):
                        # convert
                        entry[cmd] = sum(int(float(x)) * 60 ** i for i,x in enumerate(reversed(val.split(":"))))
    # if header, write header
    if os.path.exists(csvFileName):
        # open and jump to end
        with open(csvFileName, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=possible_entries)
            writer.writerow(entry)
    else:
        # create, write headers
        with open(csvFileName, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=possible_entries)
            writer.writeheader()
            writer.writerow(entry)


def main():
    # count args
    if len(sys.argv) < 3:
        print("usage " + sys.argv[0] + " output.csv input1.log input2.log ...")
    outfile = sys.argv[1];
    for i in range(2, len(sys.argv)):
        parseLogFileAndWriteToCSV(outfile, sys.argv[i])


if __name__ == "__main__":
    main()
