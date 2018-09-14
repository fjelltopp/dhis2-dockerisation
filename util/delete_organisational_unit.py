
import requests
import json
from requests.auth import HTTPBasicAuth
import datetime


def get_pages(url, auth, data_object):
    ret = requests.get(url, auth=auth)
    ret_dict = json.loads(ret.text)
    collated = []
    if 'pager' in ret_dict.keys():
        while int(ret_dict['pager']['page']) < int(ret_dict['pager']['pageCount']):
            collated = collated + ret_dict[data_object]
            next_page = int(ret_dict['pager']['page']) + 1
            ret = requests.get(url + '&page=' + str(next_page), auth=auth)
            ret_dict = json.loads(ret.text)

        collated = collated + ret_dict[data_object]
        return collated
    else:
        return ret_dict


def delete_organisational_unit(dhis2_url, ou_to_delete):

    with open('secret') as f:
        lines = f.readlines()
    username = lines[0].rstrip('\n')
    password = lines[1].rstrip('\n')

    auth = HTTPBasicAuth(username=username, password=password)

    # get the data set Ids
    get_data_set_url = '{}/api/27/dataSets'.format(dhis2_url)

    r = requests.get(get_data_set_url, auth=auth)
    r_dict = json.loads(r.text)

    # get relevant organisation Ids
    get_org_unit_url = '{}/api/27/organisationUnits?filter=displayName:like:{}'.format(dhis2_url, ou_to_delete)
    organisation_units = get_pages(get_org_unit_url, auth, 'organisationUnits')

    # define date limits
    period_start = datetime.date(2010, 1, 1)
    today = datetime.date.today()
    period_start_str = period_start.strftime('%Y-%m-%d')
    today_str = today.strftime('%Y-%m-%d')

    for organisation_unit in organisation_units:
        for data_set in r_dict['dataSets']:


            # get data values for each org unit within the date limits
            get_dvs_url = \
                '{root_url}/api/27/dataValueSets?dataSet={dataSetId}&orgUnit={orgUnitId}&startDate={startDate}&endDate={endDate}'\
                .format(
                    root_url=dhis2_url,
                    dataSetId=data_set['id'],
                    orgUnitId=organisation_unit['id'],
                    startDate=period_start_str,
                    endDate=today_str
                )
            dvs = requests.get(get_dvs_url, auth=auth)

            # loop through data values and remove them
            data_dict = json.loads(dvs.text)
            for data_point in data_dict.get('dataValues', []):
                delete_data_value_url = \
                    '{root_url}/api/27/dataValues?de={dataElementId}&ou={orgUnitId}&pe={period}&co={cat}'.format(
                        root_url=dhis2_url,
                        orgUnitId=organisation_unit['id'],
                        dataElementId=data_point['dataElement'],
                        period=data_point['period'],
                        cat=data_point['categoryOptionCombo'])
                ret_delete = requests.delete(delete_data_value_url, auth=auth)

        # get_audit_url = '{}/api/27/audits/dataValue?ou=iPjpfPR1Ptd' \
        #     .format(dhis2_url, organisation_unit['id'])
        # ret_delete = requests.delete(get_audit_url, auth=auth)

        # delete organisational units
        delete_organisational_unit_url = '{}/api/27/organisationUnits/{}'.format(dhis2_url, organisation_unit['id'])
        ret_delete = requests.delete(delete_organisational_unit_url, auth=auth)


dhis2_url = 'https://dhis2.emro.info'
ou_to_delete = 'Burtinle District Hospital'

delete_organisational_unit(dhis2_url, ou_to_delete)