from pathlib import Path
import pytest

from kipoi_containers.dockerhelper import (
    build_docker_image,
    cleanup,
    push_docker_image,
    test_docker_image,
)


class DockerUpdater:
    def __init__(self, model_group, name_of_docker_image):
        """
        This function instantiate the DockerUpdater class
        """
        self.model_group = model_group
        self.name_of_docker_image = name_of_docker_image

    def update(self, models_to_test):
        """
        This functions rebuilds the given docker image for the given modelgroup and
        tests all the models with this new image. The steps are -
        1. Rebuild the image
        2. Rerun the tests for this image

        Parameters
        ----------
        model_group : str
            Model group which has been updated in the kipoi model repo
        name_of_docker_image : str
            Corresponding name of the docker image

        Raises
        ------
        ValueError
            exitcode from the pytest instance that ran to ensure the new image
            is working with all the models under the group named <model_group>
        """
        print(f"Updating {self.model_group} and {self.name_of_docker_image}")
        if self.model_group in [
            "MMSplice/mtsplice",
            "APARENT/veff",
            "APARENT/site_probabilities",
        ]:
            dockerfile_name = (
                f"Dockerfile.{self.model_group.replace('/', '-').lower()}"
            )
        elif self.model_group in [
            "MMSplice/pathogenicity",
            "MMSplice/splicingEfficiency",
            "MMSplice/deltaLogitPSI",
            "MMSplice/modularPredictions",
        ]:
            dockerfile_name = "Dockerfile.mmsplice"
        else:
            dockerfile_name = (
                f"Dockerfile.{self.model_group.split('/')[0].lower()}"
            )
        dockerfile_path = Path.cwd() / "dockerfiles" / dockerfile_name
        if dockerfile_path.exists():
            build_docker_image(
                dockerfile_path=dockerfile_path,
                name_of_docker_image=self.name_of_docker_image,
            )
            for model in models_to_test:
                test_docker_image(
                    image_name=self.name_of_docker_image, model_name=model
                )
            push_docker_image(tag=self.name_of_docker_image.split(":")[1])
            cleanup(images=True)
        else:
            raise ValueError(
                f"{self.model_group} needs to be containerized first"
            )
