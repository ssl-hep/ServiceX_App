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
from flask import Response
from pytest import fixture

from tests.resource_test_base import ResourceTestBase


class TestAllTransformationRequest(ResourceTestBase):
    @staticmethod
    def example_json():
        return [{'request_id': '123'}, {'request_id': '456'}]

    @fixture()
    def mock_return_json(self, mocker):
        import servicex
        mock_return_json = mocker.patch.object(
            servicex.models.TransformRequest, 'return_json',
            return_value=self.example_json())
        return mock_return_json

    def test_get_all_auth_disabled(self, mock_rabbit_adaptor,
                                   mock_return_json):
        client = self._test_client(rabbit_adaptor=mock_rabbit_adaptor)
        response: Response = client.get('/servicex/transformation')
        assert response.status_code == 200
        assert response.json == self.example_json()
        mock_return_json.assert_called()

    def test_get_all_authorized(self, mock_rabbit_adaptor, mock_jwt_required,
                                mock_return_json, mock_requesting_user):
        mock_requesting_user.admin = True
        client = self._test_client(rabbit_adaptor=mock_rabbit_adaptor,
                                   extra_config={'ENABLE_AUTH': True})
        response: Response = client.get('/servicex/transformation')
        assert response.status_code == 200
        assert response.json == self.example_json()
        mock_return_json.assert_called()

    def test_get_all_unauthorized(self, mock_rabbit_adaptor, mock_jwt_required,
                                  mock_return_json, mock_requesting_user):
        mock_requesting_user.admin = False
        client = self._test_client(rabbit_adaptor=mock_rabbit_adaptor,
                                   extra_config={'ENABLE_AUTH': True})
        response: Response = client.get('/servicex/transformation')
        assert response.status_code == 401
        mock_return_json.assert_not_called()

    def test_get_by_user_from_self(self, mock_rabbit_adaptor, mock_jwt_required,
                                   mock_requesting_user, mock_return_json):
        user_id = mock_requesting_user.id
        client = self._test_client(rabbit_adaptor=mock_rabbit_adaptor,
                                   extra_config={'ENABLE_AUTH': True})
        response = client.get(f'/servicex/transformation?submitted_by={user_id}')
        assert response.status_code == 200
        assert response.json == self.example_json()
        mock_return_json.assert_called()

    def test_get_by_user_from_admin(self, mock_rabbit_adaptor, mock_jwt_required,
                                    mock_requesting_user, mock_return_json):
        user_id = mock_requesting_user.id + 1
        mock_requesting_user.admin = True
        client = self._test_client(rabbit_adaptor=mock_rabbit_adaptor,
                                   extra_config={'ENABLE_AUTH': True})
        response = client.get(f'/servicex/transformation?submitted_by={user_id}')
        assert response.status_code == 200
        assert response.json == self.example_json()
        mock_return_json.assert_called()

    def test_get_by_user_unauthorized(self, mock_jwt_required, mock_return_json,
                                      mock_rabbit_adaptor, mock_requesting_user):
        user_id = mock_requesting_user.id + 1
        mock_requesting_user.admin = False
        client = self._test_client(rabbit_adaptor=mock_rabbit_adaptor,
                                   extra_config={'ENABLE_AUTH': True})
        response = client.get(f'/servicex/transformation?submitted_by={user_id}')
        assert response.status_code == 401
        mock_return_json.assert_not_called()