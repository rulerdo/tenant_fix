import gzip
import re
import os

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
    

def get_config_file_name():

    cf_name = input('Provide the config file name (.gz format): ')
    
    return cf_name



def get_log_file_name():

    lf_name = input('Provide the log file name (.txt format): ')
    
    return lf_name


def get_serial_number():
    
    sn = input('Provide the device serial number: ')
    
    return sn


def fix_config_file(serial_number,tenant,config_file):
    
    old_config = 'OLD_' + config_file
    os.rename(config_file, old_config)
    
    print(f'Old config file renamed to: "{old_config}"')

    with gzip.open(config_file,'wb') as nc:

        with gzip.open(old_config,'rt') as old_cf:

            for line in old_cf:

                if 'tenant_id' in line:
                    new_line = line.replace(tenant,serial_number)
                    nc.write(new_line)

                else:
                    nc.write(line)
    
    print(f'Updated file saved as: "{config_file}"')


def main():

    cf = get_config_file_name()
    
    lf = get_log_file_name()

    sn = get_serial_number()

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
