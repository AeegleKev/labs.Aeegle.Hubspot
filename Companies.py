import csv, requests, json

# GLOBAL VARS
host = 'https://api.hubapi.com'
hapikey = '8a7b8099-d61e-402d-ac36-0f1098d0c0c0'


# populationData = []

# GET DATA FROM .CSV FILE
def get_data_from_file(fileName):
    with open(fileName, encoding='utf-8') as csvFile:
        rows = csv.DictReader(csvFile)
        data = []
        for row in rows:
            data.append(row)
        return data


# GET ALL COMPANIES
def get_all_companies():
    params = {'properties': 'name', 'hapikey': hapikey, 'limit': 250}
    companies = []

    url = '{0}/companies/v2/companies/paged?properties={1}&properties={2}'.format(host, 'domain', 'population')
    response = requests.get(url, params)

    response = json.loads(response.text)
    companies = response['companies']
    has_more = response['has-more']
    offset = response['offset']

    params.setdefault('offset', offset)

    while (has_more):
        _response = requests.get(url, params)
        _response = json.loads(_response.text)

        companies += _response['companies']
        has_more = _response['has-more']
        offset = _response['offset']

        params['offset'] = offset

    return companies


# Update el campo Population
def update_population(data_list):
    i = 1
    for company in data_list:
        url = '{0}/companies/v2/companies/{1}?hapikey={2}'.format(host, company['company_id'], hapikey)
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.put(url, data=json.dumps(company['data']), headers=headers)
            print("{0}/{1}. COMPANY UPDATE ... ".format(i, len(data_list)))
            i += 1
        except Exception as err:
            print(err)

    print("POPULATION UPDATE FINISHED")


# Formato para hacer update de Population
def format_population(id_company, population, domain):
    diccionary = {'company_id': id_company, 'domain': domain,
                  'data': {'properties': [{'name': 'population', 'value': population}]}}
    return diccionary


def create_company(companies):
    url = '{0}/companies/v2/companies/'.format(host)
    headers = {"Content-Type": "application/json"}
    hapi = {"hapikey": hapikey}
    for c in companies:
        company = {'name': '', 'description': '', 'domain': '', 'population': ''}

        if c['Company Name'] or c['Company Name'] != 'NULL':
            company['name'] = c['Company Name']
        if c['Description'] and c['Description'] != 'NULL':
            company['description'] = c['Description']
        if c['Domain Name'] and c['Domain Name'] != 'NULL':
            company['domain'] = c['Domain Name']
        if c['Population'] and c['Population'] != 'NULL':
            company['population'] = c['Population']

        data = {"properties": [
            {
                "name": "name",
                "value": company['name']
            },
            {
                "name": "description",
                "value": company['description']
            },
            {
                "name": "domain",
                "value": company['domain']
            },
            {
                "name": "population",
                "value": company['population']
            }
        ]}

        r = requests.request("POST", url, data=json.dumps(data), headers=headers, params=hapi)
        print(r.text)


# Unir y verificar dato a dato, ademas de actulizar o crear companies
def merge_data_companies():
    local_data = get_data_from_file('csv/data.csv')
    hubspot_data = get_all_companies()
    data_update = []  # COMPANIES QUE SE ACTUALIZARA
    data_create = []  # COMPANIES QUE SE CREARAN
    not_found = []  # COMPANIES CON ERRORES

    for row in local_data:
        found = False
        for company in hubspot_data:

            if (row['E-mail'].find('@') != -1):
                domainLocal = row['E-mail'].split('@')
                domainLocal = domainLocal[1]
            else:
                domainLocal = False

            try:
                domain = company['properties']['domain']['value']
            except Exception as err:
                domain = False

            if (domainLocal and domain):

                if (domainLocal == domain):
                    if (row['Population'] != 'NULL' and row['Population'] != '' and row['Population'] != None):
                        data_update.append(format_population(company['companyId'], row['Population'], domain))
                    found = True

        if (not (found)):
            if (row['E-mail'].find('@') != -1):
                data_create.append(row)
            else:
                not_found.append(row)

    # update_population(data_update)

    # create_company(data_create)

    print("Nuevos: {0} Erroneos: {1}".format(len(data_create), len(not_found)))
    for data in data_create:
        print(data, '\n\n')


if __name__ == '__main__':
    merge_data_companies()
