import gzip
import re


def get_tenant_id(config_file):

    regex = r'\{"tenant_id":"(.*?)"\}'

    with gzip.open(config_file) as cf:

        for line in cf:

            if 'tenant_id' in line.decode("utf-8"):
                tenant = re.search(regex,line.decode("utf-8")).group(1)
                print(f'Current Tenant value is: {tenant}')
                break
                
    return tenant


def find_invalid_key(log_file):

    with open(log_file) as lf:

        if "Invalid Key" in lf.read():
            invalid_found = True

        else:
            invalid_found = False
    
    return invalid_found
    

def get_info_from_user():

    cf_name = input('Provide the config file name (.gz format): ')
    lf_name = input('Provide the log file name (.txt format): ')
    
    return cf_name,lf_name


def fix_config_file(serial_number,tenant,config_file):

    with open("new_config.txt",'w') as nc:

        with gzip.open(config_file) as cf:

            for line in cf:

                text_line = line.decode("utf-8")

                if 'tenant_id' in text_line:
                    new_line = text_line.replace(tenant,serial_number)
                    nc.write(new_line)

                else:
                    nc.write(text_line)
    
    print('File saved as: "new_config.txt"')


def main():

    cf,lf = get_info_from_user()

    sn = input('Provide the device serial number: ')

    print('Obtaining tenant value from config file ...')
    tenant = get_tenant_id(cf)
    
    print('Searching on log file for Invalid Key messages ...')
    invalid_found = find_invalid_key(lf)

    if invalid_found:

        print('Invalid Key log found')
        
        if tenant == sn:
            print('Tenant value in config file is correct')
            print('No issues')

        else:
            print('Tenant value in config file is NOT correct, fixing it ...')
            fix_config_file(sn,tenant,cf)

    else:
        print('No invalid key log found!')
        print('No issues')


if __name__ == '__main__':
    main()