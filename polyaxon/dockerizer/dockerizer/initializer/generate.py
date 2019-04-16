import logging

from typing import List, Optional, Tuple

from polyaxon_dockerizer import generate as dockerizer_generate

_logger = logging.getLogger('polyaxon.dockerizer')


def generate(job,
             build_path: str,
             from_image: str,
             build_steps: Optional[List[str]] = None,
             env_vars: Optional[List[Tuple[str, str]]] = None,
             nvidia_bin: str = None,
             set_lang_env: bool = True,
             uid: int = None,
             gid: int = None) -> bool:
    """Build necessary code for a job to run"""
    rendered_dockerfile = dockerizer_generate(repo_path=build_path,
                                              from_image=from_image,
                                              build_steps=build_steps,
                                              env_vars=env_vars,
                                              nvidia_bin=nvidia_bin,
                                              set_lang_env=set_lang_env,
                                              uid=uid,
                                              gid=gid)

    if rendered_dockerfile:
        job.log_dockerfile(dockerfile=rendered_dockerfile)
    return True
