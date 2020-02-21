# Collecting instance costs and estimating availability for GCP

This sub-directory contains scripts to collect costs and estimate availability for GCP instances.
Both scripts assume that the [GCloud command line interface](https://cloud.google.com/sdk)
is available, and that a GCP paying account is available (instances are launched).

`spin_up_and_shut_down.py` attempts to spin up a preemptible instance on GCP,
and immediately shuts the instance down if successful -- the goal here is to
measure the time fraction instance requests are granted.
`spin_up_and_shut_down.py` takes the following arguments,

```bash
python spin_up_and_shut_down.py -h
usage: spin_up_and_shut_down.py [-h] [--zones ZONES [ZONES ...]]
                                [--gpu_types GPU_TYPES [GPU_TYPES ...]]
                                [--all_num_gpus ALL_NUM_GPUS [ALL_NUM_GPUS ...]]

Get GCP preemptible instance availability by spinning up instance and
immediately shutting them down

optional arguments:
  -h, --help            show this help message and exit
  --zones ZONES [ZONES ...]
                        GCP availability zones
  --gpu_types GPU_TYPES [GPU_TYPES ...]
                        GPU types
  --all_num_gpus ALL_NUM_GPUS [ALL_NUM_GPUS ...]
                        Number of GPUs per instance
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

Get GCP preemptible instance availability

optional arguments:
  -h, --help            show this help message and exit
  --zones ZONES [ZONES ...]
                        GCP availability zones
  --gpu_types GPU_TYPES [GPU_TYPES ...]
                        GPU types
  --all_num_gpus ALL_NUM_GPUS [ALL_NUM_GPUS ...]
                        Number of GPUs per instance
```
