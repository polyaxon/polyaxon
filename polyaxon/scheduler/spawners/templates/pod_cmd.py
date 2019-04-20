def get_horovod_pod_command_args(n_workers, gpus, n_processes, hosts, port, run_config):
    total_processes = n_workers * n_processes
    command, args = run_config.get_container_cmd()
    args = (
        'mpirun --allow-run-as-root -np {}'.format(total_processes) +
        ('  -x LD_LIBRARY_PATH' if gpus else '') +
        '  --tag-output' +
        '  -H {} -mca plm_rsh_args '.format(hosts) +
        '"-p {} -q -o ConnectTimeout=2 -o ConnectionAttempts=10"'.format(port) +
        '  {}'.format(args[0]))
    return command, [args]
