from fileinput import FileInput

import boto3


from src.storage.base import Storage


class AWSStorage(Storage):
    def __init__(
        self,
        bucket_name: str,
        region: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
    ):
        self.__bucket_name = bucket_name
        self.__region = region
        self.__conn = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def save_file(self, file: FileInput):
        key = f"public/{self.get_secure_filename(file.filename())}"
        self.__conn.put_object(
            Bucket=self.__bucket_name, Key=key, Body=file, CacheControl="max-age=259200"
        )
        return f"https://{self.__bucket_name}.s3.{self.__region}.amazonaws.com/{key}"
