import requests
import json
from pprint import pprint
from requests.auth import HTTPBasicAuth

#dhis2_url = 'https://dhis2.emro.info'
dhis2_url = 'https://play.dhis2.org/2.27'

with open('secret') as f:
    lines = f.readlines()
username = lines[0].rstrip('\n')
password = lines[1].rstrip('\n')

#prefix = 'HOQM'
prefix = 'PMTCT'

auth = HTTPBasicAuth(username=username, password=password)

# get the data set Id
get_data_set_url = '{}/api/27/dataSets?filter=displayName:like:{}'.format(dhis2_url, prefix)

r = requests.get(get_data_set_url, auth=auth)
r_dict = json.loads(r.text)

dataSetIds = [r_dict['dataSets'][0]['id']]

# get relevant organisation Ids

get_org_unit_url = '{}/api/27/organisationUnits?dataSets.id:like:{}'.format(dhis2_url, dataSetIds[0])

r_ou = requests.get(get_org_unit_url, auth=auth)
ou_dict = json.loads(r_ou.text)
organisation_units = []
while ou_dict['pager']['page'] < ou_dict['pager']['pageCount']:
    organisation_units = organisation_units + ou_dict['organisationUnits']
    r_ou = requests.get(ou_dict['pager']['nextPage'], auth=auth)
    ou_dict = json.loads(r_ou.text)
organisation_units = organisation_units + ou_dict['organisationUnits']

for dataSetId in dataSetIds:
    for orgUnit in organisation_units:
        get_data_value_set_ids_url = \
            '{root_url}/api/27/dataValueSets?filter=orgUnit:eq:{orgUnitId}&dataSet:eq:{dataSetId}'.format(
                root_url=dhis2_url,
                orgUnitId=orgUnit['id'],
                dataSetId=dataSetId)
        data_value_sets = requests.get(get_data_value_set_ids_url, auth=auth)

pprint(json.loads(r_ou.text))

get_data_elements_url = '{}/api/27/dataElements?filter=displayName:like:HOQM'

#r_de = requests.get(get_data_value_url, auth=auth)

pprint(dataSetId)
pprint(json.loads(r.text))

def delete_data_values():
    pass

"""
TODO: 
TODO: Get data elements
TODO: Get data values

TRACKER
events
dataElements
programStage
program
"""