# concatenate local ancestry calls per bp to segments
# seth d temple, sethtem at umich dot edu, 9/18/2025
# python concatenate-lai.py file_input file_output
# run after clean-flare-lai.py

import sys
import gzip
import re

filein, fileout, = sys.argv[1:]

with gzip.open(fileout, 'wt') as g:
    g.write('ID_HAP\tCHROM\tBPLEFT\tBPRIGHT\tCMLEFT\tCMRIGHT\tANCESTRY\n')

    # process the previous file to get LAI segments
    with gzip.open(filein, 'rt') as f:
        # read the first line containing individual IDs
        line = f.readline().strip().split('\t')
        individuals = line[3:]
        nind = len(individuals)
        laisegs = [[] for _ in range(nind)]
        # initialize segments for each haplotype of each individual
        line = f.readline().strip().split('\t')
        positional = line[:3]
        cM = float(line[2])
        bp = int(line[1])

        # # get string whether it be chr1 or 1
        # chrom = line[0]

        # get number only
        match = re.search(r'\d+', line[0])
        chrom = int(match.group())

        ancestry_data = line[3:]
        for _ in range(nind):
            ind = individuals[_]
            ancgt = ancestry_data[_]
            # I assume that there are less than 10 ancestries
            # Which is why I hard coded 0 and 2 below
            laisegs[_] = [ind, chrom, bp, bp, cM, cM, ancgt]
        for line in f:
            line = line.strip().split('\t')
            positional = line[:3]
            cM = float(line[2])
            bp = int(line[1])
            ancestry_data = line[3:]
            for _ in range(nind):
                ind = individuals[_]
                ancgt = ancestry_data[_]

                # first haplotype
                if ancgt == laisegs[_][6]:
                    laisegs[_][3] = bp
                    laisegs[_][5] = cM
                else:
                    # write out the previous segment
                    g.write('\t'.join(map(str, laisegs[_])) + '\n')
                    # start a new segment
                    laisegs[_] = [ind, chrom, bp, bp, cM, cM, ancgt]

    for _ in range(nind):
        g.write('\t'.join(map(str, laisegs[_])) + '\n')