import logging
import sys
import threading
from os import listdir, path
from os.path import isfile, join
import boto3
from botocore.exceptions import ClientError
from settings import BUCKET_NAME, S3_REGION, S3_KEY, S3_SECRET


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


class S3Uploader(object):
    def __init__(self):
        self.__client = boto3.client(
            's3',
            region_name=S3_REGION,
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )

    def upload_folder_content(self, folder_path: str, target_storage_path: str) -> None:
        files = [f for f in listdir(folder_path) if isfile(join(folder_path, f)) and f.endswith(".mp3")]
        for f in files:
            self.__single_file_upload(join(folder_path, f), join(target_storage_path, f))

    def __single_file_upload(self, target_file: str, target_storage_path: str) -> bool:
        try:
            response = self.__client.upload_file(
                target_file,
                BUCKET_NAME,
                target_storage_path,
                Callback=ProgressPercentage(target_file)
            )
            logging.info("{}".format(response))
        except ClientError as e:
            logging.error(e)
            return False
        return True
