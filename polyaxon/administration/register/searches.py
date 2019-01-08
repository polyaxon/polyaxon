from db.models.searches import Search


def register(admin_register):
    admin_register(Search)
