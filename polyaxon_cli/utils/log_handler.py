from polyaxon_cli.utils.formatting import Printer
from polyaxon_schemas.utils import to_list


def handle_job_logs(message):
    log_lines = to_list(message['log_lines'])
    status = message.get('status')
    if not status and log_lines:
        for log_line in log_lines:
            Printer.log(log_line, nl=True)
    else:
        status = Printer.get_colored_status(status)
        Printer.log('{} ...'.format(status))
        for log_line in log_lines:
            Printer.log(log_line, nl=True)
