import docker
from docker import DockerClient


class DockerAdapter:
    def __init__(self):
        self._client = None

    @property
    def client(self) -> DockerClient:
        if not self._client:
            self._client = docker.from_env()
        return self._client

    def run_container(self, image_name: str, bash_command: str | None = None):
        return self.client.containers.run(image_name, command=bash_command, detach=True, tty=True)

    def close(self):
        if self._client is not None:
            self._client.close()
            self._client = None
