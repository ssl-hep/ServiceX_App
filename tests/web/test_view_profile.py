from flask import Response, url_for, render_template

from .web_test_base import WebTestBase


class TestViewProfile(WebTestBase):
    def test_view_profile(self, client, user):
        with client.session_transaction() as sess:
            sess['sub'] = 'janedoe'
        response: Response = client.get(url_for('profile'))
        assert response.status_code == 200
        assert response.data.decode() == render_template('profile.html', user=user)
