import csv
import datetime
import os


results_csv = open('Pardot_Results.csv', 'w', newline='')
results_write = csv.writer(results_csv)
header_list = ['CRM Number','Last Name', 'First Name', 'Company', 'Clicks']
results_write.writerow(header_list)

error_doc = open('error_log.txt', 'a')

'''class Record:
    def __init__(self, last_name,first_name,company_name,crm_num):
        self.last_name = last_name
        self.first_name = first_name
        self.company_name = company_name
        self.crm_num = crm_num'''


def pardot_reader(error):
    output_dict = {}
    debug_count = 0
    for pardot_file in os.listdir('.'):
        if not pardot_file.endswith('.csv'):
            print(f'Skipping... {pardot_file}')
            continue
        elif pardot_file == 'Pardot_Results.csv':
            continue
        else:
            #read the file
            debug_count += 1
            csv_file_obj = open(pardot_file)
            file_reader = csv.reader(csv_file_obj)
            file_list = list(file_reader)

            for row in file_list:
                crmnum = row[37]
                last_name = row[2]
                first_name = row[1]
                company_name = row[4]
                if crmnum == 'CRM Contact FID':
                    continue
                elif crmnum in output_dict:
                    try:
                        output_dict[crmnum]['Clicks'] += 1

                    except: 

                        error.write(f'There was an error in {pardot_file}, with the row {last_name} {first_name}.')
                        print(f'Error found in {pardot_file} and logged.')

                else:
                    output_dict.update({crmnum : dict([('CRM', crmnum), ('Last Name', last_name), ('First Name', first_name), ('Company', company_name), ('Clicks', 1)])})
    print(debug_count)

    for k in output_dict:
        csv_output_list = [output_dict[k]['CRM'],output_dict[k]['Last Name'],output_dict[k]['First Name'],output_dict[k]['Company'],output_dict[k]['Clicks']]
        results_write.writerow(csv_output_list)

pardot_reader(error_doc)






        



#go through each row, create an output dictionary
#pass the dictionary to a writer