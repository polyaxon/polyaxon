import re

from collections import deque

from hestia.list_utils import to_list

from polyaxon_cli.utils.formatting import Printer

MASTER_REGEX = re.compile(r'master\.\d+')
WORKER_REGEX = re.compile(r'worker\.\d+')
PS_REGEX = re.compile(r'ps\.\d+')
TIMESTAMP_REGEX = re.compile(r'\d{2}(?:\d{2})?-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\s\w+\s')


def get_logs_handler(handle_job_info=False, show_timestamp=True, stream=True):
    colors = deque(Printer.COLORS)
    job_to_color = {}

    def get_job_info(log_line, job_regex):
        log_search = job_regex.search(log_line)
        if not log_search:
            return log_line, False

        job_info = log_search.group()
        if job_info in job_to_color:
            color = job_to_color[job_info]
        else:
            color = colors[0]
            colors.rotate(-1)
            job_to_color[job_info] = color
        return re.sub(job_regex, Printer.add_color(job_info, color), log_line), True

    def add_job_color(log_line):
        log_line, found = get_job_info(log_line=log_line, job_regex=MASTER_REGEX)
        if found:
            return log_line
        log_line, found = get_job_info(log_line=log_line, job_regex=WORKER_REGEX)
        if found:
            return log_line
        log_line, found = get_job_info(log_line=log_line, job_regex=PS_REGEX)
        return log_line

    def handle_timestamp(log_line):
        log_search = TIMESTAMP_REGEX.search(log_line)
        if not log_search:
            return log_line

        if not show_timestamp:
            return re.sub(TIMESTAMP_REGEX, '', log_line)

        timestamp_info = log_search.group()
        return re.sub(TIMESTAMP_REGEX, Printer.add_color(timestamp_info, 'white'), log_line)

    def handle_status(status, log_lines):
        status = Printer.get_colored_status(status)
        Printer.log('{} ...'.format(status), nl=True)
        for log_line in log_lines:
            if log_line:
                log_line = handle_timestamp(log_line)
                Printer.log(log_line, nl=True)

    def handle_log_lines(log_lines):
        for log_line in log_lines:
            if log_line:
                log_line = handle_timestamp(log_line)
                if handle_job_info:
                    log_line = add_job_color(log_line=log_line)
                Printer.log(log_line, nl=True)

    def handle_logs(message):
        log_lines = to_list(message['log_lines'])
        status = message.get('status')
        if not status and log_lines:
            handle_log_lines(log_lines)
        else:
            handle_status(status, log_lines)

    return handle_logs if stream else handle_log_lines
