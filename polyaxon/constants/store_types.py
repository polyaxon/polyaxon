class StoreTypes(object):
    HOST_PATH = 'host_path'
    VOLUME_CLAIM = 'volume_claim'
    GCS = 'gcs'
    S3 = 's3'
    AZURE = 'azure'

    VALUES = {HOST_PATH, VOLUME_CLAIM, GCS, S3, AZURE}
    CLOUD_STORES = {GCS, S3, AZURE}

    CHOICES = (
        (HOST_PATH, HOST_PATH),
        (VOLUME_CLAIM, VOLUME_CLAIM),
        (GCS, GCS),
        (S3, S3),
        (AZURE, AZURE)
    )
