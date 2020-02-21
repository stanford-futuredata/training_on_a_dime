# Analysis and Exploitation of Dynamic Pricing in the Public Cloud for ML Training

This repository contains code and data to accompany the paper `Analysis and
Exploitation of Dynamic Pricing in the Public Cloud for ML
Training` that is to appear at DISPA 2020. In particular, we provide scripts
that can be used to collect pricing information across cloud providers, as well
as logs we collected in Februrary and March 2020.

This repository is organized as follows:
- `scripts`: Scripts to automatically scrape pricing information for
  AWS and GCP; we manually collected prices for Azure.
- `logs`: Collected pricing information for AWS, Azure, and GCP.
- `notebooks`: Jupyter notebooks that show how to parse and analyze the raw logs,
  as well as more advanced analyses on top of this pricing information (for
  example, simulations that determine the cost savings of incorporating
  various sources of price variation).
- `graphs`: Graphs from our analysis; a subset of these graphs are included
  in the paper.

READMEs in each of the sub-directories provide instructions on how to run
the code, how to intepret the logs, and how to perform analyses with the
pricing information.
