# BETS analysis for Bhutan TB

Run [Bayesian Evaluation of Temporal Signal](https://doi.org/10.1093/molbev/msaa163) (BETS) analysis with strict and UCLN clock models and exponential population growth using nested sampling for Marginal Likelihood Estimation.

## Set up

This pipeline can be installed with [snk](https://snk.wytamma.com) (recommended for ease of use).

```bash
snk install wytamma/bhutan-tb-bets
```

# Data

Core alignment file derived from Snippy. 

Use [Core-SNP-filter](https://github.com/rrwick/Core-SNP-filter) to create the soft core alignment file. 

## Constant sites

core = `123579424 236159820 235266551 123686338`
soft core = `721745 1376926 1371926 722492`

# Running the Bhutan TB Analysis

Run the analysis in tmux to avoid the process being killed when the ssh connection is lost.

The `slurm` profile is used to submit jobs to the slurm queue on the HPC.  

```bash
bhutan-tb-bets run --alignment data/core_dated.aln --beast-constant-site-weights "123579424 236159820 235266551 123686338" results/BETS/BETS.png --profile slurm
```

## Running 95% soft core 

```bash
bhutan-tb-bets run --alignment data/core_.95.aln --beast-constant-site-weights "123579424 236159820 235266551 123686338" soft_core_95/BETS/BETS.png --profile slurm --out soft_core_95
```

### Increase number of particles 

There was overlap in the BF CI so I increased the number of particles to 5

```bash
bhutan-tb-bets run --alignment data/core_.95.aln --beast-constant-site-weights "123579424 236159820 235266551 123686338" soft_core_95_5/BETS/BETS.png --profile slurm --out soft_core_95_5 --bets-particle-count 5
```

# Running bhutan + vietnam dataset

Added the Vietnam samples to the Bhutan dataset to attempt to increase the temporal signal.

All the viet samples are missing days e.g. SRR5065238|2010-12

Add `-15` to the end of all of the dates (https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012900). 

```bash
sed -E 's/(>[A-Za-z0-9_]+\|[0-9]{4}-[0-9]{2})$/\1-15/' data/bhutan_vietnam.aln > data/bhutan_vietnam_fixed_dates.aln
```

```bash
bhutan-tb-bets run --alignment data/bhutan_vietnam_fixed_dates.aln --beast-constant-site-weights "721082 1374963 1370030 721829" bhutan_vietnam_fixed_dates/BETS/BETS.png --profile slurm --out bhutan_vietnam_fixed_dates --bets-particle-count 5
```

Increased the subchain length to 50000.

```bash
bhutan-tb-bets run --alignment data/bhutan_vietnam_fixed_dates.aln --beast-constant-site-weights "721082 1374963 1370030 721829" bhutan_vietnam_fixed_dates_constant_sites/BETS/BETS.png --profile slurm --out bhutan_vietnam_fixed_dates_50K --bets-particle-count 5 --bets-subchain-length 50000
```

Longer sub-chain length to 100K

```bash
bhutan-tb-bets run --alignment data/bhutan_vietnam_fixed_dates.aln --beast-constant-site-weights "721082 1374963 1370030 721829" bhutan_vietnam_fixed_dates_100K/BETS/BETS.png --profile slurm --out bhutan_vietnam_fixed_dates_100K --bets-particle-count 5 --bets-subchain-length 100000
```
