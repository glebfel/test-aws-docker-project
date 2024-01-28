import argparse
import logging

from src.adapters.cloudwatch import AWSCloudwatchAdapter
from src.adapters.docker import DockerAdapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Run Docker container and send logs to AWS CloudWatch.')
    parser.add_argument('--docker-image', required=True, help='Name of the Docker image')
    parser.add_argument('--bash-command', required=True, help='Bash command to run inside the Docker image')
    parser.add_argument('--aws-cloudwatch-group', required=True, help='Name of the AWS CloudWatch group')
    parser.add_argument('--aws-cloudwatch-stream', required=True, help='Name of the AWS CloudWatch stream')
    parser.add_argument('--aws-access-key-id', required=True, help='AWS Access Key')
    parser.add_argument('--aws-secret-access-key', required=True, help='AWS Secret Key')
    parser.add_argument('--aws-region', required=True, help='AWS Region')

    args = parser.parse_args()

    # initiate cloudwatch instance
    cloudwatch = AWSCloudwatchAdapter(args.aws_access_key_id, args.aws_secret_access_key, args.aws_region)
    cloudwatch.create_log_group(log_group_name=args.aws_cloudwatch_group)
    cloudwatch.create_log_stream(log_group_name=args.aws_cloudwatch_group,
                                 log_stream_name=args.aws_cloudwatch_stream)

    # run docker container
    docker = DockerAdapter()
    container = docker.run_container(image_name=args.docker_image, bash_command=args.bash_command)

    try:
        sequence_token, logs_accumulator, new_line_counter = '1', '', 0

        for log in container.logs(stream=True):
            log = log.decode('utf-8')
            new_line_counter = new_line_counter + 1 if not log.strip() else 0

            if new_line_counter == 2:
                sequence_token = cloudwatch.send_logs(
                    logs=[logs_accumulator],
                    log_group_name=args.aws_cloudwatch_group,
                    log_stream_name=args.aws_cloudwatch_stream,
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


if __name__ == '__main__':
    main()
