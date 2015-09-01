#!/usr/bin/env python
#
# jaccardSimilarity.py
# Author: Hannah DeBaets
# Date Created: 1/14/15
# Last Modified: 1/14/15
#
# EG: Invoke the script using: ./jaccardSimilarity.py classificationsFile1.txt classificationsFile2.txt

from sys import argv
from sys import exit
lvl = 'Species'
minPct = float(1.0)

def main():
    if len(argv) != 4:
        usage()
        exit(1)
    lvl = argv[3]   # level to explore phylogeny
    lvlFilter(lvl)  # Make sure lvl is valid
    #make dictionary of names and percentages that pass requirements
    sample1 = accumulateApproved(argv[1], lvl, minPct)
    sample2 = accumulateApproved(argv[2], lvl, minPct)
    #count up overlap/compare
    Nc = float(findOverlap(sample1, sample2))
    #calculate similarity
    Na = float(len(sample1))
    Nb = float(len(sample2))
    jaccardValue = float(Nc/(Na+Nb-Nc))
    return jaccardValue
    #print similarity
    print "Jaccard Similarity between", argv[1], "and", argv[2], "is:", jaccardValue
    #print percentages in easy to make bar graph format
    exit(0)


# Makes sure the level is either "Species" or "Genus" otherwise calls usage
# and thus exits non-zero
def lvlFilter(lvl):
    if lvl == 'Genus':
        return
    elif lvl == 'Species':
        return
    else:  # Not a valid level
        print "ERROR: The only valid levels are \"species\" and \"genus\""
        usage()

#prints usage and exits nonzero
def usage():
    print "USAGE:", argv[0], "Classification 1, Classification2, level"
    exit(1)

#takes calssification file as input, with set level (genus, species, etc.)
#and minimum percent (1.0 = 1%, 0.5 = 0.5%)
#creates a dictionary of {genus or species: percentage present in sample}
def accumulateApproved(classyFile, lvl, minPct):
    sample = {}
    with open(classyFile, 'r') as filer:
        for line in filer:
            line = line.strip()
            col = line.split("\t")[2:]
            if col[0].startswith(lvl) and float(col[3])>=minPct:
                if col[1] != "Unclassified":
                    sample[col[1]] = [col[3]]
    return sample

#takes input of two sample dictionaries
#returns the number of overlapping genus/species
def findOverlap(sample1, sample2):
    counter = 0
    for key in sample1:
        if key in sample2:
            counter = 1 + counter
    return counter


if __name__ == '__main__':
        main()
