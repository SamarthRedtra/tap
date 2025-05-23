from __future__ import absolute_import, division, print_function

import tap
import tap.api_resources
from tap.api_resources.abstract.api_resource import APIResource
import tap.api_resources.api_requestor



class ListeableAPIResource(APIResource):

    @classmethod
    def auto_paging_iter(cls, *args, **params):
        return cls.list(*args, **params).auto_paging_iter()

    @classmethod
    def list(cls, api_key=None, tap_version=None, tap_account=None, **params):

        requestor = tap.api_resources.api_requestor.APIRequestor(api_key, api_version=tap_version,
                                               account=tap_account)
        url = '%s/list' % (cls.class_url())
        response, api_key = requestor.request('post', url, params)
        tap_object = tap.util.convert_to_tap_object(response, api_key, tap_version,
                                                   tap_account)

        return tap_object
