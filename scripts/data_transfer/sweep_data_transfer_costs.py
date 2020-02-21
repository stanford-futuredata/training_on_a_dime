import utils

def main():
    all_transfer_dataset = [True, False]
    all_data_sizes = [1, 10, 100, 1000, 10000]
    all_intra_region = [True, False]
    all_clouds = ['aws', 'azure', 'gcp']
    all_continents = ['north_america', 'europe', 'asia', 'south_america']

    print('Data size (GB),Intra-region,Src cloud,Src continent,'
          'Dst cloud,Dst continent')

    for data_size in all_data_sizes:
        for intra_region in all_intra_region:
            for i, src_cloud in enumerate(all_clouds):
                for j, src_continent in enumerate(all_continents):
                    for dst_cloud in all_clouds[i:]:
                        for k, dst_continent in enumerate(all_continents[j:]):
                            if (intra_region and
                                (src_cloud != dst_cloud or
                                 src_continent != dst_continent)):
                                continue
                            result = utils.analyze(data_size, intra_region,
                                                   src_cloud, src_continent,
                                                   dst_cloud, dst_continent)
                            print(result)

if __name__=='__main__':
    main()
