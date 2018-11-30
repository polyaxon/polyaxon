from hestia.string_utils import strip_spaces


def get_pod_command_args(run_config):
    if not run_config or not run_config.cmd:
        raise ValueError('The specification must contain a command.')

    def sanitize_cmd(cmd):
        cmd = strip_spaces(value=cmd, join=False)
        cmd = [c.strip().strip('\\') for c in cmd if (c and c != '\\')]
        cmd = [c for c in cmd if (c and c != '\\')]
        return ' '.join(cmd)

    return (
        ["/bin/bash", "-c"],
        [' && '.join([sanitize_cmd(cmd) for cmd in run_config.cmd])]
        if isinstance(run_config.cmd, list)
        else [sanitize_cmd(run_config.cmd)]
    )
