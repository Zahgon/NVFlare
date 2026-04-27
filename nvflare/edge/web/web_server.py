# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Any

from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider

from nvflare.edge.web.models.api_error import ApiError
from nvflare.edge.web.views.feg_views import feg_bp

app = Flask(__name__)


def clean_dict(value: Any):
    pass


class FilteredJSONProvider(DefaultJSONProvider):
    sort_keys = False

    def dumps(self, obj: Any, **kwargs: Any) -> str:
        pass


@app.errorhandler(ApiError)
def handle_api_error(error: ApiError):
    pass


def run_server(host, port):
    pass


if __name__ == "__main__":
    # This is for testing web server startup only. Web server will not work standalone
    run_server("localhost", 8101)
