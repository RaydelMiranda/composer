from bisect import bisect_left

import boto3
from composer_core.config import settings
from pathlib import Path


class S3Sync:
    """
    Class that holds the operations need for synchronize buckets/
    """

    def __init__(self, endpoint_url=None, *args, **kwargs):
        self._endpoint_url = endpoint_url
        self._s3_access_key = settings.s3_access_key
        self._s3_secret_key = settings.s3_secret_key

        self._s3 = boto3.client(
            's3',
            endpoint_url=self._endpoint_url,
            aws_access_key_id=self._s3_access_key,
            aws_secret_access_key=self._s3_secret_key,
            *args, **kwargs
        )

    def sync(self, source: str, dest: str) -> [str]:
        """
        Sync source to dest, this means that all elements existing in
        source that not exists in dest will be copied to dest.

        No element will be deleted.

        :param source: Source folder.
        :param dest: Destination folder.

        :return: A [str] containing the keys or filenames of those elements that where copied.
        """

        paths = self.list_source_objects(source_folder=source)
        objects = self.list_bucket_objects(dest)

        # Getting the keys and ordering in order to perform binary search
        # each time we want to check if any paths is already there.
        object_keys = [obj['Key'] for obj in objects]
        object_keys.sort()
        object_keys_length = len(object_keys)

        for path in paths:
            # Binary search.
            index = bisect_left(object_keys, path)
            if index == object_keys_length:
                # If path not found in object_keys, it has to be sync-ed.
                self._s3.upload_file(str(Path(source).joinpath(path)),  Bucket=dest, Key=path)

    def list_bucket_objects(self, bucket: str) -> [dict]:
        """
        List all objects for the given bucket.

        :param bucket: Bucket name.
        :return: A [dict] containing the elements in the bucket.

        Example of a single object.

        {
            'Key': 'CR02-R009-1/CR02-R009-1_CR02-F018-4.webp',
            'LastModified': datetime.datetime(2019, 7, 4, 13, 50, 34, 893000, tzinfo=tzutc()),
            'ETag': '"b11564415be7f58435013b414a59ae5c"',
            'Size': 115280,
            'StorageClass': 'STANDARD',
            'Owner': {
                'DisplayName': 'webfile',
                'ID': '75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a'
            }
        }

        """
        try:
            contents = self._s3.list_objects(Bucket=bucket)['Contents']
        except KeyError:
            # No Contents Key, empty bucket.
            return []
        else:
            return contents

    @staticmethod
    def list_source_objects(source_folder: str) -> [str]:
        """
        :param source_folder:  Root folder for resources you want to list.
        :return: A [str] containing relative names of the files.

        Example:

            /tmp
                - example
                    - file_1.txt
                    - some_folder
                        - file_2.txt

            >>> sync.list_source_objects("/tmp/example")
            ['file_1.txt', 'some_folder/file_2.txt']

        """

        path = Path(source_folder)

        paths = []

        for file_path in path.rglob("*"):
            if file_path.is_dir():
                continue
            str_file_path = str(file_path)
            str_file_path = str_file_path.replace(f'{str(path)}/', "")
            paths.append(str_file_path)

        return paths


if __name__ == '__main__':
    bucket_name = "COMPOSITIONS_1"

    sync = S3Sync(endpoint_url='http://localhost:4572')
    sync.sync("/home/miranda/.projects/qpy_image_composer/test_data/output", bucket_name)

    result = sync.list_bucket_objects(bucket_name)

    for elem in result:
        print(elem['Key'])
