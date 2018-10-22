from hestia.string_utils import strip_spaces


def get_pod_command_args(run_config):
    if not run_config or not run_config.cmd:
        raise ValueError('The specification must contain a command.')

    cmd = strip_spaces(value=run_config.cmd, join=False)
    cmd = [c.strip().strip('\\') for c in cmd if (c and c != '\\')]
    cmd = [c for c in cmd if (c and c != '\\')]
    return cmd, []
