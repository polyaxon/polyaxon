from polyaxon.exceptions import HTTP_ERROR_MESSAGES_MAPPING
from polyaxon.utils.formatting import Printer


def handle_cli_error(e, message=None):
    if message:
        Printer.print_error(message)
    Printer.print_error("Error message: {}.".format(e))
    if hasattr(e, "status"):
        Printer.print_error(HTTP_ERROR_MESSAGES_MAPPING.get(e.status))
