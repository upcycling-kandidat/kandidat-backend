import os
import logging
import uuid
from dotenv import dotenv_values
from minio import Minio
from minio.error import S3Error
from PIL import Image

log = logging.getLogger("app.sub")

config = dotenv_values(".env")

client = Minio(
    config["MINIO_URL"],
    access_key=config["MINIO_ACCESS_KEY"],
    secret_key=config["MINIO_SECRET_KEY"],
    secure=False,
)

"""
Uploads a file to the MinIO server.
param str input_file: The path of the image to upload.
"""


def temp_file(filename, input_file: Image, file_ext=".jpeg"):
    new_filename = filename.rsplit(".", 1)[0] + file_ext
    input_file.save(new_filename)
    return new_filename


def upload_file(input_file: str, file_ext=".jpeg"):
    # Create a client with the MinIO server playground, its access key
    # and secret key.

    # Make 'asiatrip' bucket if not exist.
    bucket = client.bucket_exists(config["MINIO_BUCKET_NAME"])
    if not bucket:
        client.make_bucket(config["MINIO_BUCKET_NAME"])
    else:
        log.debug(f'Bucket {config["MINIO_BUCKET_NAME"]} already exists')

    try:
        output_file = str(uuid.uuid1()) + file_ext
        log.debug(f"output_file: {output_file}")
        putted = client.fput_object(
            config["MINIO_BUCKET_NAME"],
            output_file,
            input_file,
        )
    except S3Error as err:
        log.error(err)

    log.debug(f"Object name: {putted.object_name}")
    log.debug(
        f"Successfully uploaded {input_file} as {output_file} to {config['MINIO_BUCKET_NAME']}."
    )

    response = {
        "input_file": input_file,
        "output_file": output_file,
        "bucket": config["MINIO_BUCKET_NAME"],
    }

    return response
