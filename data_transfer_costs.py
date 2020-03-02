import argparse

continent_map = {
    'north_america': 'North America',
    'europe': 'Europe',
    'asia': 'Asia',
    'south_america': 'South America',
}

def aws(data_transfer_size):
    data_transfer_cost = 0.0
    if not args.inter_region:
        data_transfer_cost = 0.01 * data_transfer_size
    else:
        if args.continent == 'north_america':
            data_transfer_cost = 0.02 * data_transfer_size
        elif args.continent == 'europe':
            data_transfer_cost = 0.02 * data_transfer_size
        elif args.continent == 'asia':
            data_transfer_cost = 0.08 * data_transfer_size
        elif args.continent == 'south_america':
            data_transfer_cost = 0.16 * data_transfer_size
    return data_transfer_cost


def azure(data_transfer_size):
    data_transfer_cost = 0.0
    if not args.inter_region:
        if args.continent == 'north_america' or args.continent == 'europe':
            if data_transfer_size > 5 and data_transfer_size <= 10000:
                data_transfer_cost += .087 * min(data_transfer_size - 5,
                                                 10000 - 5)
            if data_transfer_size > 10000 and data_transfer_size <= 50000:
                data_transfer_cost += .083 * min(data_transfer_size - 10000,
                                                 50000 - 10000)
            if data_transfer_size > 50000 and data_transfer_size <= 150000:
                data_transfer_cost += .07 * min(data_transfer_size - 50000,
                                                 150000 - 50000)
            if data_transfer_size > 150000 and data_transfer_size <= 500000:
                data_transfer_cost += .05 * min(data_transfer_size - 150000,
                                                 500000 - 150000)
        elif args.continent == 'asia':
            if data_transfer_size > 5 and data_transfer_size <= 10000:
                data_transfer_cost += .12 * min(data_transfer_size - 5,
                                                 10000 - 5)
            if data_transfer_size > 10000 and data_transfer_size <= 50000:
                data_transfer_cost += .085 * min(data_transfer_size - 10000,
                                                 50000 - 10000)
            if data_transfer_size > 50000 and data_transfer_size <= 150000:
                data_transfer_cost += .082 * min(data_transfer_size - 50000,
                                                 150000 - 50000)
            if data_transfer_size > 150000 and data_transfer_size <= 500000:
                data_transfer_cost += .08 * min(data_transfer_size - 150000,
                                                 500000 - 150000)
        elif args.continent == 'south_america':
            if data_transfer_size > 5 and data_transfer_size <= 10000:
                data_transfer_cost += .181 * min(data_transfer_size - 5,
                                                 10000 - 5)
            if data_transfer_size > 10000 and data_transfer_size <= 50000:
                data_transfer_cost += .175 * min(data_transfer_size - 10000,
                                                 50000 - 10000)
            if data_transfer_size > 50000 and data_transfer_size <= 150000:
                data_transfer_cost += .17 * min(data_transfer_size - 50000,
                                                150000 - 50000)
            if data_transfer_size > 150000 and data_transfer_size <= 500000:
                data_transfer_cost += .16 * min(data_transfer_size - 150000,
                                                500000 - 150000)
    return data_transfer_cost

def gcp(data_transfer_size):
    data_transfer_cost = 0.0
    if not args.inter_region:
        if args.continent == 'north_america':
            data_transfer_cost = 0.01 * data_transfer_size
        elif args.continent == 'europe':
            data_transfer_cost = 0.02 * data_transfer_size
        elif args.continent == 'asia':
            data_transfer_cost = 0.05 * data_transfer_size
        elif args.continent == 'south_america':
            data_transfer_cost = 0.08 * data_transfer_size
    return data_transfer_cost

def main(args):
    data_transfer_size = args.model_size * args.num_transfers
    if args.transfer_dataset:
        data_transfer_size += args.dataset_size

    aws_results = aws(data_transfer_size)
    azure_results = azure(data_transfer_size)
    gcp_results = gcp(data_transfer_size)

    if args.output_format == 'human_readable':
        print('')
        print('Analysis using the following selections:')
        print('Dataset size: %.2f GB' % (args.dataset_size))
        print('Model size: %.2f GB' % (args.model_size))
        transfer_type = 'inter-region' if args.inter_region else 'intra-region'
        continent_type = 'in %s' % (continent_map[args.continent])
        print('%d %s transfers %s' % (args.num_transfers, transfer_type,
                                      continent_type))
        print('')
        print('-----')
        print('')
        print('Total data transfer size: %.2f GB' % (data_transfer_size))
        print('')

        print('AWS:')
        print('Data transfer cost: $%.2f' % (aws_results))
        print('')

        print('Azure:')
        print('Data transfer cost: $%.2f' % (azure_results))
        print('')

        print('GCP:')
        print('Data transfer cost: $%.2f' % (gcp_results))
        print('')
    else:
        print('%f,%f,%s,%s,%d,%f,%f,%f' % (args.dataset_size, args.model_size,
                                           args.inter_region, args.continent,
                                           args.num_transfers, aws_results,
                                           azure_results, gcp_results))


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
    parser.add_argument('--inter_region', action='store_true',
                        default=False,
                        help=('If set, indicates that VMs are spread between '
                              'different regions.'))
    parser.add_argument('--continent',
                        choices=['north_america', 'europe', 'asia',
                                 'south_america',],
                        required=True,
                        help=('Which continent the VMs are located in'))
    parser.add_argument('--output_format', choices=['human_readable', 'csv'],
                        default='human_readable', help='Output format')
    args = parser.parse_args()
    main(args)
