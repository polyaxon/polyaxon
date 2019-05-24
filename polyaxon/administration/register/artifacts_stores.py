from db.models.artifacts_stores import ArtifactsStore


def register(admin_register):
    admin_register(ArtifactsStore)
