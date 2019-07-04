import boto3

from composer_core.config import settings


class S3Sync:
    """
    Class that holds the operations need for synchronize buckets/
    """

    @staticmethod
    def sync(source: str, dest: str) -> [str]:
        """
        Sync source to dest, this means that all elements existing in
        source that not exists in dest will be copied to dest.

        No element will be deleted.

        :param source: Source folder.
        :param dest: Destination folder.

        :return: A [str] containing the keys or filenames of those elements that where copied.
        """

        connection = boto3.client('s3')

    @staticmethod
    def list_objects(bucket: str) -> [dict]:
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

        s3 = boto3.client(
            's3',
            endpoint_url='http://localhost:4572',
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name='us-east-1'
        )

        return s3.list_objects(Bucket=bucket)['Contents']


if __name__ == '__main__':
    contents = S3Sync.list_objects("COMPOSITIONS")
    for elem in contents:
        print(elem)
