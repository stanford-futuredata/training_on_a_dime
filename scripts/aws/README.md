# Collecting instance costs for AWS

This sub-directory contains scripts to collect costs for AWS instances.
Both scripts assume that the [AWS command line interface](https://aws.amazon.com/cli/)
is available; `availability.py` in addition assumes that an AWS paying account
is available (instances are launched).

`cost.py` collects current spot instance prices for various instance types
and regions. `cost.py` takes the following arguments,

```bash
python cost.py -h
usage: cost.py [-h] [--regions REGIONS [REGIONS ...]]
               [--instance_types INSTANCE_TYPES [INSTANCE_TYPES ...]]

Get AWS spot instance price

optional arguments:
  -h, --help            show this help message and exit
  --regions REGIONS [REGIONS ...]
                        AWS regions
  --instance_types INSTANCE_TYPES [INSTANCE_TYPES ...]
                        Instance types
```

`availability.py` spins up instances of the desired types in the desired regions,
then pings the instances every 10 minutes to check if the instances are still
alive. If not, a new instance is spun up and the process is repeated. `availability.py`
has the following arguments,

```bash
python availability.py -h
usage: availability.py [-h] [--zones ZONES [ZONES ...]]
                       [--gpu_types GPU_TYPES [GPU_TYPES ...]]
                       [--all_num_gpus ALL_NUM_GPUS [ALL_NUM_GPUS ...]]

Get AWS spot instance availability

optional arguments:
  -h, --help            show this help message and exit
  --zones ZONES [ZONES ...]
                        AWS availability zones
  --gpu_types GPU_TYPES [GPU_TYPES ...]
                        GPU types
  --all_num_gpus ALL_NUM_GPUS [ALL_NUM_GPUS ...]
                        Number of GPUs per instance
```
