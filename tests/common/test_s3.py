# tests/common/test_s3.py
import os
import unittest
from moto import mock_aws
import boto3

# import class S3BucketConnector từ project của Q
# giả sử module đặt tại xetra.common.s3
from xetra.common.s3 import S3BucketConnector


class TestS3BucketConnectorMethods(unittest.TestCase):
    """Unit tests for S3BucketConnector.list_files_in_prefix"""

    def setUp(self):
        # Start moto's mock S3
        self.mock = mock_aws()
        self.mock.start()


        # Create a boto3 client/resource that moto will mock
        self.aws_region = "eu-central-1"
        self.endpoint_url = "https://s3.eu-central-1.amazonaws.com"  # giá trị mô phỏng
        self.bucket_name = "test-bucket"

        # Create a session/resource and bucket in moto
        session = boto3.session.Session()
        self.s3 = session.resource("s3", region_name=self.aws_region)
        # Create bucket (with LocationConstraint for some regions)
        try:
            self.s3.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration={"LocationConstraint": self.aws_region},)
        except self.s3.meta.client.exceptions.BucketAlreadyOwnedByYou:
            pass


        # Upload two test objects with a common prefix
        self.prefix = "myprefix/"
        self.obj_keys = [f"{self.prefix}file1.txt", f"{self.prefix}file2.txt"]
        for key in self.obj_keys:
            self.s3.Object(self.bucket_name, key).put(Body=b"hello")

        # Set environment variable names expected by S3BucketConnector.
        # IMPORTANT: S3BucketConnector expects env var NAMES passed in constructor,
        # and then reads os.environ[access_key_name], os.environ[secret_key_name].
        # Here we create two env vars with dummy values (since moto does not validate them).
        os.environ["AWS_ACCESS_KEY_ID_TEST"] = "testing"
        os.environ["AWS_SECRET_ACCESS_KEY_TEST"] = "testing"

        # Create the S3BucketConnector instance for testing.
        # Pass the env var NAMES (as used in the code) and endpoint + bucket name:
        # (adjust constructor args ordering/names if your implementation differs)
        self.connector = S3BucketConnector(
            access_key="AWS_ACCESS_KEY_ID_TEST",
            secret_key="AWS_SECRET_ACCESS_KEY_TEST",
            endpoint_url=self.endpoint_url,
            bucket=self.bucket_name,
        )

    def tearDown(self):
        # Stop moto mock
        self.mock.stop()
        # Clean up environment variables
        os.environ.pop("AWS_ACCESS_KEY_ID_TEST", None)
        os.environ.pop("AWS_SECRET_ACCESS_KEY_TEST", None)

    def test_list_files_in_prefix_exists(self):
        """Prefix exists -> returns list of file keys"""
        files = self.connector.list_files_in_prefix(self.prefix)
        # Order may vary, compare as sets or sort
        self.assertIsInstance(files, list)
        self.assertEqual(set(files), set(self.obj_keys))

    def test_list_files_in_prefix_not_exists(self):
        """Prefix does not exist -> returns empty list"""
        wrong_prefix = "no-such-prefix/"
        files = self.connector.list_files_in_prefix(wrong_prefix)
        self.assertIsInstance(files, list)
        self.assertEqual(files, [])


if __name__ == "__main__":
    unittest.main()
