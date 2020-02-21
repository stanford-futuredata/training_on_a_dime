import subprocess


def get_spot_instance_prices(region, instance_type):
    command = """aws ec2 describe-spot-price-history --no-paginate \\
                 --region %(region)s \\
                 --instance-types %(instance_type)s \\
                 --product-description \"Linux/UNIX\"
    """ % {"region": region, "instance_type": instance_type}
    output = subprocess.check_output(command, shell=True)
    with open("logs/%s/%s.json" % (region, instance_type), 'w') as f:
        f.write(output.decode())

def main():
    for region in ["eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1"]:
        for instance_type in ["p3.2xlarge", "p3.8xlarge", "p3.16xlarge",
                              "p2.xlarge", "p2.8xlarge", "p2.16xlarge"]:
            get_spot_instance_prices(region, instance_type)


if __name__ == '__main__':
    main()
