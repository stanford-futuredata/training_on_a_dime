import subprocess

def analyze(data_size, intra_region, src_cloud, src_continent,
            dst_cloud, dst_continent):
    if intra_region:
        intra_region_str = '--intra_region'
    else:
        intra_region_str = ''
    command = ('python query_data_transfer_costs.py --data_size %f '
               '%s --src_cloud %s --src_continent %s --dst_cloud %s '
               '--dst_continent %s '
               '--output_format csv') % (data_size,
                                         intra_region_str,
                                         src_cloud,
                                         src_continent,
                                         dst_cloud,
                                         dst_continent)
    output = subprocess.check_output(command, shell=True).strip()
    return output.decode('utf-8')
