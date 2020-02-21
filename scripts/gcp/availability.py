import argparse
from datetime import datetime
import signal
import subprocess
import sys
import time


instances = {}

def signal_handler(sig, frame):
    global instances
    # Clean up all instances when program is interrupted.
    for (zone, gpu_type, num_gpus) in instances:
        [instance_name, _] = instances[(zone, gpu_type, num_gpus)]
        delete_spot_instance(zone, instance_name)
    sys.exit(0)

def launch_spot_instance(zone, gpu_type, num_gpus, instance_name):
    num_cpus = 8 * num_gpus
    memory = 32 * num_gpus
    command = """google-cloud-sdk/bin/gcloud compute instances create %(instance_name)s \\
                 --preemptible --accelerator=count=%(num_gpus)d,type=%(gpu_type)s \\
                 --custom-cpu=%(num_cpus)d --custom-memory=%(memory)d --zone=%(zone)s 2>/dev/null""" % {
        "instance_name": instance_name, "zone": zone, "num_gpus": num_gpus,
        "gpu_type": gpu_type, "num_cpus": num_cpus, "memory": memory,
    }
    try:
        print("[%s] Trying to create instance %s with %d GPU(s) of type %s in zone %s" % (
            datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            instance_name, num_gpus, gpu_type, zone), file=sys.stderr)
        output = subprocess.check_output(command, shell=True).decode()
        if "RUNNING" in output:
            print("[%s] Created instance %s with %d GPU(s) of type %s in zone %s" % (
                datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                instance_name, num_gpus, gpu_type, zone))
            return True
    except Exception as e:
        pass
    print("[%s] Instance %s creation failed" % (
        datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'), instance_name))
    return False

def monitor_spot_instance(zone, instance_name):
    command = """google-cloud-sdk/bin/gcloud compute instances describe %(instance_name)s \\
                 --zone=%(zone)s 2>/dev/null""" % {
        "instance_name": instance_name, "zone": zone,
    }
    try:
        output = subprocess.check_output(command, shell=True).decode()
        if "RUNNING" in output:
            print("[%s] Instance %s running in zone %s" % (
                datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                instance_name, zone))
            return True
    except Exception as e:
        pass
    print("[%s] Instance %s not running in zone %s" % (
        datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'), instance_name, zone))
    # Delete spot instance in case it exists.
    delete_spot_instance(zone, instance_name)
    return False

def delete_spot_instance(zone, instance_name):
    command = """echo "y" | google-cloud-sdk/bin/gcloud compute instances \\
                 delete %(instance_name)s --delete-disks=all \\
                 --zone=%(zone)s 2>/dev/null""" % {
        "instance_name": instance_name,
        "zone": zone,
    }
    try:
        output = subprocess.check_output(command, shell=True)
        print("[%s] Successfully deleted instance %s" % (
            datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'), instance_name))
    except:
        return

def main(args):
    global instances
    i = 0
    for zone in args.zones:
        for gpu_type in args.gpu_types:
            for num_gpus in args.all_num_gpus:
                instances[(zone, gpu_type, num_gpus)] = ["instance%d" % i, False]
                i += 1

    while True:
        # Spin in a loop; try to launch spot instances of particular type if
        # not running already. Check on status of instances, and update to
        # "not running" as needed.
        for (zone, gpu_type, num_gpus) in instances:
            [instance_name, running] = instances[(zone, gpu_type, num_gpus)]
            if not running:
                instances[(zone, gpu_type, num_gpus)][1] = \
                    launch_spot_instance(zone, gpu_type, num_gpus, instance_name)
            instances[(zone, gpu_type, num_gpus)][1] = \
                monitor_spot_instance(zone, instance_name)
        time.sleep(600)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='Get GCP preemptible instance availability')
    parser.add_argument('--zones', type=str, nargs='+',
                        default=["us-west1-b", "us-east1-c", "us-central1-c"],
                        help='GCP availability zones')
    parser.add_argument('--gpu_types', type=str, nargs='+',
                        default=["nvidia-tesla-v100", "nvidia-tesla-p100",
                                 "nvidia-tesla-k80"],
                        help='GPU types')
    parser.add_argument('--all_num_gpus', type=int, nargs='+',
                        default=[1, 2, 4, 8],
                        help='Number of GPUs per instance')
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    main(args)
