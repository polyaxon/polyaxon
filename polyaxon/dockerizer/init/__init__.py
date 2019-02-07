from dockerizer.constants import BUILD_PATH
from dockerizer.init.generate import generate
from dockerizer.init.git_download import download_code


def init(build_job: 'BuildJob', build_path: str = BUILD_PATH):
    # Check image if exists
    # Download repo
    filename = '_code'
    status = download_code(
        build_job=build_job,
        build_path=build_path,
        filename=filename)
    if not status:
        return status
    # Generate dockerfile
    generate(build_job=build_job, build_path=build_path)
