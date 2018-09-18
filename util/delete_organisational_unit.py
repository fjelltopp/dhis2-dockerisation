
import requests
import json
import argparse
import datetime
from util import get_pages, get_auth


def delete_organisational_unit(dhis2_url, ou_to_delete):

    auth = get_auth('secret')

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
        print('Organisation unit id: {}'.format(organisation_unit['id']))

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Delete organisational unit from DHIS2 instance')
dhis2_url = 'ENTER DHIS2 BASE URL'
ou_to_delete = 'ENTER ORGANISATION UNIT DISPLAY NAME'

delete_organisational_unit(dhis2_url, ou_to_delete)