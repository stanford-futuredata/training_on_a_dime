import argparse
import datetime
import subprocess


def get_spot_instance_prices(region, instance_type):
    command = """aws ec2 describe-spot-price-history --no-paginate \\
                 --region %(region)s \\
                 --instance-types %(instance_type)s \\
                 --product-description \"Linux/UNIX\" \\
                 --start-time %(start_time)s --end-time %(end_time)s
    """ % {"region": region, "instance_type": instance_type,
           "start_time": (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S"),
           "end_time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}
    output = subprocess.check_output(command, shell=True)
    with open("../../logs/aws/cost/%s/%s.%s.json" % (
            region,
            datetime.datetime.now().strftime("%Y-%m-%d"),
            instance_type), 'w') as f:
        f.write(output.decode())

def main(args):
    for region in args.regions:
        for instance_type in args.instance_types:
            get_spot_instance_prices(region, instance_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                description='Get AWS spot instance price')
    parser.add_argument('--regions', type=str, nargs='+',
                        default=["us-east-1", "us-east-2", "us-west-1",
                                 "us-west-2", "eu-central-1", "eu-west-1",
                                 "eu-west-2", "eu-west-3", "eu-north-1"],
                        help='AWS regions')
    parser.add_argument('--instance_types', type=str, nargs='+',
                        default=["p3.2xlarge", "p3.8xlarge", "p3.16xlarge",
                                 "p2.xlarge", "p2.8xlarge", "p2.16xlarge"],
                        help='Instance types')
    args = parser.parse_args()

    main(args)
