from types import SimpleNamespace
from unittest.mock import MagicMock

from flask import Response
from pytest import fixture

from tests.resource_test_base import ResourceTestBase


class TestTokenRefresh(ResourceTestBase):
    module = 'servicex.resources.users.token_refresh'
    endpoint = '/token/refresh'
    fake_token = 'abcd'

    @fixture(autouse=True, scope="class")
    def unwrap(self):
        """Remove the @jwt_refresh_token_required decorator."""
        from servicex.resources.users.token_refresh import TokenRefresh
        TokenRefresh.post = TokenRefresh.post.__wrapped__

    @fixture
    def jwt_funcs(self, mocker) -> SimpleNamespace:
        m = self.module
        patch = mocker.patch
        sub = "janedoe@example.com"
        return SimpleNamespace(
            get_jwt_identity=patch(f"{m}.get_jwt_identity", return_value=sub),
            create_access_token=patch(f"{m}.create_access_token", return_value=self.fake_token),
            get_raw_jwt=patch(f"{m}.get_raw_jwt", return_value={"jti": "1234"}),
            decode_token=mocker.patch(f"{m}.decode_token")
        )

    @fixture
    def mock_user(self, mocker) -> MagicMock:
        return mocker.patch(f"{self.module}.UserModel.find_by_sub").return_value

    def make_request(self, client):
        response: Response = client.post(self.endpoint)
        assert response.status_code == 200
        assert response.json == {'access_token': self.fake_token}

    def test_post_valid_refresh_token(self, client, jwt_funcs, mock_user):
        jwt_funcs.decode_token.return_value = jwt_funcs.get_raw_jwt.return_value
        self.make_request(client)

    def test_post_invalid_refresh_token(self, client, jwt_funcs, mock_user):
        jwt_funcs.decode_token.return_value = {"jti": "this value will not match"}
        response: Response = client.post(self.endpoint)
        assert response.status_code == 401
        assert response.json == {"message": "Invalid or outdated refresh token"}

    def test_post_user_mgmt_disabled(self, jwt_funcs):
        client = self._test_client(extra_config={'DISABLE_USER_MGMT': True})
        self.make_request(client)
        jwt_funcs.get_jwt_identity.assert_called_once()
