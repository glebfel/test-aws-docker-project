## Docker Logs to AWS CloudWatch

This script runs a Docker container and sends its logs to AWS CloudWatch. It uses the provided Docker image and executes a specified bash command inside the container. The logs generated during this process are then sent to an AWS CloudWatch log group and stream.

### Prerequisites

Before using the script, make sure you have the following prerequisites:

- Docker installed on the machine where the script will run.
- AWS credentials with the necessary permissions to create and write to CloudWatch log groups and streams.

### Usage

```bash
python script_name.py --docker-image <DOCKER_IMAGE> --bash-command <BASH_COMMAND> --aws-cloudwatch-group <CLOUDWATCH_GROUP> --aws-cloudwatch-stream <CLOUDWATCH_STREAM> --aws-access-key-id <ACCESS_KEY_ID> --aws-secret-access-key <SECRET_ACCESS_KEY> --aws-region <REGION>
```

### Arguments

- `--docker-image` (required): Name of the Docker image to run.
- `--bash-command` (required): Bash command to execute inside the Docker container.
- `--aws-cloudwatch-group` (required): Name of the AWS CloudWatch log group where the logs will be stored.
- `--aws-cloudwatch-stream` (required): Name of the AWS CloudWatch log stream within the specified log group.
- `--aws-access-key-id` (required): AWS Access Key ID with the necessary permissions.
- `--aws-secret-access-key` (required): AWS Secret Access Key corresponding to the provided Access Key ID.
- `--aws-region` (required): AWS region where the CloudWatch log group is located.

### Example

```bash
python script_name.py --docker-image my-docker-image --bash-command "echo Hello, CloudWatch!" --aws-cloudwatch-group MyLogGroup --aws-cloudwatch-stream MyLogStream --aws-access-key-id ABCDEFGHIJKLMNOP --aws-secret-access-key 1234567890abcdefghijklmnopqrstuvwxyz --aws-region us-east-1
```

Replace the placeholder values with your specific Docker image, bash command, AWS CloudWatch log group, stream names, access key, secret key, and AWS region.
