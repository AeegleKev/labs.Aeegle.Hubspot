# IMPORTS AND GLOBAL VARS
import csv
import re
import time

file = ['../csv/contacts2.csv', '../csv/UpdateLanguage.csv']


def get_contact_csv():
    with open(file[0], encoding='utf-8') as csv_file:
        file_reader = csv.DictReader(csv_file)
        data = []
        for read in file_reader:
            data.append(read)

        return data


def write_row(language):
    # FILE OPEN IN SESSION
    with open(file[1], 'a', newline='\n', encoding='utf-8') as new_csv_file:
        row_data = csv.writer(new_csv_file)
        print(language)
        row_data.writerow([language])


def check_contact():
    # VARS DECLARATION
    data_csv = get_contact_csv()
    data_csv = data_csv
    i = 0
    j = 0

    # CSV CREATION AND INJECT HEADER
    with open(file[1], 'w', newline='\n', encoding='utf-8') as new_csv_file:
        row_header = csv.writer(new_csv_file, delimiter=',',
                                quotechar=',', quoting=csv.QUOTE_MINIMAL)
        row_header.writerow(['hs_language'])

    # STRUCTURE CONTROL
    # Lead Subject, FirstName, LastName, Company Name, Description
    k = 0
    pattron = re.compile('[àâçéèêëîïôûùüÿñæœ]')
    for contact in data_csv:
        k += 1
        print(k)
        # if contact['sm_LeadLanguage']:
        #     print('entro a sm')
        #     if contact['sm_LeadLanguage'] == 'French' or contact['sm_LeadLanguage'] == 'french' and contact[
        #         'sm_LeadLanguage'] != 'NULL':
        #         write_row('fr')
        #     else:
        #         if contact['SM_Language']:
        #             if contact['SM_Language'] == 1:
        #                 write_row('fr')
        #             elif contact['SM_Language'] == 2:
        #                 write_row('en-us')
        #             elif contact['SM_Language'] == 'English':
        #                 write_row('en-us')
        #         else:
        #             print('entra al match')
        #             if contact['Lead Subject'] and pattron.search(contact['Lead Subject']) is not None:
        #                 write_row('fr')
        #             elif contact['FirstName'] and pattron.search(contact['FirstName']) is not None:
        #                 write_row('fr')
        #             elif contact['LastName'] and pattron.search(contact['LastName']) is not None:
        #                 write_row('fr')
        #             elif contact['CompanyName'] and pattron.search(contact['CompanyName']) is not None:
        #                 write_row('fr')
        #             elif contact['Description'] and pattron.search(contact['Description']) is not None:
        #                 write_row('fr')
        #             else:
        #                 write_row('en-us')
        # elif contact['SM_Language']:
        #     print('entro a SM')
        #     if contact['SM_Language'] == 1:
        #         write_row('fr')
        #     elif contact['SM_Language'] == 2:
        #         write_row('en-us')
        #     elif contact['SM_Language'] == 'English':
        #         write_row('en-us')
        #
        # else:
        #     print('entra al match')
        #     if contact['Lead Subject'] and pattron.search(contact['Lead Subject']) is not None:
        #         write_row('fr')
        #     elif contact['FirstName'] and pattron.search(contact['FirstName']) is not None:
        #         write_row('fr')
        #     elif contact['LastName'] and pattron.search(contact['LastName']) is not None:
        #         write_row('fr')
        #     elif contact['CompanyName'] and pattron.search(contact['CompanyName']) is not None:
        #         write_row('fr')
        #     elif contact['Description'] and pattron.search(contact['Description']) is notNone:
        #         write_row('fr')
        #     else:
        #         write_row('en-us')

        if contact['sm_LeadLanguage'] or contact['sm_LeadLanguage'] != 'NULL':
            print('Entra a sm_')
            if contact['sm_LeadLanguage'] == 'French' or contact['sm_LeadLanguage'] == 'french':
                write_row('fr')
            elif contact['sm_LeadLanguage'] == 'English' or contact['sm_LeadLanguage'] == 'english':
                write_row('en-us')
            else:
                print('Entra al match de sm_')
                if contact['Lead Subject'] and pattron.search(contact['Lead Subject']) is not None:
                    write_row('fr')
                elif contact['FirstName'] and pattron.search(contact['FirstName']) is not None:
                    write_row('fr')
                elif contact['LastName'] and pattron.search(contact['LastName']) is not None:
                    write_row('fr')
                elif contact['CompanyName'] and pattron.search(contact['CompanyName']) is not None:
                    write_row('fr')
                elif contact['Description'] and pattron.search(contact['Description']) is not None:
                    write_row('fr')
                else:
                    print('English')
                    write_row('en-us')
        else:
            print('Entra al match')
            if contact['Lead Subject'] and pattron.search(contact['Lead Subject']) is not None:

                write_row('fr')
            elif contact['FirstName'] and pattron.search(contact['FirstName']) is not None:
                write_row('fr')
            elif contact['LastName'] and pattron.search(contact['LastName']) is not None:
                write_row('fr')
            elif contact['CompanyName'] and pattron.search(contact['CompanyName']) is not None:
                write_row('fr')
            elif contact['Description'] and pattron.search(contact['Description']) is not None:
                write_row('fr')
            else:
                print('English')
                write_row('en-us')
    # TEST DEBUGGING
    print('CANTIDAD DE COMPANY', len(data_csv))
    print(i)
    print(j)


# def proof():
#     pattron = re.compile('[àâçéèêëîïôûùüÿñæœ]')
#     print(pattron.search('é'))


if __name__ == '__main__':
    check_contact()
