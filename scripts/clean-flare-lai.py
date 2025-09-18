# table for local ancestry intervals from flare
# seth d temple, sethtem at umich dot edu, 9/18/2025
# python clean-flare-lai.py *.vcf.gz a_file_prefix
# *.anc.vcf.gz : a gzipped anc vcf after flare, which is one of its outputs
# *.map : the genetic map for the chromosome
# file name for output

# imports
import sys
import gzip
import pandas as pd
from scipy.interpolate import interp1d

# setup, reading
vcfin,mapin,fileout=sys.argv[1:]
g=gzip.open(fileout,'wt')
itr=0

table = pd.read_csv(mapin, sep='\t', header=None)
# column 4 (index 3) as x, column 3 (index 2) as y
x = table[3].values
y = table[2].values

# create linear interpolation model
interp_model = interp1d(x, y, kind='linear', fill_value='extrapolate')

# process imputation vcf
with gzip.open(vcfin, 'rt') as f:
    for line in f:
        if line[:2]=='##':
            # this are details lines in vcf
            pass
        elif line[0]=='#':
            # this is header line in vcf
            header=line.strip().split('\t')
            hsamps=header[9:]
            samlen=len(hsamps)
            # write header line
            g.write('CHROM\tPOS\tCM\t')
            for j in range(samlen):
                # phased haplotypes
                hsamp=hsamps[j]
                if j < (samlen-1):
                    g.write(hsamp+'_1'); g.write('\t')
                    g.write(hsamp+'_2'); g.write('\t')
                else:
                    g.write(hsamp+'_1'); g.write('\t')
                    g.write(hsamp+'_2'); g.write('\n') # newline
        else:
            # these are the data lines in vcf
            lindat=(line.strip().split('\t'))
            g.write(lindat[0]+'\t'+lindat[1] + '\t' + str(interp_model(float(lindat[1])))); g.write('\t')
            lindat=lindat[9:]
            # print(lindat)
            # write the ref,alt alleles for phased haplotypes
            for j in range(samlen-1):
                gentyp=lindat[j]
                allel1,allel2=gentyp.split('|')
                idx=allel2.find(':')
                laianc=allel2[idx+1:]
                laiidx=laianc.find(':')
                anc1=laianc[:laiidx]
                anc2=laianc[laiidx+1:]
                g.write(anc1); g.write('\t')
                g.write(anc2); g.write('\t')
            gentyp=lindat[-1]
            allel1,allel2=gentyp.split('|')
            idx=allel2.find(':')
            laianc=allel2[idx+1:]
            laiidx=laianc.find(':')
            anc1=laianc[:laiidx]
            anc2=laianc[laiidx+1:]
            g.write(anc1); g.write('\t')
            g.write(anc2); g.write('\n')
g.close()
