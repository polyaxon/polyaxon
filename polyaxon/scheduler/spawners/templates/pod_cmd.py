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


def get_horovod_pod_command_args(n_workers, gpus, n_processes, hosts, port, run_config):
    total_processes = n_workers * n_processes
    command, args = get_pod_command_args(run_config=run_config)
    args = (
        'mpirun --allow-run-as-root -np {}'.format(total_processes) +
        '  -x LD_LIBRARY_PATH' if gpus else '' +
        '  --tag-output' +
        '  -H {} -mca plm_rsh_args '.format(hosts) +
        '"-p {} -q -o ConnectTimeout=2 -o ConnectionAttempts=10"'.format(port) +
        '  {}'.format(args))
    return command, [args]
