# Pricing analysis

The notebooks in this directory analyze the pricing logs we collected over
February and March 2020.

- `aws.ipynb`, `azure.ipynb`, and `gcp.ipynb` analyze the variation of per-hour
  price of spot or preemptible instances with time, as well as the change in
  availability.
- `overlaid.ipynb` shows the prices for the same instance types across cloud
  providers.
- `normalized_throughput_per_cost.ipynb` shows throughput and dollar-normalized
  throughput for various models, using GCP on-demand prices.
- `single_job_cost_analysis.ipynb` runs more complicated simulations that
  try to estimate the cost reductions that would be achieved if one were to
  leverage these different sources of price variation, for different model types.
