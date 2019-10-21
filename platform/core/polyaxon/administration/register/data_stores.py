from db.models.data_stores import DataStore


def register(admin_register):
    admin_register(DataStore)
