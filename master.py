#!/usr/bin/env python

# Runs Jaccard Similarity script with all of the classification files
# against each other at the Genus and the Species level

from sys import argv
from sys import exit
import subprocess as sp
import os
import uuid

# CONSTANTS
UUID = str(uuid.uuid4())
SCRIPT = "./jaccardSimilarity1.py"
GENUS_OUT = "genus-similarity-" + UUID + ".csv"
SPEC_OUT = "species-similarity-" + UUID + ".csv"

def main():
    # Get classification files
    files = [x for x in os.listdir(".") if x.startswith("Classification")]
    sampleNames = getSampleNames(files)

    jaccGenus = getJacc(files, sampleNames, "Genus")
    jaccSpec = getJacc(files, sampleNames, "Species")

    writeOut(jaccGenus, GENUS_OUT)
    writeOut(jaccSpec, SPEC_OUT)

    print "Genus output written to:", GENUS_OUT
    print "Species output written to:", SPEC_OUT

    exit(0)



# Takes a list of Classification files and returns a parallel list of sample
# names corresponding to those files
def getSampleNames(files):
    toReturn = []
    for f in files:
        toReturn.append(getName(f))

    return toReturn

# Dives into file to retrieve name of sample contained within it
def getName(fi):
    with open(fi, 'Ur') as filer:
        filer.readline()
        secLine = filer.readline()
        listL = secLine.split("\t")

        return listL[1]

# Spins off subprocesses using SCRIPT. Returns a list of lists where each list
# is [SAMP1, SAMP2, Jaccard]
# NOTE: Jaccard Similarity is a symetric measurement
def getJacc(files, names, lvl):
    toReturn = []
    for x in range(len(files)):
        for y in range(x + 1, len(files)):
            val = sp.check_output([SCRIPT, files[x], files[y], lvl]).strip()
            toReturn.append([names[x], names[y], val])

    return toReturn


# Writes out the output to a CSV file
def writeOut(info, fileName):
    with open(fileName, 'w') as filew:
        filew.write("#Sample_1,Sample_2,Jaccard_Similarity\n")
        for entry in info:
            filew.write(",".join(entry) + "\n")
        

if __name__ == '__main__':
    main()
