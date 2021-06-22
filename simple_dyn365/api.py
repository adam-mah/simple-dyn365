##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : api.py
import base64
import json
from collections import OrderedDict

import requests

from .login import DynamicsLogin


class Dynamics:
    """Dynamics Instance

    An instance of Dynamics is a way to wrap a Dynamics session
    for easy use of the Dynamics Web API.
    """

    def __init__(
            self,
            username=None,
            password=None,
            client_id=None,
            client_secret=None,
            crm_org=None,
            tenant_id=None,  # oauth token endpoint
            grant_type='client_credentials'
    ):
        if client_id is not None:
            self.session_id, self.dyn_instance = DynamicsLogin(
                username=username,
                password=password,
                client_id=client_id,
                client_secret=client_secret,
                crm_org=crm_org,
                tenant_id=tenant_id,  # oauth token endpoint
                grant_type=grant_type)

        else:
            raise TypeError('You must provide login information')
        self.session = requests.Session()
        self.headers = {
            'Authorization': 'Bearer ' + self.session_id,
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            'Prefer': 'odata.maxpagesize=500',
            'X-PrettyPrint': '1'
        }

        self.version = '9.2.21051.00140'
        self.base_url = ('{instance}/api/data/v{version}/'
                         .format(instance=self.dyn_instance,
                                 version=self.version))

    # Generic Rest Function
    def restful(self, path, params=None, method='GET', **kwargs):
        """Allows you to make a direct REST call if you know the path

        Arguments:

        * path: The path of the request
            Example: contacts('record ID')'
        * params: dict of parameters to pass to the path
        * method: HTTP request method, default GET
        * other arguments supported by requests.request (e.g. json, timeout)
        """

        url = self.base_url + path
        result = self._call_dynamics(method, url, name=path, params=params,
                                     **kwargs)

        json_result = result.json(object_pairs_hook=OrderedDict)
        if len(json_result) == 0:
            return None

        return json_result

    def _call_dynamics(self, method, url, **kwargs):
        """Utility method for performing HTTP call to Salesforce.

        Returns a `requests.result` object.
        """
        headers = self.headers.copy()
        additional_headers = kwargs.pop('headers', dict())
        headers.update(additional_headers or dict())

        result = self.session.request(
            method, url, headers=headers, **kwargs)

        if result.status_code >= 300:
            raise Exception()

        return result

    def query(self, query, headers=None):
        result = self._call_dynamics(
            method='GET', url=self.base_url+f'{query}',
            headers=headers
        )
        return result.json(object_pairs_hook=OrderedDict)

    def __getattr__(self, name):
        """Returns an `DYNEnity` instance for the given Dynamics enity.
        Arguments:
        * name -- the name of a Dynamics entity, Ex: accounts, contacts..
        """

        if name.startswith('__'):
            return super().__getattr__(name)

        return DYNEntity(
            entity_name=name, session_id=self.session_id, dyn_instance=self.dyn_instance, session=self.session)


class DYNEntity:
    """An interface to a specific type of DYN Entity"""

    def __init__(
            self,
            entity_name,
            session_id,
            dyn_instance,
            session=None,
    ):
        self.session_id = session_id
        self.name = entity_name
        self.session = session
        self.dyn_instance = dyn_instance
        self.version = '9.2.21051.00140'
        self.base_url = (
            '{instance}/api/data/v{version}/{entity_name}'.format(instance=dyn_instance,
                                                                           entity_name=entity_name,
                                                                           version=self.version))

    def metadata(self, headers=None):
        """Returns the result of a GET to `.../EntityDefinitions(LogicalName='{entity_name}')` as a dict
        decoded from the JSON payload returned by Dynamics.
        """
        meta_url = (
            '{instance}/api/data/v{version}/EntityDefinitions(LogicalName=\'{entity_name}\')'.format(instance=self.dyn_instance,
                                                                  entity_name=self.name,
                                                                  version=self.version))
        result = self._call_dynamics('GET', meta_url, headers=headers)
        return result.json(object_pairs_hook=OrderedDict)

    def get(self, entity_id, headers=None):
        result = self._call_dynamics(
            method='GET', url=self.base_url+f'({entity_id})',
            headers=headers
        )
        return result.json(object_pairs_hook=OrderedDict)

    def query(self, query, headers=None):
        result = self._call_dynamics(
            method='GET', url=self.base_url+f'?${query}',
            headers=headers
        )
        return result.json(object_pairs_hook=OrderedDict)

    def create(self, data, headers=None):
        result = self._call_dynamics(
            method='POST', url=self.base_url,
            json=json.dumps(data), headers=headers
        )

        if result.status_code == 204:
            return result.headers['OData-EntityId']

        return result.json(object_pairs_hook=OrderedDict)

    def upsert(self, entity_id, data, raw_response=False, headers=None):
        result = self._call_dynamics(
            method='PATCH', url=self.base_url+f'({entity_id})',
            data=json.dumps(data), headers=headers
        )
        return self._raw_response(result, raw_response)

    def update(self, entity_id, data, raw_response=False, headers=None):
        result = self._call_dynamics(
            method='PATCH', url=self.base_url+f'({entity_id})',
            data=json.dumps(data), headers=headers
        )
        return self._raw_response(result, raw_response)

    def delete(self, entity_id, raw_response=False, headers=None):
        result = self._call_dynamics(
            method='DELETE', url=self.base_url+f'({entity_id})',
            headers=headers
        )
        return self._raw_response(result, raw_response)

    def _call_dynamics(self, method, url, **kwargs):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.session_id,
            'X-PrettyPrint': '1',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json'
        }
        additional_headers = kwargs.pop('headers', dict())
        headers.update(additional_headers or dict())
        result = self.session.request(method, url, headers=headers, **kwargs)

        if result.status_code >= 300:
            raise Exception(result.text)

        return result

    def _raw_response(self, response, body_flag):
        """Utility method for processing the response and returning either the
        status code or the response object.

        Returns either an `int` or a `requests.Response` object.
        """
        if not body_flag:
            return response.status_code

        return response

    def upload_base64(self, file_path, base64_field='documentbody', codec='utf-8', data={}, headers=None, **kwargs):
        with open(file_path, "rb") as f:
            body = base64.b64encode(f.read()).decode(codec)
        data[base64_field] = body
        result = self._call_dynamics(method='POST', url=self.base_url, headers=headers, json=data, **kwargs)

        return result

    def get_base64(self, entity_id, base64_field='documentbody', data=None, headers=None, **kwargs):
        """Returns binary stream of base64 object at specific path.
        """
        result = self._call_dynamics(method='GET', url=self.base_url+f'({entity_id})',
                                       data=data,
                                       headers=headers, **kwargs)
        result = result.json(object_pairs_hook=OrderedDict)
        return base64.b64decode(result[base64_field])

    def update_base64(self, record_id, file_path, base64_field='documentbody', codec='utf-8', data={}, headers=None, raw_response=False,
                      **kwargs):
        with open(file_path, "rb") as f:
            body = base64.b64encode(f.read()).decode(codec)
        data[base64_field] = body
        result = self._call_dynamics(method='PATCH', url=self.base_url+f'({record_id})', json=data,
                                       headers=headers, **kwargs)

        return self._raw_response(result, raw_response)