import os

from flask import current_app
import globus_sdk


def load_app_client():
    client_id = os.environ.get('GLOBUS_CLIENT_ID',
                               current_app.config['GLOBUS_CLIENT_ID'])
    client_secret = os.environ.get('GLOBUS_CLIENT_SECRET',
                                   current_app.config['GLOBUS_CLIENT_SECRET'])
    return globus_sdk.ConfidentialAppAuthClient(client_id, client_secret)
