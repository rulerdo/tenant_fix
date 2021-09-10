import gzip
import re
import os

def get_tenant_id(config_file):

    regex = r'\{"tenant_id":"(.*?)"\}'

    with gzip.open(config_file,'rt') as cf:

        for line in cf:

            if 'tenant_id' in line:
                tenant = re.search(regex,line).group(1)
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

    with gzip.open(config_file,'wt') as nc:

        with gzip.open(old_config,'rt') as old_cf:

            for line in old_cf:

                if 'tenant_id' in line:
                    new_line = line.replace(tenant,serial_number)
                    nc.write(new_line)

                else:
                    nc.write(line)
    
    print(f'Updated file saved as: "{config_file}"')


def post_checks(config_file,serial_number):

    tenant = get_tenant_id(config_file)

    if tenant == serial_number:
        response = f'Post checks OK!'

    else:
        response = 'Something went wrong!'

    return response


def rollback_config_files(config_file):

    os.remove(config_file)
    print('New config file deleted')

    os.rename('OLD_' + config_file, config_file)
    print('Original config file name reverted')


def print_config_file(config_file):

    print('Printing NEW config file:\n')
    with gzip.open(config_file,'rt') as cf:

        x = cf.read()
        print(x)


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

    # Uncomment next 2 lines to troubleshot issues with config files
    # print_config_file(cf)
    # print_config_file('OLD_' + cf)

    print('Performing post checks ...')
    response = post_checks(cf,sn)
    print(response)

    if response == 'Something went wrong!':
        print('Rolling back config file changes ...')
        rollback_config_files(cf)


if __name__ == '__main__':
    main()
