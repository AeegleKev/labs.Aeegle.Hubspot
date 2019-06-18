# IMPORTS AND GLOBAL VARS
import csv

file = ['csv/companies.csv', 'UpdateCompanies.csv']


def get_company_csv():
    # VARS DECLARATION
    # header = []

    # STRUCTURE CONTROL
    with open(file[0], encoding='utf-8') as csv_file:
        file_reader = csv.DictReader(csv_file)
        data = []
        for read in file_reader:
            data.append(read)
        # for d in data:
        #     if i >= 1:
        #         break
        #     else:
        #         header.append(d.keys())
        #         i += 1

        # TEST DEBUGGING
        # print(header)

        return data


def write_row(company, state='Default'):
    # UPDATE DOMAIN IN COMPANY DATA
    if state == 'update':
        mail = company['EMailAddress1'].split('@')
        domain = mail[1]
        print(domain)
        company.update({'Domain Name': domain})

    # MAPPING DATA COMPANY
    company = [company['Domain Name']]

    # FILE OPEN IN SESSION
    with open('csv/' + file[1], 'a', newline='\n', encoding='utf-8') as new_csv_file:
        row_data = csv.writer(new_csv_file)

        row_data.writerow(company)


def check_company():
    # VARS DECLARATION
    data_csv = get_company_csv()
    data_csv = data_csv
    i = 0
    j = 0

    # CSV CREATION AND INJECT HEADER
    with open('csv/' + file[1], 'w', newline='\n', encoding='utf-8') as new_csv_file:
        row_header = csv.writer(new_csv_file, delimiter=',',
                                quotechar=',', quoting=csv.QUOTE_MINIMAL)
        row_header.writerow(['Domain Name'])

    # STRUCTURE CONTROL
    for company in data_csv:
        if company['Domain Name'] == '' and company['EMailAddress1'] and company['EMailAddress1'].find('@') != -1:
            write_row(company, 'update')
        elif company['Domain Name']:
            write_row(company)
        else:
            write_row({'Domain Name': 'N/A'})

    # TEST DEBUGGING
    print('CANTIDAD DE COMPANY', len(data_csv))
    print(i)
    print(j)


if __name__ == '__main__':
    check_company()
