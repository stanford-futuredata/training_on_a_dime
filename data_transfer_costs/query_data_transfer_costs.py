import argparse

import data_transfer_costs

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

def main(args):
    # Data transfer size in GB.
    dst_internet = args.src_cloud != args.dst_cloud

    if args.src_cloud == 'aws':
        data_transfer_cost = data_transfer_costs.aws(args.data_size,
                                                     args.intra_region,
                                                     args.src_continent,
                                                     dst_internet)
    elif args.src_cloud == 'azure':
        data_transfer_cost = data_transfer_costs.azure(args.data_size,
                                                       args.intra_region,
                                                       args.src_continent,
                                                       dst_internet)
    elif args.src_cloud == 'gcp':
        data_transfer_cost = data_transfer_costs.gcp(args.data_size,
                                                     args.intra_region,
                                                     args.src_continent,
                                                     dst_internet)

    if args.output_format == 'human_readable':
        if args.intra_region:
            print('Cost of intra-region transfer of %f GB in'
                  '%s %s: $%.2f' % (args.data_size, cloud_map[args.src_cloud],
                                    continent_map[args.src_continent],
                                    data_transfer_cost))
        else:
            print('Cost of transfer of %f GB from %s %s to '
                  '%s %s: $%.2f' % (args.data_size, cloud_map[args.src_cloud],
                                    continent_map[args.src_continent],
                                    cloud_map[args.dst_cloud],
                                    continent_map[args.dst_continent],
                                    data_transfer_cost))
    else:
        print('%f,%s,%s,%s,%s,%s,%f' % (args.data_size,
                                        args.intra_region,
                                        args.src_cloud,
                                        args.src_continent,
                                        args.dst_cloud,
                                        args.dst_continent,
                                        data_transfer_cost))


if __name__=='__main__':
    parser = argparse.ArgumentParser(
                description='Determine data transfer costs')
    parser.add_argument('--data_size', type=float, required=True,
                        help='Data size in GB')
    parser.add_argument('--intra_region', action='store_true',
                        default=False,
                        help=('If set, indicates that VMs are all located in '
                              'the same region.'))
    parser.add_argument('--src_cloud', type=str, required=True,
                        choices=['aws', 'azure', 'gcp'], help='Source cloud.')
    parser.add_argument('--dst_cloud', type=str, required=True,
                        choices=['aws', 'azure', 'gcp', 'internet'],
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
