import argparse

class Range(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __eq__(self, other):
        return self.start <= other <= self.end

cloud_map = {
    'aws': 'AWS',
    'azure': 'Azure',
    'gcp': 'GCP'
}

continent_map = {
    'north_america': 'North America',
    'europe': 'Europe',
    'asia': 'Asia',
    'south_america': 'South America',
}

def aws(data_transfer_size, intra_region, src_continent, dst_internet):
    # https://aws.amazon.com/ec2/pricing/on-demand/
    data_transfer_cost = 0.0
    if intra_region:
        data_transfer_cost = 0.01 * data_transfer_size
    elif dst_internet:
        if data_transfer_size > 1:
            data_transfer_cost += .25 * min(data_transfer_size - 1,
                                            10000 - 1)
        if data_transfer_size > 10000:
            data_transfer_cost += .23 * min(data_transfer_size - 10000,
                                            50000 - 10000)
        if data_transfer_size > 50000:
            data_transfer_cost += .21 * min(data_transfer_size - 50000,
                                            150000 - 50000)
        if data_transfer_size > 150000:
            data_transfer_cost += .19 * min(data_transfer_size - 150000,
                                            500000 - 150000)
    else:
        if src_continent == 'north_america' or src_continent == 'europe':
            data_transfer_cost = 0.02 * data_transfer_size
        elif src_continent == 'asia':
            data_transfer_cost = 0.08 * data_transfer_size
        elif src_continent == 'south_america':
            data_transfer_cost = 0.16 * data_transfer_size
    return data_transfer_cost


def azure(data_transfer_size, intra_region, src_continent, dst_internet):
    # https://azure.microsoft.com/en-us/pricing/details/bandwidth/
    data_transfer_cost = 0.0
    if not intra_region:
        if src_continent == 'north_america' or src_continent == 'europe':
            if data_transfer_size > 5:
                data_transfer_cost += .087 * min(data_transfer_size - 5,
                                                 10000 - 5)
            if data_transfer_size > 10000:
                data_transfer_cost += .083 * min(data_transfer_size - 10000,
                                                 50000 - 10000)
            if data_transfer_size > 50000:
                data_transfer_cost += .07 * min(data_transfer_size - 50000,
                                                 150000 - 50000)
            if data_transfer_size > 150000:
                data_transfer_cost += .05 * min(data_transfer_size - 150000,
                                                 500000 - 150000)
        elif src_continent == 'asia':
            if data_transfer_size > 5:
                data_transfer_cost += .12 * min(data_transfer_size - 5,
                                                 10000 - 5)
            if data_transfer_size > 10000:
                data_transfer_cost += .085 * min(data_transfer_size - 10000,
                                                 50000 - 10000)
            if data_transfer_size > 50000:
                data_transfer_cost += .082 * min(data_transfer_size - 50000,
                                                 150000 - 50000)
            if data_transfer_size > 150000:
                data_transfer_cost += .08 * min(data_transfer_size - 150000,
                                                 500000 - 150000)
        elif src_continent == 'south_america':
            if data_transfer_size > 5:
                data_transfer_cost += .181 * min(data_transfer_size - 5,
                                                 10000 - 5)
            if data_transfer_size > 10000:
                data_transfer_cost += .175 * min(data_transfer_size - 10000,
                                                 50000 - 10000)
            if data_transfer_size > 50000:
                data_transfer_cost += .17 * min(data_transfer_size - 50000,
                                                150000 - 50000)
            if data_transfer_size > 150000:
                data_transfer_cost += .16 * min(data_transfer_size - 150000,
                                                500000 - 150000)
    return data_transfer_cost

def gcp(data_transfer_size, intra_region, src_continent, dst_internet):
    # https://cloud.google.com/compute/network-pricing
    data_transfer_cost = 0.0
    if not intra_region:
        if dst_internet:
            data_transfer_cost += min(data_transfer_size * 0.12, 1000 * 0.12)
            if data_transfer_size > 1000:
                data_transfer_cost += .11 * min(data_transfer_size - 1000,
                                                10000 - 1000)
            if data_transfer_size > 10000:
                data_transfer_cost += .08 * data_transfer_size - 10000
        elif src_continent == 'north_america':
            data_transfer_cost = 0.01 * data_transfer_size
        elif src_continent == 'europe':
            data_transfer_cost = 0.02 * data_transfer_size
        elif src_continent == 'asia':
            data_transfer_cost = 0.05 * data_transfer_size
        elif src_continent == 'south_america':
            data_transfer_cost = 0.08 * data_transfer_size
    return data_transfer_cost

def main(args):
    # Data transfer size in GB.
    data_transfer_size = args.model_size * args.num_transfers
    if args.transfer_dataset:
        data_transfer_size += args.dataset_size

    dst_internet = args.src_cloud != args.dst_cloud

    data_transfer_cost = 0.0

    if args.src_cloud == 'aws':
        data_transfer_cost += \
            aws(data_transfer_size * args.src_to_dst_fraction,
                args.intra_region, args.src_continent, dst_internet)
    elif args.src_cloud == 'azure':
        data_transfer_cost += \
            azure(data_transfer_size * args.src_to_dst_fraction,
                  args.intra_region, args.src_continent, dst_internet)
    elif args.src_cloud == 'gcp':
        data_transfer_cost += \
            gcp(data_transfer_size * args.src_to_dst_fraction,
                args.intra_region, args.src_continent, dst_internet)

    if args.dst_cloud == 'aws':
        data_transfer_cost += \
            aws(data_transfer_size * (1.0 - args.src_to_dst_fraction),
                args.intra_region, args.dst_continent, dst_internet)
    elif args.dst_cloud == 'azure':
        data_transfer_cost += \
            azure(data_transfer_size * (1.0 - args.src_to_dst_fraction),
                  args.intra_region, args.dst_continent, dst_internet)
    elif args.dst_cloud == 'gcp':
        data_transfer_cost += \
            gcp(data_transfer_size * (1.0 - args.src_to_dst_fraction),
                args.intra_region, args.dst_continent, dst_internet)


    if args.output_format == 'human_readable':
        print('')
        print('Analysis using the following selections:')
        if args.transfer_dataset:
            print('Dataset size: %.2f GB' % (args.dataset_size))
        print('Model size: %.2f GB' % (args.model_size))
        if args.intra_region:
            print('%d intra-region transfers '
                  'in %s %s' % (args.num_transfers, cloud_map[args.src_cloud],
                                continent_map[args.src_continent]))
        else:
            num_src_to_dst_transfers = \
                int(args.num_transfers * args.src_to_dst_fraction)
            print('%d transfers from %s %s to '
                  '%s %s' % (num_src_to_dst_transfers,
                             cloud_map[args.src_cloud],
                             continent_map[args.src_continent],
                             cloud_map[args.dst_cloud],
                             continent_map[args.dst_continent]))
            if num_src_to_dst_transfers < args.num_transfers:
                print('%d transfers from %s %s to '
                      '%s %s' % (args.num_transfers - num_src_to_dst_transfers,
                                 cloud_map[args.dst_cloud],
                                 continent_map[args.dst_continent],
                                 cloud_map[args.src_cloud],
                                 continent_map[args.src_continent]))
        print()
        print('-----')
        print()
        print('Total data transfer size: %.2f GB' % (data_transfer_size))
        print('Total data transfer cost: $%.2f' % (data_transfer_cost))
    else:
        print('%s,%f,%f,%d,%f,%s,%s,%s,%s,%s,%f' % (args.transfer_dataset,
                                                    args.dataset_size,
                                                    args.model_size,
                                                    args.num_transfers,
                                                    args.src_to_dst_fraction,
                                                    args.intra_region,
                                                    args.src_cloud,
                                                    args.src_continent,
                                                    args.dst_cloud,
                                                    args.dst_continent,
                                                    data_transfer_cost))


if __name__=='__main__':
    parser = argparse.ArgumentParser(
                description='Determine data transfer costs')
    parser.add_argument('--transfer_dataset', action='store_true',
                        default=False,
                        help='If set, account for cost of transferring dataset')
    parser.add_argument('--dataset_size', type=float, required=True,
                        help='Dataset size (in GB)')
    parser.add_argument('--model_size', type=float, required=True,
                        help='Model size (in GB)')
    parser.add_argument('--num_transfers', type=int, required=True,
                        help='Number of model transfers')
    parser.add_argument('--src_to_dst_fraction', type=float, default=1.0,
                        choices=[Range(0.0, 1.0)],
                        help=('Fraction of transfers from source to '
                              'destination. Remaining transfers are from '
                              'destination to source.'))
    parser.add_argument('--intra_region', action='store_true',
                        default=False,
                        help=('If set, indicates that VMs are all located in '
                              'the same region.'))
    parser.add_argument('--src_cloud', type=str, required=True,
                        choices=['aws', 'azure', 'gcp'], help='Source cloud.')
    parser.add_argument('--dst_cloud', type=str, required=True,
                        choices=['aws', 'azure', 'gcp'],
                        help='Destination cloud.')
    parser.add_argument('--src_continent', type=str, required=True,
                        choices=['north_america', 'europe', 'asia',
                                 'south_america'], help='Source continent')
    parser.add_argument('--dst_continent', type=str, required=True,
                        choices=['north_america', 'europe', 'asia',
                                 'south_america'], help='Destination continent')
    parser.add_argument('--output_format', choices=['human_readable', 'csv'],
                        default='human_readable', help='Output format')
    args = parser.parse_args()

    if (args.intra_region and
        (args.src_cloud != args.dst_cloud or
         args.src_continent != args.dst_continent)):
        raise ValueError('Intra-region analysis must have same source '
                         'and destination regions')

    main(args)
