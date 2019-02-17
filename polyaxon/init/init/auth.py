import argparse

from polyaxon_client.client import PolyaxonClient


def create_experiment_auth_context(entity_name: str):
    parts = entity_name.split('.')
    client = PolyaxonClient()
    client.auth.login_experiment_impersonate_token(username=parts[0],
                                                   project_name=parts[1],
                                                   experiment_id=parts[-1],
                                                   internal_token=client.api_config.token)


def create_job_auth_context(entity_name: str):
    parts = entity_name.split('.')
    client = PolyaxonClient()
    client.auth.login_job_impersonate_token(username=parts[0],
                                            project_name=parts[1],
                                            job_id=parts[-1],
                                            internal_token=client.api_config.token)


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
    parser.set_defaults(nocache=False)
    args = parser.parse_args()
    arguments = args.__dict__

    entity = arguments.pop('entity')
    entity_name = arguments.pop('entity_name')

    if entity == 'experiment':
        create_experiment_auth_context(entity_name=entity_name)
    elif entity == 'job':
        create_job_auth_context(entity_name=entity_name)
    # elif entity == 'notebook':
    #     create_notebook_auth_context(username=username,
    #                                  project_name=project_name,
    #                                  job_id=entity_id)

    else:
        raise ValueError('Entity `{}` not recognized'.format(entity))
