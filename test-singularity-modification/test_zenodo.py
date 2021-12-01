import os
import requests
import json
from pathlib import Path

from modelupdater import singularityhelper

from modelupdater import zenodoclient


def test_zenodo_get_access():
    zenodo_client = zenodoclient.Client()
    response_json = zenodo_client.get_content(
        "https://zenodo.org/api/deposit/depositions"
    )
    assert len(response_json) == 10  # By default zenodo page size is 10


def test_get_available_sc_depositions():
    zenodo_client = zenodoclient.Client()
    singularity_container_number = (
        singularityhelper.total_number_of_singularity_containers(
            singularityhelper.populate_singularity_container_info().values()
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


def test_get_existing_sc_by_recordid():
    zenodo_client = zenodoclient.Client()
    response_json = zenodo_client.get_content(
        "https://zenodo.org/api/deposit/depositions/5643929"
    )
    assert (
        response_json["files"][0]["filename"] == "kipoi-docker_deeptarget.sif"
    )


# def test_push_new_singularity_image():
#     test_singularity_dict = {
#         "url": "https://zenodo.org/record/5725936/files/tiny-container_latest.sif?download=1",
#         "name": "tiny-container_latest.sif",
#         "md5": "0a85bfc85e749894210d1e53b4add11d",
#     }
#     (
#         deposition_id,
#         new_singularity_dict,
#     ) = singularityhelper.push_new_singularity_image(
#         test_singularity_dict,
#         model_group="Dummy",
#         file_to_upload="busybox_1.34.1.sif",
#         path=Path(__file__).parent.resolve(),
#         cleanup=False,
#     )
#     assert test_singularity_dict == new_singularity_dict
#     r = requests.delete(
#         f"https://zenodo.org/api/deposit/depositions/{deposition_id}",
#         params=singularityhelper.get_zenodo_access_token(),
#     )
#     assert r.status_code == 204


# def test_update_existing_singularity_container():
#     test_singularity_dict = {
#         "url": "https://zenodo.org/record/5725936/files/tiny-container_latest.sif?download=1",
#         "name": "tiny-container_latest.sif",
#         "md5": "0a85bfc85e749894210d1e53b4add11d",
#     }
#     (
#         new_deposition_id,
#         _,
#         new_test_singularity_dict,
#     ) = singularityhelper.update_existing_singularity_container(
#         test_singularity_dict,
#         model_group="Test",
#         file_to_upload="busybox_1.34.1.sif",
#         path=Path(__file__).parent.resolve(),
#         cleanup=False,
#     )
#     assert (
#         new_test_singularity_dict == test_singularity_dict
#     )  # If push=True this will be different
#     r = requests.delete(
#         f"https://zenodo.org/api/deposit/depositions/{new_deposition_id}",
#         params=singularityhelper.get_zenodo_access_token(),
#     )
#     assert r.status_code == 204
