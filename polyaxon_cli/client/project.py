# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import sys

from polyaxon_schemas.project import ProjectConfig
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from polyaxon_cli.client.base import PolyaxonClient
from polyaxon_cli.exceptions import PolyaxonException, AuthenticationError, NotFoundError
from polyaxon_cli.logging import logger
from polyaxon_cli.utils.files import get_files_in_current_directory, create_progress_callback


class ProjectClient(PolyaxonClient):
    """Client to get projects from the server"""
    ENDPOINT = "/projects"

    def get_projects(self):
        try:
            response = self.get(self._get_url())
            projects_dict = response.json()
            return [ProjectConfig.from_dict(project) 
                    for project in projects_dict.get("projects", [])]
        except PolyaxonException as e:
            logger.info("Error while retrieving projects: {}".format(e.message))
            if isinstance(e, AuthenticationError):
                # exit now since there is nothing we can do without login
                sys.exit(1)
            return []

    def get_by_name(self, name):
        request_url = self._build_url(self.auth_config.username, name)
        request_url = self._get_url(request_url)
        try:
            response = self.get(request_url)
            return ProjectConfig.from_dict(response.json())
        except NotFoundError:
            return None

    def upload(self):
        try:
            upload_files, total_file_size = get_files_in_current_directory(file_type='code')
        except OSError:
            sys.exit(
                "Directory contains too many files to upload. "
                "If you have data files in the current directory, "
                "please upload them separately using `polyaxon data` "
                "command and remove them from here.\n"
                "See http://docs.polyaxon.com/faqs/job/ "
                "for more details on how to fix this.")

        logger.info("Creating project run. Total upload size: %s", total_file_size)
        logger.debug("Creating module. Uploading: %s files", len(upload_files))
        logger.info("Syncing code ...")

        # Add request data
        multipart_encoder = MultipartEncoder(fields=upload_files)

        # Attach progress bar
        progress_callback, bar = create_progress_callback(multipart_encoder)
        multipart_encoder_monitor = MultipartEncoderMonitor(multipart_encoder, progress_callback)

        try:
            response = self.request("POST",
                                    self._get_url(),
                                    data=multipart_encoder_monitor,
                                    headers={"Content-Type": multipart_encoder.content_type},
                                    timeout=3600)
        finally:
            # always make sure we clear the console
            bar.done()
        return response.json().get("uuid")

