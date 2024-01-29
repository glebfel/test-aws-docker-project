import logging

from docker.models.containers import Container

from src.adapters.cloudwatch import AWSCloudwatchAdapter
from src.adapters.docker import DockerAdapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_exception(ex):
    if 'The security token included in the request is invalid' in str(ex):
        logger.error("Invalid aws-access-key-id. Check your credentials...")
    elif 'Check your AWS Secret Access Key' in str(ex):
        logger.error("Invalid aws-secret-access-key. Check your credentials...")
    elif 'Error while fetching server API version' in str(ex):
        logger.error("Docker daemon has not been started yet ...")
    elif 'repository does not exist' in str(ex):
        logger.error(f"Docker image does not exist ...")
    else:
        raise


def clean_up_resources(docker: DockerAdapter | None,
                       cloudwatch: AWSCloudwatchAdapter | None,
                       container: Container | None):
    logger.error("Cleaning up all resources ...")
    container.stop() if container else None
    cloudwatch.close() if cloudwatch else None
    docker.close() if docker else None
