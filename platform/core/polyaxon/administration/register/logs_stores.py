from db.models.logs_stores import LogsStore


def register(admin_register):
    admin_register(LogsStore)
