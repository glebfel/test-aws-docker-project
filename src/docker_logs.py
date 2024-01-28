import logging

from src.adapters.cloudwatch import AWSCloudwatchAdapter
from src.adapters.docker import DockerAdapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_logs(aws_access_key_id: str,
                 aws_secret_access_key: str,
                 aws_region: str,
                 aws_cloudwatch_group: str,
                 aws_cloudwatch_stream: str,
                 docker_image: str,
                 bash_command: str,):
    # initiate cloudwatch instance
    cloudwatch = AWSCloudwatchAdapter(access_key=aws_access_key_id,
                                      secret_key=aws_secret_access_key,
                                      region_name=aws_region)
    cloudwatch.create_log_group(log_group_name=aws_cloudwatch_group)
    cloudwatch.create_log_stream(log_group_name=aws_cloudwatch_group,
                                 log_stream_name=aws_cloudwatch_stream)

    # run docker container
    docker = DockerAdapter()
    container = docker.run_container(image_name=docker_image, bash_command=bash_command)

    try:
        sequence_token, logs_accumulator, new_line_counter = '1', '', 0

        for log in container.logs(stream=True):
            log = log.decode('utf-8')
            new_line_counter = new_line_counter + 1 if not log.strip() else 0

            if new_line_counter == 2:
                sequence_token = cloudwatch.send_logs(
                    logs=[logs_accumulator],
                    log_group_name=aws_cloudwatch_group,
                    log_stream_name=aws_cloudwatch_stream,
                    sequence_token=sequence_token
                )
                logger.info(logs_accumulator)
                logs_accumulator, new_line_counter = '', 0
                continue

            logs_accumulator += log
    except KeyboardInterrupt:
        container.stop()
        cloudwatch.close()
        docker.close()
