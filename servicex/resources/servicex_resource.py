# Copyright (c) 2019, IRIS-HEP
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from datetime import datetime, timezone
from typing import Optional

import pkg_resources
from flask import current_app
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource

from servicex.models import TransformationResult, UserModel


class ServiceXResource(Resource):
    @classmethod
    def _generate_advertised_endpoint(cls, endpoint):
        return "http://" + current_app.config['ADVERTISED_HOSTNAME'] + "/" + endpoint

    @staticmethod
    def get_requesting_user() -> Optional[UserModel]:
        """
        :return: User who submitted request for resource.
        If auth is enabled, this cannot be None for JWT-protected resources
        which are decorated with @auth_required or @admin_required.
        """
        user = None
        if current_app.config.get('ENABLE_AUTH'):
            user = UserModel.find_by_sub(get_jwt_identity())
        return user

    @staticmethod
    def _generate_file_status_record(dataset_file, status):
        time = int(datetime.now(tz=timezone.utc).timestamp() * 1000)

        return {
            "req_id": dataset_file.request_id,
            "adler32": dataset_file.adler32,
            "file_size": dataset_file.file_size,
            "file_events": dataset_file.file_events,
            "file_path": dataset_file.file_path,
            "status": status,
            "info": 'info',
            "created_at": time,
            "last_accessed_at": time,
            "events_served": 0,
            "retries": 0
        }

    def _generate_transformation_record(self, submitted_request, status):
        request_id = submitted_request.request_id
        count = TransformationResult.count(request_id)
        time = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
        current_stats = TransformationResult.statistics(request_id)

        events_transformed = 0 if not current_stats else current_stats['total-events']
        return {
            "name": 'Transformation Request',
            "description": 'Transformation Request',
            "dataset": submitted_request.did,
            "dataset_size": int(submitted_request.total_bytes or 0),
            "dataset_files": count,
            "dataset_events": int(submitted_request.total_events or 0),
            "columns": submitted_request.columns,
            "events": 0,
            "events_transformed": events_transformed,
            "events_served": 0,
            "events_processed": 0,
            "created_at": submitted_request.submit_time,
            "modified_at": time,
            "status": status,
            "info": ' '
        }

    @classmethod
    def _get_app_version(cls):
        """
        Examine installed packages to get the version number for the ServiceX App
        :return: The version number, or the string "develop" if servicex_app not installed
        """
        try:
            app_version = pkg_resources.get_distribution('servicex_app').version
            return app_version
        except pkg_resources.DistributionNotFound:
            return "develop"
