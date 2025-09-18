# Overlaying local ancestry on IBD segments

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)

This pipeline is a series of three Python scripts that determine if both haplotypes in a long IBD segment have the same local ancestry. The final files are of the type `chr.lai.ibd.overlap.gz` under the folder you specify in the `config.yaml` file.
- The `ANCESTRY` column is a number that corresponds to those panels in the FLARE `anc.vcf.gz` output.
- The `ANCESTRY` is -1 if one or both of the haplotypes have an ancestry switch in the IBD stretch.
- The file format mirrors that of `hap-ibd.jar` but with an `ANCESTRY` column and a header.

In `config.yaml`, you need to adjust the file paths to where your genetic map, FLARE, and IBD segment data are.

You can run the script with `snakemake -c1 --configfile config.yaml`. Use `-n` to make a dry-run and see if the files are specified correctly. Visit [isweep](https://isweep.readthedocs.io/en/latest/misc.html#snakemake-options) for more advice.

I have not designed the `scripts/overlap-flare-lai-and-ibd.py` script for chunked dataframe processing. If you have a large IBD file (say from a biobank-scale) analysis, the program may crash.

### Assumptions
---

Some assumptions of the scripts are:
- There are less than 11 ancestry groups in the FLARE analysis.
- You have used the file format of `hap-ibd.jar` to call IBD.
- You have Python `pandas` installed in your current environment.
- You have Snakemake installed in your current environment.

### Other software
---

This code is part of a Snakemake workflow.

For more information about Snakemake workflows, rules, and configuration, see the official documentation:
https://snakemake.readthedocs.io/.

This code is written and tested on output data from
- [FLARE (Browning Lab)](https://github.com/browning-lab/flare)
- [hap-ibd (Browning Lab)](https://github.com/browning-lab/hap-ibd)

This code can be run after the [isweep local ancestry pipeline](https://github.com/sdtemple/isweep/tree/main/workflow/phasing-ancestry).

