import argparse
import logging

from src.docker_logs import process_logs

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

    process_logs(
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        aws_region=args.aws_region,
        aws_cloudwatch_group=args.aws_cloudwatch_group,
        aws_cloudwatch_stream=args.aws_cloudwatch_stream,
        docker_image=args.docker_image,
        bash_command=args.bash_command,
    )


if __name__ == '__main__':
    main()
