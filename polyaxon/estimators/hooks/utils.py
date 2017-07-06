def can_run_hook(run_context):
    ops = run_context.original_args[0]
    no_run_hooks_ops = [op.name == 'no_run_hooks' for op in ops]
    if any(no_run_hooks_ops):
        return False
    return True
