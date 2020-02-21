# Cost of data transfer

This sub-directory contains scripts to measure the cost of transferring data within and out of each public cloud. The data transfer costs were collected from these sources:

| Cloud |                  Data Transfer Costs Source                  |
|:-----:|:------------------------------------------------------------:|
| AWS   | https://aws.amazon.com/ec2/pricing/on-demand/                |
| Azure | https://azure.microsoft.com/en-us/pricing/details/bandwidth/ |
| GCP   | https://cloud.google.com/compute/network-pricing             |

`query_data_transfer_costs.py` calculates the data transfer cost for a given data size and source / destination combination, given the following arguments:
```bash
python query_data_transfer_costs.py -h
usage: query_data_transfer_costs.py [-h] --data_size DATA_SIZE
                                    [--intra_region] --src_cloud
                                    {aws,azure,gcp} --dst_cloud
                                    {aws,azure,gcp,internet} --src_continent
                                    {north_america,europe,asia,south_america}
                                    --dst_continent
                                    {north_america,europe,asia,south_america}
                                    [--output_format {human_readable,csv}]

Calculate data transfer costs

optional arguments:
  -h, --help            show this help message and exit
  --data_size DATA_SIZE
                        Data size in GB
  --intra_region        If set, indicates that VMs are all located in the same
                        region.
  --src_cloud {aws,azure,gcp}
                        Source cloud.
  --dst_cloud {aws,azure,gcp,internet}
                        Destination cloud.
  --src_continent {north_america,europe,asia,south_america}
                        Source continent
  --dst_continent {north_america,europe,asia,south_america}
                        Destination continent
  --output_format {human_readable,csv}
                        Output format
```

`sweep_data_transfer_costs.py` sweeps over a specified list of data size and source / destination combinations.
