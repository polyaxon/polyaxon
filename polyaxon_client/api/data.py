# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.exceptions import (
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    PolyaxonException
)
from polyaxon_client.logger import logger
from polyaxon_client.schemas import DatasetConfig


class DatasetApi(BaseApiHandler):
    """
    Api handler to get datasets from the server.
    """
    ENDPOINT = "/datasets"

    def get_datasets(self):
        try:
            response = self.transport.get(self._get_http_url())
            datasets_dict = response.json()
            return [DatasetConfig.from_dict(dataset)
                    for dataset in datasets_dict.get("datasets", [])]
        except PolyaxonException as e:
            if isinstance(e, AuthenticationError):
                # exit now since there is nothing we can do without login
                raise e
            logger.info("Error while retrieving datasets: %s", e.message)
            return []

    def get_by_name(self, username, datasetname):
        request_url = self._build_url(username, datasetname)
        request_url = self._get_http_url(request_url)
        try:
            response = self.transport.get(request_url)
            return DatasetConfig.from_dict(response.json())
        except NotFoundError:
            return None

    def create_dataset(self, data):
        """
        Create a temporary directory for the tar file that will be removed at
        the end of the operation.
        """
        try:
            post_body = data.to_dict()
            post_body["resumable"] = True
            response = self.transport.post(self._get_http_url(), json_data=post_body)
            return response.json()
        except BadRequestError as e:
            logger.error('Could not create data %s', e.message)
            return None
        except PolyaxonException as e:
            logger.error('Could not create data %s', e.message)
            return None

    def delete_dataset(self, data_uuid):
        request_url = self._get_http_url(data_uuid)
        try:
            # data delete is a synchronous process, it can take a long time
            self.transport.delete(request_url, timeout=60)
            return True
        except PolyaxonException as e:
            logger.error('Could not create data %s', e.message)
            return False
