from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
import subprocess


@shared_task(name=("search_in_dataset"))
def search_in_dataset(query, dataset_path):
    dataset_path = dataset_path.replace("\n", "")
    command = [
        settings.SIFT_BIN,
        "--exclude-files=info.json",
        "--no-filename",
        "--blocksize=200M",
        query,
        dataset_path,
    ]
    output = subprocess.run(command, capture_output=True)
    output = output.stdout.decode("utf-8")
    output = output.replace(dataset_path + ":", "")
    output = output.splitlines()
    return output
