import os
import requests
import json
from pathlib import Path

import pytest

from modelupdater import singularityhelper, singularityhandler
from modelupdater import zenodoclient


@pytest.fixture(scope="module")
def zenodo_client():
    return zenodoclient.Client()


def test_zenodo_get_access(zenodo_client):
    response_json = zenodo_client.get_content(
        "https://zenodo.org/api/deposit/depositions"
    )
    assert len(response_json) == 10  # By default zenodo page size is 10


def test_get_available_sc_depositions(zenodo_client):
    singularity_handler = singularityhandler.SingularityHandler(
        "Basset", "Dummy"
    )
    singularity_container_number = (
        singularityhelper.total_number_of_singularity_containers(
            (singularity_handler.model_group_to_image_dict.values())
        )
    )
    extra_kwargs = {
        "status": "published",
        "q": "singularity container",
        "size": singularity_container_number,
    }

    response_json = zenodo_client.get_content(
        "https://zenodo.org/api/deposit/depositions", **extra_kwargs
    )

    assert len(response_json) == singularity_container_number
    for index, item in enumerate(response_json):
        for file_obj in item["files"]:
            assert (
                "kipoi-docker" in file_obj["filename"]
                or "busybox_latest" in file_obj["filename"]
            )


def test_get_existing_sc_by_recordid(zenodo_client):
    response_json = zenodo_client.get_content(
        "https://zenodo.org/api/deposit/depositions/5643929"
    )
    assert (
        response_json["files"][0]["filename"] == "kipoi-docker_deeptarget.sif"
    )


def test_update_existing_singularity_container(zenodo_client):
    test_singularity_dict = {
        "url": "https://zenodo.org/record/5725936/files/tiny-container_latest.sif?download=1",
        "name": "tiny-container_latest.sif",
        "md5": "0a85bfc85e749894210d1e53b4add11d",
    }
    new_test_singularity_dict = (
        singularityhelper.update_existing_singularity_container(
            zenodo_client=zenodo_client,
            singularity_dict=test_singularity_dict,
            singularity_image_folder=Path(__file__).parent.resolve(),
            model_group="Test",
            file_to_upload="busybox_1.34.1.sif",
            cleanup=False,
        )
    )
    for key in ["url", "md5", "name"]:
        assert new_test_singularity_dict.get(key) == test_singularity_dict.get(
            key
        )  # If push=True this will be different
    assert new_test_singularity_dict["file_id"] == ""
    zenodo_client.delete_content(
        f"https://zenodo.org/api/deposit/depositions/{new_test_singularity_dict.get('new_deposition_id')}"
    )


def test_push_new_singularity_image(zenodo_client):
    test_singularity_dict = {
        "url": "https://zenodo.org/record/5725936/files/tiny-container_latest.sif?download=1",
        "name": "tiny-container_latest.sif",
        "md5": "0a85bfc85e749894210d1e53b4add11d",
    }
    new_singularity_dict = singularityhelper.push_new_singularity_image(
        zenodo_client=zenodo_client,
        singularity_image_folder=Path(__file__).parent.resolve(),
        singularity_dict=test_singularity_dict,
        model_group="Dummy",
        file_to_upload="busybox_1.34.1.sif",
        cleanup=False,
    )
    for key in ["url", "md5", "name"]:
        assert test_singularity_dict.get(key) == new_singularity_dict.get(key)
    zenodo_client.delete_content(
        f"https://zenodo.org/api/deposit/depositions/{new_singularity_dict.get('new_deposition_id')}"
    )
