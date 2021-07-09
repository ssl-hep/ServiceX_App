import os
import tempfile

import pytest

config_params = {
    'TESTING': True,
    'SECRET_KEY': 'secret',
    'WTF_CSRF_ENABLED': False,
    'RABBIT_MQ_URL': 'amqp://foo.com',
    'RABBIT_RETRIES': 12,
    'RABBIT_RETRY_INTERVAL': 10,
    'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'TRANSFORMER_RABBIT_MQ_URL': "amqp://trans.rabbit",
    'TRANSFORMER_DEFAULT_IMAGE': "sslhep/servicex_func_adl_xaod_transformer:1.0.0-RC.3",
    'TRANSFORMER_NAMESPACE': "my-ws",
    'TRANSFORMER_MANAGER_ENABLED': False,
    'TRANSFORMER_MANAGER_MODE': 'internal-kubernetes',
    'TRANSFORMER_AUTOSCALE_ENABLED': True,
    'ADVERTISED_HOSTNAME': 'cern.analysis.ch:5000',
    'TRANSFORMER_PULL_POLICY': 'Always',
    'OBJECT_STORE_ENABLED': False,
    'MINIO_URL': 'localhost:9000',
    'MINIO_ACCESS_KEY': 'miniouser',
    'MINIO_SECRET_KEY': 'leftfoot1',
    'CODE_GEN_IMAGE': 'sslhep/servicex_code_gen_func_adl_xaod:develop',
    'CODE_GEN_SERVICE_URL': 'http://localhost:5001',
    'ENABLE_AUTH': False,
    'GLOBUS_CLIENT_ID': 'globus-client-id',
    'GLOBUS_CLIENT_SECRET': 'globus-client-secret',
    'DID_FINDER_DEFAULT_SCHEME': 'rucio',
    'VALID_DID_SCHEMES': ['rucio'],
    'JWT_ADMIN': 'admin',
    'JWT_PASS': 'pass',
    'JWT_SECRET_KEY': 'schtum',
}

test_params = {
    'TESTING': True,
    'SECRET_KEY': 'testvalue',
    'WTF_CSRF_ENABLED': True,
    'RABBIT_MQ_URL': 'amqp://test.com',
    'RABBIT_RETRIES': 99,
    'RABBIT_RETRY_INTERVAL': 99,
    'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'TRANSFORMER_RABBIT_MQ_URL': "amqp://test.rabbit",
    'TRANSFORMER_DEFAULT_IMAGE': "sslhep/servicex_func_adl_xaod_transformer:1.0.0-RC.3-test",
    'TRANSFORMER_NAMESPACE': "test-value",
    'TRANSFORMER_MANAGER_ENABLED': False,
    'TRANSFORMER_MANAGER_MODE': 'external-kubernetes',
    'TRANSFORMER_AUTOSCALE_ENABLED': False,
    'ADVERTISED_HOSTNAME': 'test.ch:5000',
    'TRANSFORMER_PULL_POLICY': 'Never',
    'OBJECT_STORE_ENABLED': False,
    'MINIO_URL': 'localhost.test:9000',
    'MINIO_ACCESS_KEY': 'testuser',
    'MINIO_SECRET_KEY': 'testpass',
    'CODE_GEN_IMAGE': 'sslhep/servicex_code_gen_func_adl_xaod:test',
    'CODE_GEN_SERVICE_URL': 'http://localhost.test:5001',
    'ENABLE_AUTH': True,
    'GLOBUS_CLIENT_ID': 'test-value',
    'GLOBUS_CLIENT_SECRET': 'test-secret',
    'DID_FINDER_DEFAULT_SCHEME': 'rucio',
    'VALID_DID_SCHEMES': "['rucio']",
    'JWT_ADMIN': 'testadmin',
    'JWT_PASS': 'jwtpass',
    'JWT_SECRET_KEY': 'testkey',
}


@pytest.fixture
def config_file():
    with tempfile.NamedTemporaryFile(mode="w+") as temp_file:
        for k, v in config_params.items():
            if type(v) == str:
                temp_file.write(f"{k} = '{v}'\n")
            else:
                temp_file.write(f"{k} = {v}\n")
        temp_file.flush()
        yield temp_file.name


@pytest.mark.parametrize("env_param", test_params.keys())
def test_env_config(env_param):
    """
    Test to make sure that configuration in the environment
    overrides regular configuration
    """
    from servicex import create_app
    os.environ[env_param] = str(test_params[env_param])
    app = create_app(test_config=config_params)
    assert (app.config[env_param] == test_params[env_param])
    del os.environ[env_param]
