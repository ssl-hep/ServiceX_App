import os

from flask import current_app
import globus_sdk


def load_app_client():
    if ('GLOBUS_CLIENT_ID' in os.environ):
        client_id = os.environ['GLOBUS_CLIENT_ID']
    else:
        client_id = current_app.config['GLOBUS_CLIENT_ID']

    if ('GLOBUS_CLIENT_SECRET' in os.environ):
        client_secret = os.environ['GLOBUS_CLIENT_SECRET']
    else:
        client_secret = current_app.config['GLOBUS_CLIENT_SECRET']
    return globus_sdk.ConfidentialAppAuthClient(client_id, client_secret)
