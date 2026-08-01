from minio import Minio

from app.env import settings

def get_storage() -> Minio:
    return Minio(
        endpoint   = settings.garage_endpoint,
        access_key = settings.garage_default_access_key,
        secret_key = settings.garage_default_secret_key,
        region     = 'garage',
        secure     = False
    )


if __name__ == "__main__":

    storage = get_storage()

    print(storage.list_buckets())
