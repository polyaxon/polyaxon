import os

from polyaxon.env_vars.keys import POLYAXON_KEYS_RUN_INSTANCE
from polyaxon.exceptions import PolyaxonClientException


def get_run_info():
    job_instance = os.getenv(POLYAXON_KEYS_RUN_INSTANCE, None)
    if not job_instance:
        raise PolyaxonClientException(
            "Could get run info, "
            "please make sure this is run is correctly started by Polyaxon."
        )

    parts = job_instance.split(".")
    if not len(parts) == 4:
        raise PolyaxonClientException(
            "run instance is invalid `{}`, "
            "please make sure this is run is correctly started by Polyaxon.".format(
                job_instance
            )
        )
    return parts[0], parts[1], parts[-1]
