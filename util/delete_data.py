import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

dhis2_url = 'https://dhis2.emro.info'

with open('secret') as f:
    lines = f.readlines()
username = lines[0].rstrip('\n')
password = lines[1].rstrip('\n')

auth = HTTPBasicAuth(username=username, password=password)

# get the data set Id
get_data_set_url = '{}/api/27/dataSets?filter=displayName:like:HOQM'.format(dhis2_url)

r = requests.get(get_data_set_url, auth=auth)
r_dict = json.loads(r.text)

dataSetId = r_dict['dataSets'][0]['id']

# get relevant organisation Ids

get_org_unit_url = '{}/api/27/organisationUnits'.format(dhis2_url)

r_ou = requests.get(get_org_unit_url, auth=auth)
ou_dict = json.loads(r_ou.text)
organisation_units = []
while ou_dict['pager']['page'] < ou_dict['pager']['pageCount']:
    organisation_units = organisation_units + ou_dict['organisationUnits']
    r_ou = requests.get(ou_dict['pager']['nextPage'], auth=auth)
    ou_dict = json.loads(r_ou.text)
organisation_units = organisation_units + ou_dict['organisationUnits']



pprint(json.loads(r_ou.text))

get_data_value_url = '{}/api/27/dataValueSets?dataSet={}'.format(dhis2_url, dataSetId)

r_de = requests.get(get_data_value_url, auth=auth)

pprint(dataSetId)
pprint(json.loads(r.text))

"""
TODO: 
TODO: Get data elements
TODO: Get data values
"""