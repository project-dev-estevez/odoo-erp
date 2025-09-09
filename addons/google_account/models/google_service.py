# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
import logging

import json
import requests
from werkzeug import urls

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

TIMEOUT = 20

GOOGLE_AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_API_BASE_URL = 'https://www.googleapis.com'


def _get_client_secret(ICP_sudo, service):
    """ Return the client_secret for a specific service.

    Note: This method serves as a hook for modules that would like share their own keys.
          This method should never be callable from a method that return it in clear, it
          should only be used directly in a request.

    :param ICP_sudo: the model ir.config_parameters in sudo
    :param service: the service that we need the secret key
    :return: The ICP value
    :rtype: str
    """
    return ICP_sudo.get_param('google_%s_client_secret' % service)

class GoogleService(models.AbstractModel):
    _name = 'google.service'
    _description = 'Google Service'

    def _get_client_id(self, service):
        # client id is not a secret, and can be leaked without risk. e.g. in clear in authorize uri.
        ICP = self.env['ir.config_parameter'].sudo()
        return ICP.get_param('google_%s_client_id' % service)

    @api.model
    def _get_authorize_uri(self, service, scope, redirect_uri, state=None, approval_prompt=None, access_type=None):
        """ This method return the url needed to allow this instance of Odoo to access to the scope
            of gmail specified as parameters
        """
        params = {
            'response_type': 'code',
            'client_id': self._get_client_id(service),
            'scope': scope,
            'redirect_uri': redirect_uri,
        }

        if state:
            params['state'] = state

        if approval_prompt:
            params['approval_prompt'] = approval_prompt

        if access_type:
            params['access_type'] = access_type


        encoded_params = urls.url_encode(params)
        return "%s?%s" % (GOOGLE_AUTH_ENDPOINT, encoded_params)

    @api.model
    def _get_google_tokens(self, authorize_code, service, redirect_uri):
        """ Call Google API to exchange authorization code against token """
        ICP = self.env['ir.config_parameter'].sudo()
        headers = {"content-type": "application/x-www-form-urlencoded"}
    
        # Construye la URL completa para depuración
        full_redirect_uri = self.get_base_url() + '/google_account/authentication'
        _logger.info("Google Auth - Redirect URI: %s", full_redirect_uri)
        _logger.info("Google Auth - Using Client ID: %s", self._get_client_id(service))

        data = {
            'code': authorize_code,
            'client_id': self._get_client_id(service),
            'client_secret': _get_client_secret(ICP, service),
            'redirect_uri': full_redirect_uri,  # Usa la URL completa
            'grant_type': 'authorization_code',
            'access_type': 'offline',
            'prompt': 'consent'
        }

        try:
            # Registra los datos para depuración
            _logger.debug("Sending to Google: %s", data)
        
            # Realiza la solicitud directamente con requests
            response = requests.post(
                'https://oauth2.googleapis.com/token',
                data=data,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            token_data = response.json()
        
            _logger.info("Google token response: %s", token_data)
        
            return (
                token_data.get('access_token'),
                token_data.get('refresh_token'),
                token_data.get('expires_in')
            )
        
        except requests.HTTPError as e:
            error_content = e.response.text if e.response else str(e)
            _logger.error("Google Token Error [HTTP %s]: %s", 
                        e.response.status_code if e.response else "N/A", 
                        error_content)
        
            error_msg = _("Google authentication failed: %s") % error_content
            raise self.env['res.config.settings'].get_config_warning(error_msg)
        
        except Exception as e:
            _logger.exception("Unexpected error during Google token exchange")
            error_msg = _("Unexpected error: %s") % str(e)
            raise self.env['res.config.settings'].get_config_warning(error_msg)


    @api.model
    def _do_request(self, uri, params=None, headers=None, method='POST', preuri=GOOGLE_API_BASE_URL, timeout=TIMEOUT):
        """ Execute the request to Google API. Return a tuple ('HTTP_CODE', 'HTTP_RESPONSE')
            :param uri : the url to contact
            :param params : dict or already encoded parameters for the request to make
            :param headers : headers of request
            :param method : the method to use to make the request
            :param preuri : pre url to prepend to param uri.
        """
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        assert urls.url_parse(preuri + uri).host in [
            urls.url_parse(url).host for url in (GOOGLE_TOKEN_ENDPOINT, GOOGLE_API_BASE_URL)
        ]

        # Remove client_secret key from logs
        if isinstance(params, str):
            _log_params = json.loads(params) or {}
        else:
            _log_params = (params or {}).copy()
        if _log_params.get('client_secret'):
            _log_params['client_secret'] = _log_params['client_secret'][0:4] + 'x' * 12

        _logger.debug("Uri: %s - Type : %s - Headers: %s - Params : %s!", uri, method, headers, _log_params)

        ask_time = fields.Datetime.now()
        try:
            if method.upper() in ('GET', 'DELETE'):
                res = requests.request(method.lower(), preuri + uri, params=params, timeout=timeout)
            elif method.upper() in ('POST', 'PATCH', 'PUT'):
                res = requests.request(method.lower(), preuri + uri, data=params, headers=headers, timeout=timeout)
            else:
                raise Exception(_('Method not supported [%s] not in [GET, POST, PUT, PATCH or DELETE]!', method))
            res.raise_for_status()
            status = res.status_code

            if int(status) == 204:  # Page not found, no response
                response = False
            else:
                response = res.json()

            try:
                ask_time = datetime.strptime(res.headers.get('date', ''), "%a, %d %b %Y %H:%M:%S %Z")
            except ValueError:
                pass
        except requests.HTTPError as error:
            if error.response.status_code in (204, 404):
                status = error.response.status_code
                response = ""
            else:
                _logger.exception("Bad google request : %s!", error.response.content)
                raise error
        return (status, response, ask_time)
