import csv
import json
import time

import requests
import re

# Global vars
csv_file = ['../csv/Contacts.csv']
host = 'https://api.hubapi.com'
hapikey = '8a7b8099-d61e-402d-ac36-0f1098d0c0c0'


# Open .csv file and load in memory
def get_csv_contacts():
    with open(csv_file[0], encoding='utf-8') as file_contact:
        file_read = csv.DictReader(file_contact)
        data = []
        for row in file_read:
            data.append(row)

        # Return a Dictionary with all contact data
        return data


# Compare contacts
def compare_contact(contact):
    pattron = re.compile('[0-9-]')
    data = {'firstname': '', 'lastname': '', 'email': '', 'company': '', 'jobtitle': '', 'phone': '', 'hs_language': '',
            'description': '', 'mobilephone': '', 'website': '', 'industry': 'Municipal', 'city': '', 'leadsubject': ''}

    if contact['FirstName']:
        data.update({'firstname': contact['FirstName']})

    if contact['LastName']:
        data.update({'lastname': contact['LastName']})

    if contact['EMailAddress1'].find('@') != -1:
        data.update({'email': contact['EMailAddress1']})

    if contact['CompanyName'] and contact['CompanyName'] != 'NULL':
        data.update({'company': contact['CompanyName']})

    if contact['JobTitle'] != 'NULL':
        data.update({'jobtitle': contact['JobTitle']})

    if contact['Telephone1']:
        data.update({'phone': contact['Telephone1']})

    if contact['hs_language'] and contact['hs_language'] != 'NULL':
        data.update({'hs_language': contact['hs_language']})

    if contact['Description'] != 'NULL':
        data.update({'description': contact['Description']})

    if contact['MobilePhone'] != 'NULL' and pattron.match(str(contact['MobilePhone'])) is None:
        data.update({'mobilephone': contact['MobilePhone']})

    if contact['WebSiteUrl']:
        if contact['WebSiteUrl'] != 'NULL':
            data.update({'website': contact['WebSiteUrl']})

    if contact['Industry']:
        if contact['Industry'] != 'NULL':
            data.update({'industry': contact['Industry']})
    else:
        if contact['Lead Subject']:
            if contact['Lead Subject'].find('Airport') != -1:
                data.update({'industry': 'Airport'})
        elif contact['CompanyName']:
            if contact['CompanyName'].find('Airport') != -1:
                data.update({'industry': 'Airport'})
        elif contact['Description']:
            if contact['Description'].find('Airport') != -1:
                data.update({'industry': 'Airport'})
        elif contact['JobTitle']:
            if contact['JobTitle'].find('Airport') != -1:
                data.update({'industry': 'Airport'})

    if contact['City'] and contact['City'] != '#REF!' and contact['City'] != '#¡REF!':
        data.update({'city': contact['City']})
    else:
        if contact['Lead Subject']:
            if contact['Lead Subject'].find('City') != -1 or contact['Lead Subject'].find('city') != -1:
                data.update({'city': contact['Lead Subject']})
        elif contact['CompanyName']:
            if contact['CompanyName'].find('City') != -1 or contact['CompanyName'].find('city') != -1:
                data.update({'city': contact['CompanyName']})
        elif contact['Insured']:
            if contact['Insured'].find('City') != -1 or contact['Insured'].find('city') != -1:
                data.update({'city': contact['Insured']})

    if contact['Lead Subject']:
        if contact['Lead Subject'] != 'NULL':
            data.update({'leadsubject': contact['Lead Subject']})

    return data


def json_POST(contact):
    contact_data = {
        "properties": [
            {
                "property": "firstname",
                "value": contact['firstname'],
            },
            {
                "property": "lastname",
                "value": contact['lastname'],
            },
            {
                "property": "email",
                "value": contact['email'],
            },
            {
                "property": "company",
                "value": contact['company'],
            },
            {
                "property": "jobtitle",
                "value": contact['jobtitle'],
            },
            {
                "property": "phone",
                "value": contact['phone'],
            },
            {
                "property": "hs_language",
                "value": contact['hs_language'],
            },
            {
                "property": "description",
                "value": contact['description'],
            },
            {
                "property": "mobilephone",
                "value": contact['mobilephone'],
            },
            {
                "property": "website",
                "value": contact['website'],
            },
            {
                "property": "industry",
                "value": contact['industry'],
            },
            {
                "property": "city",
                "value": contact['city'],
            },
            {
                "property": "leadsubject",
                "value": contact['leadsubject'],
            }
        ]
    }

    return contact_data


def save_hubspot_contact(contact):
    # if contact['firstname'] and contact['lastname'] and contact['email']:
    #     url = '{0}/contacts/v1/search/query?q={1} {2} {3}&hapikey={4}'.format(host, contact['firstname'],
    #                                                                           contact['lastname'], contact['email'],
    #                                                                           hapikey)
    # elif contact['firstname'] and contact['lastname']:
    #     url = '{0}/contacts/v1/search/query?q={1} {2}&hapikey={3}'.format(host, contact['firstname'],
    #                                                                       contact['lastname'], hapikey)
    # elif contact['lastname']:
    #     url = '{0}/contacts/v1/search/query?q={1}&hapikey={2}'.format(host, contact['lastname'], hapikey)
    if contact['email']:
        url = '{0}/contacts/v1/search/query?q={1}&hapikey={2}'.format(host, contact['email'], hapikey)
        response = requests.get(url)
        try:
            response = json.loads(response.text)

            contact_data = json_POST(contact)
            # print("CONTACT DATA")
            # print(contact_data)

            url = '{0}/contacts/v1/contact/'.format(host)
            headers = {"Content-Type": "application/json"}
            hapi = {"hapikey": hapikey}
            if response['total'] == 0:
                # {{HOST}}/contacts/v1/contact/?hapikey={{HApikey}}
                # https: // api.hubapi.com / contacts / v1 / contact / email / testingapis @ hubspot.com / profile?hapikey = demo

                print('CREANDO CONTACTO')
                r = requests.request("POST", url, data=json.dumps(contact_data), headers=headers, params=hapi)
                print(r.text)
            elif response['total'] == 1:
                print('CONTACTO EXISTE')
                # url = '{0}/contacts/v1/contact/email/{1}/profile'.format(host, contact['email'])
                url = '{0}/contacts/v1/contact/email/{1}/profile?hapikey={2}'.format(host, contact['email'], hapikey)
                headers['Content-Type'] = 'application/json'
                contact_data = {
                    "properties": [
                        {
                            "property": "hs_language",
                            "value": contact['hs_language'],
                        }
                    ]
                }
                try:
                    if response["contacts"][0]['properties']['hs_language']['value']:
                        print('CONTACTO EXISTE LANG')
                        print(response["contacts"][0]['properties']['hs_language']['value'])
                    else:
                        print('UPDATE LANG 1')
                        # r = requests.request("POST", url, data=json.dumps(contact_data), headers=headers, params=hapi)
                        r = requests.post(data=json.dumps(contact_data), url=url, headers=headers)
                        print(r)
                        print(contact['email'])
                        print(contact['hs_language'])
                except:
                    print('UPDATE LANG 2')
                    r = requests.post(data=json.dumps(contact_data), url=url, headers=headers)
                    print(r)
                    print(contact['email'])
                    print(contact['hs_language'])
        except:
            print('ERROR')
            print(response.text)
            time.sleep(3)


def save_contact():
    i = 0
    data = []
    pattron = re.compile('[0-9]')
    csv_file = get_csv_contacts()
    for cts in csv_file:
        if cts['LastName']:
            if cts['LastName'] != 'NULL' and pattron.search(cts['LastName']) is None:
                data.append(compare_contact(cts))

    for d in data:
        i += 1
        # print(i, ' ', d, '\n\n\n')
        save_hubspot_contact(d)
        print(i)


if __name__ == "__main__":
    save_contact()
