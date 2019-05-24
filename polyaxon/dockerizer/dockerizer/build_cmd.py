import argparse

from builders import settings  # noqa
from polyaxon_dockerizer import build_and_push

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--build_context',
        type=str
    )
    parser.add_argument(
        '--image_name',
        type=str
    )
    parser.add_argument(
        '--image_tag',
        type=str
    )
    parser.add_argument(
        '--nocache',
        dest='nocache',
        action='store_true'
    )
    parser.set_defaults(nocache=False)
    args = parser.parse_args()
    arguments = args.__dict__

    build_context = arguments.pop('build_context')
    image_name = arguments.pop('image_name')
    image_tag = arguments.pop('image_tag')
    nocache = arguments.pop('nocache')

    build_and_push(
        build_context=build_context,
        image_name=image_name,
        image_tag=image_tag,
        nocache=nocache,
        registries=settings.PRIVATE_REGISTRIES)
