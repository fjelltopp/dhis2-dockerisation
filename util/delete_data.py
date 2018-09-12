import requests
import json
from pprint import pprint
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


def delete_data_sets(dhis2_url, prefix):
    # dhis2_url = 'https://dhis2.emro.info'

    with open('secret') as f:
        lines = f.readlines()
    username = lines[0].rstrip('\n')
    password = lines[1].rstrip('\n')

    # prefix = 'HOQM'

    auth = HTTPBasicAuth(username=username, password=password)

    # get the data set Ids
    get_data_set_url = '{}/api/27/dataSets?filter=displayName:like:{}'.format(dhis2_url, prefix)

    r = requests.get(get_data_set_url, auth=auth)
    r_dict = json.loads(r.text)

    dataSetIds = [r_dict['dataSets'][0]['id']]

    # get relevant organisation Ids
    get_org_unit_url = '{}/api/27/organisationUnits?filter=dataSets.id:eq:{}'.format(dhis2_url, dataSetIds[0])
    organisation_units = get_pages(get_org_unit_url, auth, 'organisationUnits')


    data_values = []

    # define date limits
    period_start = datetime.date(2018, 1, 1)
    today = datetime.date.today()
    period_start_str = period_start.strftime('%Y-%m-%d')
    today_str = today.strftime('%Y-%m-%d')

    for dataSetId in dataSetIds:
        pprint('handling data set {}'.format(dataSetId))
        for orgUnit in organisation_units:
            pprint('handling org unit {}'.format(orgUnit['id']))

            # get data values for each org unit within the date limits
            get_dvs_url = \
                '{root_url}/api/27/dataValueSets?dataSet={dataSetId}&orgUnit={orgUnitId}&startDate={startDate}&endDate={endDate}'\
                .format(
                    root_url=dhis2_url,
                    dataSetId=dataSetId,
                    orgUnitId=orgUnit['id'],
                    startDate=period_start_str,
                    endDate=today_str
                )

            dvs = requests.get(get_dvs_url, auth=auth)

            # loop through data values and remove them
            data_dict = json.loads(dvs.text)
            for data_point in data_dict.get('dataValues', []):
                get_data_value_url = \
                    '{root_url}/api/27/dataValues?de={dataElementId}&ou={orgUnitId}&pe={period}'.format(
                        root_url=dhis2_url,
                        orgUnitId=orgUnit['id'],
                        dataElementId=data_point['dataElement'],
                        period=data_point['period'])
                data_value = requests.delete(get_data_value_url, auth=auth)

        # Find and delete data elements
        get_data_elements_url = '{}/api/27/dataElements?filter=dataSetElements.dataSet.id:eq:{}' \
            .format(dhis2_url, dataSetId)
        data_elements = get_pages(get_data_elements_url, auth, 'dataElements')

        for data_element in data_elements:
            delete_data_element_url = '{}/api/27/dataElements/{}'.format(dhis2_url, data_element['id'])
            ret = requests.delete(delete_data_element_url, auth=auth)

        # Delete data set
        delete_data_set_url = '{}/api/27/dataSets/{}'.format(dhis2_url, dataSetId)
        ret = requests.delete(delete_data_set_url, auth=auth)


def delete_event_trackers(dhis2_url, prefix):
    with open('secret') as f:
        lines = f.readlines()
    username = lines[0].rstrip('\n')
    password = lines[1].rstrip('\n')

    auth = HTTPBasicAuth(username=username, password=password)

    # get the program Ids
    get_program_url = '{}/api/27/programs?filter=displayName:like:{}'.format(dhis2_url, prefix)
    programs = get_pages(get_program_url, auth, 'programs')

    for program in programs:

        # get relevant organisation Ids
        get_org_unit_url = '{}/api/27/organisationUnits?filter=programs.id:eq:{}'.format(dhis2_url, program['id'])
        organisation_units = get_pages(get_org_unit_url, auth, 'organisationUnits')

        for ou in organisation_units:
            get_events_url = '{}/api/27/events?filter=program={}&orgUnit={}'\
                .format(dhis2_url, program['id'], ou['id'])
            r_events = requests.get(get_events_url, auth=auth)
            r_events_dict = json.loads(r_events.text)

            # delete events from organisation unit
            for event in r_events_dict['events']:
                event_id = event['event']

                delete_event_url = '{}/api/27/events/{}'.format(dhis2_url, event_id)

                ret_delete = requests.delete(delete_event_url, auth=auth)

        get_program_stages_url = '{}/api/27/programStages?filter=program.id:eq:{}'.format(dhis2_url, program['id'])
        program_stages = get_pages(get_program_stages_url, auth, 'programStages')

        data_elements = []

        for program_stage in program_stages:
            get_program_stage_details_url = '{}/api/27/programStages/{}'.format(dhis2_url, program_stage['id'])
            program_stage_details = requests.get(get_program_stage_details_url, auth=auth)
            program_stage_dict = json.loads(program_stage_details.text)
            data_elements = data_elements + program_stage_dict['programStageDataElements']

        get_data_elements_url = '{}/api/27/dataElements?program={}'.format(dhis2_url, program['id'])

        for data_element in program_stage_dict['programStageDataElements']:
            delete_data_element_url = '{}/api/27/dataElements/{}'.format(dhis2_url, data_element['dataElement']['id'])
            ret_delete = requests.delete(delete_data_element_url, auth=auth)

        for program_stage in program_stages:
            delete_program_stage_url = '{}/api/27/programStages/{}'.format(dhis2_url, program_stage['id'])
            ret_delete = requests.delete(delete_program_stage_url, auth=auth)

        delete_program_url = '{}/api/27/programs/{}'.format(dhis2_url, program['id'])
        ret_delete = requests.delete(delete_program_url, auth=auth)

    return True


dhis2_url = 'https://dhis2.emro.info'
prefix = 'HOQM'

delete_event_trackers(dhis2_url, prefix)
