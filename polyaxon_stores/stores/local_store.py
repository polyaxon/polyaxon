# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


from polyaxon_stores.stores.base_store import Store


class LocalStore(Store):
    """
    Local filesystem store.
    """
    STORE_TYPE = Store._LOCAL_STORE  # pylint:disable=protected-access
