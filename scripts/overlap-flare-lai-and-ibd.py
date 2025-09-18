# assign ancestry to an ibd segments if both haplotypes have same ancestry
# seth d temple, sethtem at umich dot edu, 9/18/2025
# python overlap-flare-lai-and-ibd.py *.lai.segments.gz *.ibd.gz file_output
# *.lai.segments.gz : output from concatenate-lai.py
# *.ibd.gz : a gzipped IBD file from hap-ibd.jar
# then a file output

import pandas as pd
import sys

laiin, ibdin, fileout = sys.argv[1:]

lai = pd.read_csv(laiin, sep='\t')
ibd = pd.read_csv(ibdin, sep='\t', header=None)
ibd.columns = ['ID1', 'HAP1', 'ID2', 'HAP2', 'CHROM', 'START', 'END', 'CM']
ibd['IDHAP1'] = ibd.apply(lambda x: str(x['ID1']) + '_' + str(x['HAP1']), axis=1)
ibd['IDHAP2'] = ibd.apply(lambda x: str(x['ID2']) + '_' + str(x['HAP2']), axis=1)
ibd['ANCESTRY'] = -1

num_ibd_segments = ibd.shape[0]
num_not_covered = 0
num_different_ancestry = 0

for _ in range(num_ibd_segments):

    row = ibd.iloc[_]
    lai_sub = lai[lai['ID_HAP'].isin([row['IDHAP1'], row['IDHAP2']])]
    left = float(row['START'])
    right = float(row['END'])
    # local ancestry segments must contain the IBD segment
    lai_sub = lai_sub[(lai_sub['BPLEFT'] <= left) & (lai_sub['BPRIGHT'] >= right)]

    # both haplotypes must contain the IBD stretch
    if lai_sub.shape[0] >= 2:
        if lai_sub['ANCESTRY'].nunique() <= 1:
            # same ancestry on both haplotypes
            # and they fully cover the ibd stretch
            ibd.at[_, 'ANCESTRY'] = lai_sub['ANCESTRY'].iloc[0]
        else:
            # different ancestry on the two haplotypes
            num_different_ancestry += 1
    else:
        # not fully covered by LAI segments
        num_not_covered += 1

print(f'Percent {num_not_covered/num_ibd_segments} of IBD segments not fully covered by LAI segments')
print(f'Percent {num_different_ancestry/num_ibd_segments} of fully covered IBD segments have different ancestries on haplotypes')
ibd.to_csv(fileout, sep='\t', index=False, columns = ['IDHAP1','IDHAP2','ANCESTRY','CHROM','START','END','CM'])
