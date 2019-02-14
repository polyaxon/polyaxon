import argparse

from initializer.init import cmd  # noqa
from polyaxon_client.tracking import BuildJob

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--build_context',
        type=str
    )
    parser.add_argument(
        '--from_image',
        type=str
    )
    parser.add_argument(
        '--commit',
        type=str,
        default=None,
    )
    parser.add_argument(
        '--context_path',
        type=str,
        default=None,
    )
    parser.add_argument(
        '--dockerfile_path',
        type=str,
        default=None,
    )
    args = parser.parse_args()
    arguments = args.__dict__

    build_context = arguments.pop('build_context')
    from_image = arguments.pop('from_image')
    commit = arguments.pop('commit')
    context_path = arguments.pop('context_path')
    dockerfile_path = arguments.pop('dockerfile_path')

    job = BuildJob()
    cmd(job=job,
        build_context=build_context,
        from_image=from_image,
        commit=commit,
        context_path=context_path,
        dockerfile_path=dockerfile_path)
