#!/usr/bin/python

import os.path
import csv
import sys
import xml.etree.ElementTree as ET
from math import floor

possible_entries = {"accession", "study", "spot_count", "base_count", "base_count_bio", "size", "size-units"}
possible_entries = sorted(possible_entries)

def parseLogFileAndWriteToCSV(csvFileName, xmlFileName):
    entry = dict()

    # Parse file
    print(xmlFileName)
    tree = ET.parse(xmlFileName)
    root = tree.getroot()
    if (root.tag != "Run"):
        return
    entry["accession"] = os.path.basename(os.path.splitext(root.attrib["accession"])[0])
    entry["study"] = os.path.basename(os.path.dirname(root.attrib["accession"]))
    entry["spot_count"] = root.attrib["spot_count"]
    entry["base_count"] = root.attrib["base_count"]
    entry["base_count_bio"] = root.attrib["base_count_bio"]
    size = root.findall("./Size")[0]
    entry["size"] = size.attrib["value"]
    entry["size-units"] = size.attrib["units"]

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
