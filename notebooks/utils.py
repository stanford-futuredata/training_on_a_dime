import csv
from datetime import datetime
import os
import json

def get_timestamp(timestamp):
    return datetime.strptime(
        datetime.strftime(
            datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.000Z'),
            '%Y-%m-%d'
        ),
        '%Y-%m-%d'
    )

def read_aws_prices(directory, summary=True):
    per_instance_type_spot_prices = {}
    for filename in os.listdir(directory):
        full_filepath = os.path.join(directory, filename)
        with open(full_filepath, 'r') as f:
            json_obj = json.load(f)
            for x in json_obj['SpotPriceHistory']:
                instance_type = x['InstanceType']
                if instance_type not in per_instance_type_spot_prices:
                    per_instance_type_spot_prices[instance_type] = []
                x['Timestamp'] = get_timestamp(x['Timestamp'])
                per_instance_type_spot_prices[instance_type].append(x)
    per_instance_type_spot_prices_summary = {}
    for instance_type in per_instance_type_spot_prices:
        spot_prices = [
            float(x['SpotPrice']) for x in per_instance_type_spot_prices[instance_type]]
        per_instance_type_spot_prices_summary[instance_type] = [
            max(spot_prices), min(spot_prices)
        ]
    if summary:
        return per_instance_type_spot_prices_summary
    else:
        return per_instance_type_spot_prices
    
def read_azure_prices(directory):
    per_instance_type_spot_prices = {}
    for filename in os.listdir(directory):
        full_filepath = os.path.join(directory, filename)
        with open(full_filepath, 'r') as f:
            zone = filename.replace(".csv", "")
            reader = csv.reader(f)
            i = 0
            for row in reader:
                if i == 0:
                    header = row
                    for header_elem in header[1:]:
                        if header_elem not in per_instance_type_spot_prices:
                            per_instance_type_spot_prices[header_elem] = []
                else:
                    for (header_elem, row_elem) in zip(header[1:], row[1:]):
                        per_instance_type_spot_prices[header_elem].append(
                            (zone, datetime.strptime(row[0], '%m/%d/%Y'), row_elem))
                i += 1
    return per_instance_type_spot_prices

def read_azure_instance_mapping_file(filepath):
    instance_mapping = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i > 0:
                instance_mapping[row[0]] = (row[1].lower(), int(row[2]))
            i += 1
    return instance_mapping

def read_gcp_prices(directory):
    per_instance_type_spot_prices = {}
    for filename in os.listdir(directory):
        try:
            full_filepath = os.path.join(directory, filename)
            timestamp = datetime.strptime(filename.replace(".out", ""),
                                          '%Y-%m-%dT%H:%M:%S.000Z')
            with open(full_filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    [zone, instance_type, num_gpus, price_per_hour] = [
                        x.split(": ")[1] for x in line.split(", ")]
                    num_gpus = int(num_gpus)
                    if (instance_type, num_gpus) not in per_instance_type_spot_prices:
                        per_instance_type_spot_prices[(instance_type, num_gpus)] = []
                    per_instance_type_spot_prices[(instance_type, num_gpus)].append(
                        (zone, price_per_hour, timestamp)
                    )
        except Exception as e:
            continue
    return per_instance_type_spot_prices