import csv
import json

import requests
import re

csv_file = ['../csv/Contacts.csv']
host = 'https://api.hubapi.com'
hapikey = '8a7b8099-d61e-402d-ac36-0f1098d0c0c0'


def get_csv_contacts():
    with open(csv_file[0], encoding='utf-8') as file_contact:
        file_read = csv.DictReader(file_contact)
        data = []
        for row in file_read:
            data.append(row)

        return data


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

    if contact['sm_LeadLanguage'] and contact['sm_LeadLanguage'] != 'NULL':
        if contact['sm_LeadLanguage'] == 'French':
            data.update({'hs_language': 'fr'})
        else:
            data.update({'hs_language': 'en-us'})

    else:
        if contact['SM_Language'] != 'NULL' and str(contact['SM_Language']).isdigit() is True:
            if contact['SM_Language'] == 1:
                data.update({'hs_language': 'fr'})
            elif contact['SM_Language'] == 2:
                data.update({'hs_language': 'en-us'})

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


def save_hubspot_contact(contact):
    # {{HOST}} /contacts/v1/search/query?q=Tilo
    # Rivas
    # SenStack @ njleg.org & hapikey = {{HApikey}}
    # print(contact)

    if contact['firstname'] and contact['lastname'] and contact['email']:
        url = '{0}/contacts/v1/search/query?q={1} {2} {3}&hapikey={4}'.format(host, contact['firstname'],
                                                                              contact['lastname'], contact['email'],
                                                                              hapikey)
    elif contact['firstname'] and contact['lastname']:
        url = '{0}/contacts/v1/search/query?q={1} {2}&hapikey={3}'.format(host, contact['firstname'],
                                                                          contact['lastname'], hapikey)
    elif contact['lastname']:
        url = '{0}/contacts/v1/search/query?q={1}&hapikey={2}'.format(host, contact['lastname'], hapikey)

    response = requests.get(url)
    response = json.loads(response.text)
    if response['total'] == 0:
        # {{HOST}}/contacts/v1/contact/?hapikey={{HApikey}}
        url = '{0}/contacts/v1/contact/'.format(host)
        headers = {"Content-Type": "application/json"}
        hapi = {"hapikey": hapikey}
        if contact['hs_language'] == 'fr':
            country = 'Canada'
        else:
            country = 'United State of America'

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
                },
                {
                    "property": "country",
                    "value": country
                }
            ]
        }
        r = requests.request("POST", url, data=json.dumps(contact_data), headers=headers, params=hapi)
        print(r.text)


def save_contact():
    data = []
    pattron = re.compile('[0-9]')
    csv_file = get_csv_contacts()
    for cts in csv_file:
        if cts['LastName']:
            if cts['LastName'] != 'NULL' and pattron.search(cts['LastName']) is None:
                data.append(compare_contact(cts))

    for d in data:
        # print(i, ' ', d, '\n\n\n')
        save_hubspot_contact(d)


if __name__ == "__main__":
    save_contact()
