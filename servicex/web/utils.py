import os

from flask import current_app
import globus_sdk


def load_app_client():
    return globus_sdk.ConfidentialAppAuthClient(current_app.config['GLOBUS_CLIENT_ID'],
                                                current_app.config['GLOBUS_CLIENT_SECRET'])
