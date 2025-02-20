import unittest
from unittest.mock import patch, MagicMock
from utils.aws_utils import get_required_parameters

class TestAWSUtils(unittest.TestCase):

    @patch('utils.aws_utils.boto3.client')
    def test_get_required_parameters_sqs(self, mock_boto_client):
        # Mock the boto3 client and its response
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.list_queues.return_value = {'QueueUrls': ['https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue']}

        credentials = {
            'AccessKeyId': 'mock_access_key',
            'SecretAccessKey': 'mock_secret_key',
            'SessionToken': 'mock_session_token'
        }
        result = get_required_parameters('sqs', 'get_queue_attributes', 'us-east-1', credentials)
        self.assertEqual(result, {'QueueUrl': 'https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue'})

    @patch('utils.aws_utils.boto3.client')
    def test_get_required_parameters_sns(self, mock_boto_client):
        # Mock the boto3 client and its response
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.list_topics.return_value = {'Topics': [{'TopicArn': 'arn:aws:sns:us-east-1:123456789012:MyTopic'}]}

        credentials = {
            'AccessKeyId': 'mock_access_key',
            'SecretAccessKey': 'mock_secret_key',
            'SessionToken': 'mock_session_token'
        }
        result = get_required_parameters('sns', 'get_topic_attributes', 'us-east-1', credentials)
        self.assertEqual(result, {'TopicArn': 'arn:aws:sns:us-east-1:123456789012:MyTopic'})

    @patch('utils.aws_utils.boto3.client')
    def test_get_required_parameters_secretsmanager(self, mock_boto_client):
        # Mock the boto3 client and its response
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.list_secrets.return_value = {'SecretList': [{'Name': 'MySecret'}]}

        credentials = {
            'AccessKeyId': 'mock_access_key',
            'SecretAccessKey': 'mock_secret_key',
            'SessionToken': 'mock_session_token'
        }
        result = get_required_parameters('secretsmanager', 'get_secret_value', 'us-east-1', credentials)
        self.assertEqual(result, {'SecretId': 'MySecret'})

    @patch('utils.aws_utils.boto3.client')
    def test_get_required_parameters_s3(self, mock_boto_client):
        # Mock the boto3 client and its response
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        mock_client.list_buckets.return_value = {'Buckets': [{'Name': 'MyBucket'}]}

        credentials = {
            'AccessKeyId': 'mock_access_key',
            'SecretAccessKey': 'mock_secret_key',
            'SessionToken': 'mock_session_token'
        }
        result = get_required_parameters('s3', 'get_bucket_location', 'us-east-1', credentials)
        self.assertEqual(result, {'Bucket': 'MyBucket'})

    # Add more test cases for other services and functions as needed

if __name__ == '__main__':
    unittest.main()