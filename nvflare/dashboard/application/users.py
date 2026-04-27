# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

from flask import current_app as app
from flask import jsonify, make_response, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from nvflare.dashboard.application.constants import FLARE_DASHBOARD_NAMESPACE

from .blob import gen_user_blob
from .store import Store, check_role


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/users", methods=["POST"])
def create_one_user():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/users", methods=["GET"])
@jwt_required()
def get_all_users():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/users/<id>", methods=["GET"])
@jwt_required()
def get_one_user(id):
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/users/<id>", methods=["PATCH", "DELETE"])
@jwt_required()
def update_user(id):
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/users/<int:id>/blob", methods=["POST"])
@jwt_required()
def user_blob(id):
    pass
