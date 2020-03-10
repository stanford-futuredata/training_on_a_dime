def aws(data_size, intra_region, src_continent, dst_internet):
    # https://aws.amazon.com/ec2/pricing/on-demand/
    if data_size <= 0.0:
        return 0.0
    data_transfer_cost = 0.0
    if intra_region:
        data_transfer_cost = 0.01 * data_size
    elif dst_internet:
        if src_continent == 'north_america' or src_continent == 'europe':
            if data_size > 1:
                data_transfer_cost += .09 * min(data_size - 1,
                                                10000 - 1)
            if data_size > 10000:
                data_transfer_cost += .085 * min(data_size - 10000,
                                                 50000 - 10000)
            if data_size > 50000:
                data_transfer_cost += .07 * min(data_size - 50000,
                                                150000 - 50000)
            if data_size > 150000:
                data_transfer_cost += .05 * min(data_size - 150000,
                                                500000 - 150000)
        elif src_continent == 'asia':
            if data_size > 1:
                data_transfer_cost += .114 * min(data_size - 1,
                                                 10000 - 1)
            if data_size > 10000:
                data_transfer_cost += .089 * min(data_size - 10000,
                                                 50000 - 10000)
            if data_size > 50000:
                data_transfer_cost += .086 * min(data_size - 50000,
                                                 150000 - 50000)
            if data_size > 150000:
                data_transfer_cost += .084 * min(data_size - 150000,
                                                 500000 - 150000)
        elif src_continent == 'south_america':
            if data_size > 1:
                data_transfer_cost += .25 * min(data_size - 1,
                                                10000 - 1)
            if data_size > 10000:
                data_transfer_cost += .23 * min(data_size - 10000,
                                                50000 - 10000)
            if data_size > 50000:
                data_transfer_cost += .21 * min(data_size - 50000,
                                                150000 - 50000)
            if data_size > 150000:
                data_transfer_cost += .19 * min(data_size - 150000,
                                                500000 - 150000)

    else:
        if src_continent == 'north_america' or src_continent == 'europe':
            data_transfer_cost = 0.02 * data_size
        elif src_continent == 'asia':
            data_transfer_cost = 0.08 * data_size
        elif src_continent == 'south_america':
            data_transfer_cost = 0.16 * data_size
    return data_transfer_cost


def azure(data_size, intra_region, src_continent, dst_internet):
    # https://azure.microsoft.com/en-us/pricing/details/bandwidth/
    if data_size <= 0.0:
        return 0.0
    data_transfer_cost = 0.0
    if not intra_region:
        if src_continent == 'north_america' or src_continent == 'europe':
            if data_size > 5:
                data_transfer_cost += .087 * min(data_size - 5,
                                                 10000 - 5)
            if data_size > 10000:
                data_transfer_cost += .083 * min(data_size - 10000,
                                                 50000 - 10000)
            if data_size > 50000:
                data_transfer_cost += .07 * min(data_size - 50000,
                                                 150000 - 50000)
            if data_size > 150000:
                data_transfer_cost += .05 * min(data_size - 150000,
                                                 500000 - 150000)
        elif src_continent == 'asia':
            if data_size > 5:
                data_transfer_cost += .12 * min(data_size - 5,
                                                 10000 - 5)
            if data_size > 10000:
                data_transfer_cost += .085 * min(data_size - 10000,
                                                 50000 - 10000)
            if data_size > 50000:
                data_transfer_cost += .082 * min(data_size - 50000,
                                                 150000 - 50000)
            if data_size > 150000:
                data_transfer_cost += .08 * min(data_size - 150000,
                                                 500000 - 150000)
        elif src_continent == 'south_america':
            if data_size > 5:
                data_transfer_cost += .181 * min(data_size - 5,
                                                 10000 - 5)
            if data_size > 10000:
                data_transfer_cost += .175 * min(data_size - 10000,
                                                 50000 - 10000)
            if data_size > 50000:
                data_transfer_cost += .17 * min(data_size - 50000,
                                                150000 - 50000)
            if data_size > 150000:
                data_transfer_cost += .16 * min(data_size - 150000,
                                                500000 - 150000)
    return data_transfer_cost

def gcp(data_size, intra_region, src_continent, dst_internet):
    # https://cloud.google.com/compute/network-pricing
    if data_size <= 0.0:
        return 0.0
    data_transfer_cost = 0.0
    if not intra_region:
        if dst_internet:
            if src_continent == 'asia':
                data_transfer_cost += min(data_size * 0.147, 1000 * 0.147)
                if data_size > 1000:
                    data_transfer_cost += .147 * min(data_size - 1000,
                                                     10000 - 1000)
                if data_size > 10000:
                    data_transfer_cost += .134 * data_size - 10000 
            else:
                data_transfer_cost += min(data_size * 0.12, 1000 * 0.12)
                if data_size > 1000:
                    data_transfer_cost += .11 * min(data_size - 1000,
                                                    10000 - 1000)
                if data_size > 10000:
                    data_transfer_cost += .08 * data_size - 10000
        elif src_continent == 'north_america':
            data_transfer_cost = 0.01 * data_size
        elif src_continent == 'europe':
            data_transfer_cost = 0.02 * data_size
        elif src_continent == 'asia':
            data_transfer_cost = 0.05 * data_size
        elif src_continent == 'south_america':
            data_transfer_cost = 0.08 * data_size
    return data_transfer_cost
