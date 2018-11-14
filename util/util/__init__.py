import requests
import json
from requests.auth import HTTPBasicAuth


def get_pages(url, auth, data_object):
    """
    Gets data from DHIS2 Web API and collates pages into one dictionary
    :param url: data object url
    :param auth: HTTPBasicAuth object for authorisation
    :param data_object: Metadata type of queried data object
    :return: Dictionary with all return value pages collated
    """
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


def get_auth(auth_file):
    """
    Reads username and password from file
    :param auth_file: file name with username and password as first 2 lines
    :return: HTTPBasicAuth object
    """
    with open(auth_file) as f:
        lines = f.readlines()
    username = lines[0].rstrip('\n')
    password = lines[1].rstrip('\n')

    return HTTPBasicAuth(username=username, password=password)
