import argparse
from datetime import datetime
import signal
import json
import subprocess
import sys
import time


instances = {}
instance_types = {
    ("v100", 1): "p3.2xlarge",
    ("v100", 4): "p3.8xlarge",
    ("v100", 8): "p3.16xlarge",
    ("k80", 1): "p2.xlarge",
    ("k80", 8): "p2.8xlarge",
    ("k80", 16): "p2.16xlarge",
}

def signal_handler(sig, frame):
    global instances
    # Clean up all instances when program is interrupted.
    for (zone, gpu_type, num_gpus) in instances:
        [instance_id, _] = instances[(zone, gpu_type, num_gpus)]
        if instance_id is not None:
            delete_spot_instance(zone, instance_id)
    sys.exit(0)

def launch_spot_instance(zone, gpu_type, num_gpus, instance_id):
    instance_type = instance_types[(gpu_type, num_gpus)]
    with open("specification.json.template", 'r') as f1, open("specification.json", 'w') as f2:
        template = f1.read()
        specification_file = template % (instance_type, zone)
        f2.write(specification_file)
    command = """aws ec2 request-spot-instances --instance-count 1 --type one-time --launch-specification file://specification.json"""
    try:
        spot_instance_request_id = None
        print("[%s] Trying to create instance with %d GPU(s) of type %s in zone %s" % (
            datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            num_gpus, gpu_type, zone), file=sys.stderr)
        output = subprocess.check_output(command, shell=True).decode()
        return_obj = json.loads(output)
        spot_instance_request_id = return_obj["SpotInstanceRequests"][0]["SpotInstanceRequestId"]
        command = """aws ec2 describe-spot-instance-requests --spot-instance-request-id %s""" % (
            spot_instance_request_id)
        time.sleep(30)
        output = subprocess.check_output(command, shell=True).decode()
        return_obj = json.loads(output)
        instance_id = return_obj["SpotInstanceRequests"][0]["InstanceId"]
        print("[%s] Created instance %s with %d GPU(s) of type %s in zone %s" % (
            datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            instance_id, num_gpus, gpu_type, zone))
        return [instance_id, True]
    except Exception as e:
        pass
    if spot_instance_request_id is not None:
        command = """aws ec2 cancel-spot-instance-requests --spot-instance-request-ids %s""" % (
            spot_instance_request_id)
        subprocess.check_output(command, shell=True)
    print("[%s] Instance with %d GPU(s) of type %s creation failed" % (
        datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'), num_gpus, gpu_type))
    return [None, False]

def monitor_spot_instance(zone, instance_id):
    command = """aws ec2 describe-instances --instance-id %(instance_id)s""" % {
        "instance_id": instance_id,
    }
    try:
        output = subprocess.check_output(command, shell=True).decode()
        if "running" in output:
            print("[%s] Instance %s running in zone %s" % (
                datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                instance_id, zone))
            return True
    except Exception as e:
        pass
    print("[%s] Instance %s not running in zone %s" % (
        datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'), instance_id, zone))
    # Delete spot instance in case it exists.
    delete_spot_instance(zone, instance_id)
    return False

def delete_spot_instance(zone, instance_id):
    command = """aws ec2 terminate-instances --instance-ids %(instance_id)s""" % {
        "instance_id": instance_id,
    }
    try:
        output = subprocess.check_output(command, shell=True)
        print("[%s] Successfully deleted instance %s" % (
            datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'), instance_id))
    except:
        return

def main(args):
    global instances
    for zone in args.zones:
        for gpu_type in args.gpu_types:
            for num_gpus in args.all_num_gpus:
                instances[(zone, gpu_type, num_gpus)] = [None, False]

    while True:
        # Spin in a loop; try to launch spot instances of particular type if
        # not running already. Check on status of instances, and update to
        # "not running" as needed.
        for (zone, gpu_type, num_gpus) in instances:
            [instance_id, running] = instances[(zone, gpu_type, num_gpus)]
            if instance_id is not None:
                running = \
                    monitor_spot_instance(zone, instance_id)
            if not running:
                [instance_id, running] = \
                    launch_spot_instance(zone, gpu_type, num_gpus, instance_id)
            instances[(zone, gpu_type, num_gpus)] = [instance_id, running]
        time.sleep(600)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='Get AWS spot instance availability')
    parser.add_argument('--zones', type=str, nargs='+',
                        default=["us-east-1b", "us-east-1c"],
                        help='AWS availability zones')
    parser.add_argument('--gpu_types', type=str, nargs='+',
                        default=["v100", "k80"],
                        help='GPU types')
    parser.add_argument('--all_num_gpus', type=int, nargs='+',
                        default=[1, 8],
                        help='Number of GPUs per instance')
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    main(args)
