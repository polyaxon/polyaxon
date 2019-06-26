import argparse
import time

from requests.exceptions import ConnectionError

from polyaxon_client.client import PolyaxonClient


def create_experiment_auth_context(experiment_name: str):
    parts = experiment_name.split('.')
    client = PolyaxonClient()
    client.auth.login_experiment_impersonate_token(username=parts[0],
                                                   project_name=parts[1],
                                                   experiment_id=parts[-1],
                                                   internal_token=client.api_config.token)


def create_job_auth_context(job_name: str):
    parts = job_name.split('.')
    client = PolyaxonClient()
    client.auth.login_job_impersonate_token(username=parts[0],
                                            project_name=parts[1],
                                            job_id=parts[-1],
                                            internal_token=client.api_config.token)


def create_notebook_auth_context(job_name: str):
    parts = job_name.split('.')
    client = PolyaxonClient()
    client.auth.login_notebook_impersonate_token(username=parts[0],
                                                 project_name=parts[1],
                                                 internal_token=client.api_config.token)


def _create_auth_context():
    if entity == 'experiment':
        create_experiment_auth_context(experiment_name=entity_name)
    elif entity == 'job':
        create_job_auth_context(job_name=entity_name)
    elif entity == 'notebook':
        create_notebook_auth_context(job_name=entity_name)
    else:
        raise ValueError('Entity `{}` not recognized'.format(entity))

    return True


def create_auth_context():
    retry = 0
    done = False
    while not done and retry < 3:
        try:
            done = _create_auth_context()
        except ConnectionError:
            retry += 1
            print('Could not establish connection, retrying ...')
            time.sleep(sleep_interval)

    # One last attempt
    _create_auth_context()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--entity',
        type=str
    )
    parser.add_argument(
        '--entity_name',
        type=str
    )
    parser.add_argument(
        '--sleep_interval',
        default=2,
        type=int
    )
    parser.set_defaults(nocache=False)
    args = parser.parse_args()
    arguments = args.__dict__

    entity = arguments.pop('entity')
    entity_name = arguments.pop('entity_name')
    sleep_interval = arguments.pop('sleep_interval')

    create_auth_context()
