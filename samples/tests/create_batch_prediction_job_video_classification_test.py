# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from uuid import uuid4
import pytest
import os

import helpers

from samples import (
    create_batch_prediction_job_video_classification_sample,
    cancel_batch_prediction_job_sample,
    delete_batch_prediction_job_sample,
)

PROJECT_ID = os.getenv("BUILD_SPECIFIC_GCLOUD_PROJECT")
LOCATION = "us-central1"
MODEL_ID = "667940119734386688"  # Permanent 5 class sports model
DISPLAY_NAME = f"temp_create_batch_prediction_vcn_test_{uuid4()}"
GCS_SOURCE_URI = (
    "gs://ucaip-samples-test-output/inputs/vcn_40_batch_prediction_input.jsonl"
)
GCS_OUTPUT_URI = "gs://ucaip-samples-test-output/"


@pytest.fixture(scope="function")
def shared_state():

    shared_state = {}

    yield shared_state

    assert "/" in shared_state["batch_prediction_job_name"]

    batch_prediction_job = shared_state["batch_prediction_job_name"].split("/")[-1]

    # Stop the batch prediction job
    cancel_batch_prediction_job_sample.cancel_batch_prediction_job_sample(
        project=PROJECT_ID, batch_prediction_job_id=batch_prediction_job
    )

    # Delete the batch prediction job
    delete_batch_prediction_job_sample.delete_batch_prediction_job_sample(
        project=PROJECT_ID, batch_prediction_job_id=batch_prediction_job
    )


# Creating AutoML Video Classification batch prediction job
def test_ucaip_generated_create_batch_prediction_vcn_sample(capsys, shared_state):

    model_name = f"projects/{PROJECT_ID}/locations/{LOCATION}/models/{MODEL_ID}"

    create_batch_prediction_job_video_classification_sample.create_batch_prediction_job_video_classification_sample(
        project=PROJECT_ID,
        display_name=DISPLAY_NAME,
        model_name=model_name,
        gcs_source_uri=GCS_SOURCE_URI,
        gcs_destination_output_uri_prefix=GCS_OUTPUT_URI,
    )

    out, _ = capsys.readouterr()

    # Save resource name of the newly created batch prediction job
    shared_state["batch_prediction_job_name"] = helpers.get_name(out)