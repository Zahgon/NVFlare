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

import argparse
import logging
from typing import Any

from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider

from nvflare.edge.web.models.api_error import ApiError
from nvflare.edge.web.views.feg_views import api_query, feg_bp

log = logging.getLogger(__name__)
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


def parse_args():
    pass


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
    args = parse_args()

    proxy_port = args.port
    lcp_mapping_file = args.lcp_mapping_file
    ca_cert_file = args.ca_cert_file

    ssl_context = None
    if args.ssl_cert and args.ssl_key:
        print(f"Using SSL cert: {args.ssl_cert}")
        print(f"Using SSL key: {args.ssl_key}")
        ssl_context = (args.ssl_cert, args.ssl_key)
    else:
        print("No SSL cert/key provided, running without SSL")

    api_query.set_lcp_mapping(lcp_mapping_file)
    api_query.set_ca_cert(ca_cert_file)
    api_query.start()

    app.json = FilteredJSONProvider(app)
    app.register_blueprint(feg_bp)
    app.run(host="0.0.0.0", port=proxy_port, debug=False, ssl_context=ssl_context)
