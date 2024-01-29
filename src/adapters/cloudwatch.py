import logging
import time

import boto3
from botocore.client import BaseClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AWSCloudwatchAdapter:
    def __init__(self, access_key: str, secret_key: str, region_name: str):
        self._session = boto3.Session(
            aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name
        )
        self._client = None

    @property
    def client(self) -> BaseClient:
        if not self._client:
            self._client = self._session.client('logs')
        return self._client

    def create_log_group(self, log_group_name: str):
        try:
            self.client.create_log_group(logGroupName=log_group_name)
        except self.client.exceptions.ResourceAlreadyExistsException:
            logger.warning(f'Log group {log_group_name} already exists')

    def create_log_stream(self, log_group_name: str, log_stream_name: str):
        try:
            self.client.create_log_stream(logGroupName=log_group_name,
                                          logStreamName=log_stream_name)
        except self.client.exceptions.ResourceAlreadyExistsException:
            logger.warning(f'Log stream {log_stream_name} already exists')

    def send_logs(self, logs: list[str],
                  log_group_name: str,
                  log_stream_name: str,
                  sequence_token: str = '1') -> str:
        """
        Send logs to AWS CloudWatch
        :return: The sequence token for the next PutLogEvents call (in boto3 version 1.34+ is ignored)
        """
        log_events = [{'timestamp': int(time.time() * 1000), 'message': log} for log in logs]

        res = self.client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events,
            sequenceToken=sequence_token
        )

        return res['nextSequenceToken']

    def close(self):
        if self._client is not None:
            self._client.close()
            self._cloudwatch_client = None
