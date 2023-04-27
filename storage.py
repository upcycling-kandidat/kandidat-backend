from dotenv import dotenv_values
from minio import Minio
from minio.error import S3Error

config = dotenv_values(".env")

client = Minio(
    "localhost:9000",
    access_key=config["MINIO_ACCESS_KEY"],
    secret_key=config["MINIO_SECRET_KEY"],
    secure=False,
)


def upload_file(input_file):
    # Create a client with the MinIO server playground, its access key
    # and secret key.

    # Make 'asiatrip' bucket if not exist.
    bucket = client.bucket_exists(config["MINIO_BUCKET_NAME"])
    if not bucket:
        client.make_bucket(config["MINIO_BUCKET_NAME"])
    else:
        print(f'Bucket {config["MINIO_BUCKET_NAME"]} already exists')

    try:
        output_file = f"results/{input_file}"
        putted = client.fput_object(
            config["MINIO_BUCKET_NAME"], output_file, input_file,
        )
    except S3Error as err:
        print(err)

    print(putted.object_name)
    print(
        f"Successfully uploaded {input_file} as {output_file} to {config['MINIO_BUCKET_NAME']}."
    )

    return putted


if __name__ == "__main__":
    upload_file("./test.jpeg")