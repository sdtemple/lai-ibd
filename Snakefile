# The pipeline to intersect IBD segments with local ancestry,
# where the rule all is and many of the yaml parameters.
# You run this file with the -s parameter in snakemake.

import shutil
import os

macro=str(config['change']['files']['study'])
flare_prefix=str(config['change']['files']['flare_prefix'])
flare_suffix=str(config['change']['files']['flare_suffix'])
map_prefix=str(config['change']['files']['map_prefix'])
map_suffix=str(config['change']['files']['map_suffix'])
ibd_prefix=str(config['change']['files']['ibd_prefix'])
ibd_suffix=str(config['change']['files']['ibd_suffix'])
chromosome_high=str(config['change']['files']['chromosome_high'])
chromosome_low=str(config['change']['files']['chromosome_low'])

if not os.path.exists(macro):
    os.makedirs(macro)

if not os.path.exists(macro + '/maps'):
    os.makedirs(macro + '/maps')

for chromosome in range(int(chromosome_low),int(chromosome_high)+1):
    if not os.path.exists(macro + '/maps/chr' + str(chromosome) + '.map'):
        shutil.copyfile(map_prefix + str(chromosome) + map_suffix, macro + '/maps/chr' + str(chromosome) + '.map')

rule all:
    input:
        [macro + '/chr' + str(chromosome) + '.lai.ibd.gz' for chromosome in range(int(chromosome_low),int(chromosome_high)+1)],
        # macro + '/config.yaml',

rule clean_flare:
    input:
        mapin='{macro}/maps/chr{chromosome}.map',
    output:
        fileout='{macro}/chr{chromosome}.lai.gz',
    params:
        flare_prefix=flare_prefix,
        flare_suffix=flare_suffix,
    shell:
        '''
        python scripts/clean-flare-lai.py \
            {params.flare_prefix}{wildcards.chromosome}{params.flare_suffix} \
            {input.mapin} \
            {output.fileout}
        '''

rule concatenate_lai:
    input:
        filein='{macro}/chr{chromosome}.lai.gz',
    output:
        fileout='{macro}/chr{chromosome}.lai.segments.gz',
    shell:
        'python scripts/concatenate-lai.py {input.filein} {output.fileout}'

rule overlap_lai_ibd:
    input:
        laiin='{macro}/chr{chromosome}.lai.segments.gz',
    output:
        fileout='{macro}/chr{chromosome}.lai.ibd.gz',
    params:
        ibdin=ibd_prefix + '{chromosome}' + ibd_suffix,
    shell:
        '''
        python scripts/overlap-flare-lai-and-ibd.py \
            {input.laiin} \
            {params.ibdin} \
            {output.fileout}
        '''
