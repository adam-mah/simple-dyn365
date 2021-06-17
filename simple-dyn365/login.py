##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : login.py

"""Login class and functions for Simple-DYN365
"""

from html import escape
from json.decoder import JSONDecodeError

import requests


def DynamicsLogin(
        username=None,
        password=None,
        client_id=None,
        client_secret=None,
        crm_org=None,
        tenant_id=None,  # oauth token endpoint
        grant_type='client_credentials'
):
    """
    """

    token_endpoint_url = 'https://login.microsoftonline.com/{bearer}/oauth2/token'
    token_endpoint_url = token_endpoint_url.format(bearer=tenant_id)

    username = escape(username) if username else None
    password = escape(password) if password else None

    if grant_type == 'client_credentials':
        if client_id is not None and client_secret is not None:
            login_token_request_data = {
                'client_id': client_id,
                'resource': crm_org,
                'client_secret': client_secret,
                'grant_type': grant_type
            }

            return token_login(token_url=token_endpoint_url, token_data=login_token_request_data)

    elif grant_type == 'password':
        if username is not None and password is not None:
            pass#TODO: Validations and password login

    else:
        except_code = 'INVALID AUTH'
        except_msg = (
            'You must submit either a security token or organizationId for '
            'authentication'
        )
        raise Exception(except_code, except_msg)


def token_login(token_url, token_data):
    """Process OAuth 2.0 JWT Bearer Token Flow."""

    response = requests.post(token_url, data=token_data)

    try:
        json_response = response.json()
    except JSONDecodeError as json_decode_error:
        raise Exception(
            response.status_code, response.text
        ) from json_decode_error

    if response.status_code != 200:
        except_code = json_response.get('error')
        except_msg = json_response.get('error_description')
        raise Exception(except_code, except_msg)

    access_token = json_response.get('access_token')
    resource = json_response.get('resource')

    return access_token, resource
