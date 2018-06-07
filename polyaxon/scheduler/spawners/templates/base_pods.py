def get_pod_command_args(run_config):
    if not run_config or not run_config.cmd:
        raise ValueError('The specification must contain a command.')

    cmd = run_config.cmd.split(' ')
    cmd = [c.strip().strip('\\') for c in cmd if (c and c != '\\')]
    cmd = [c for c in cmd if (c and c != '\\')]
    return cmd, []
