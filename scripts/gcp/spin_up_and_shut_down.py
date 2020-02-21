import argparse
import subprocess
import sys


per_gpu_prices = {
    "nvidia-tesla-v100": 0.74,
    "nvidia-tesla-p100": 0.43,
    "nvidia-tesla-k80": 0.135,
}


def get_spot_instance_prices(zone, gpu_type, num_gpus):
    num_cpus = 8 * num_gpus
    memory = 32 * num_gpus
    price = num_gpus * per_gpu_prices[gpu_type] * 1.15  # Additional 15% for cost of vCPUs and memory.
    command = """google-cloud-sdk/bin/gcloud compute instances create test \\
                 --preemptible --accelerator=count=%(num_gpus)d,type=%(gpu_type)s \\
                 --custom-cpu=%(num_cpus)d --custom-memory=%(memory)d --zone=%(zone)s 2>/dev/null""" % {
        "zone": zone, "num_gpus": num_gpus, "gpu_type": gpu_type,
        "num_cpus": num_cpus, "memory": memory,
    }
    try:
        print("Trying to create instance with %d GPU(s) of type %s in zone %s" % (
            num_gpus, gpu_type, zone), file=sys.stderr)
        output = subprocess.check_output(command, shell=True).decode()
        if "RUNNING" in output:
            command = """echo "y" | google-cloud-sdk/bin/gcloud compute instances \\
                         delete test --delete-disks=all --zone=%(zone)s 2>/dev/null""" % {
                "zone": zone,
            }
            output = subprocess.check_output(command, shell=True)
            print("Successfully created instance with %d GPU(s) of type %s in zone %s" % (
                num_gpus, gpu_type, zone), file=sys.stderr)
            print("Zone: %s, GPU type: %s, Number of GPUs: %d, Price per hour: $%.3f" % (
                zone, gpu_type, num_gpus, price))
    except Exception as e:
        print("Could not create instance with %d GPU(s) of type %s in zone %s" % (
            num_gpus, gpu_type, zone), file=sys.stderr)

def main(args):
    for zone in args.zones:
        for gpu_type in args.gpu_types:
            for num_gpus in args.all_num_gpus:
                get_spot_instance_prices(zone, gpu_type, num_gpus)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='Get GCP preemptible instance availability by spinning up instance and immediately shutting them down')
    parser.add_argument('--zones', type=str, nargs='+',
                        default=["us-west1-b", "us-west1-a", "us-east1-a",
                                 "us-east1-c", "us-central1-c"],
                        help='GCP availability zones')
    parser.add_argument('--gpu_types', type=str, nargs='+',
                        default=["nvidia-tesla-v100", "nvidia-tesla-p100",
                                 "nvidia-tesla-k80"],
                        help='GPU types')
    parser.add_argument('--all_num_gpus', type=int, nargs='+',
                        default=[1, 2, 4, 8],
                        help='Number of GPUs per instance')
    args = parser.parse_args()

    main(args)
