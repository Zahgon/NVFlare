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
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from nvflare.dashboard.application.constants import FLARE_DASHBOARD_NAMESPACE

from . import jwt
from .blob import gen_server_blob
from .store import Store


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/application-config")
def application_config_html():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/downloads")
def downloads_html():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE, strict_slashes=False)
def index_html_dashboard():
    pass


@app.route("/")
def index_html():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/logout")
def logout_html():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/project-admin-dashboard")
def project_admin_dashboard_html():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/project-configuration")
def project_configuration_html():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/registration-form")
def registration_form_html():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/server-config")
def server_config_html():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/site-dashboard")
def site_dashboard_html():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/user-dashboard")
def user_dashboard_html():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/login", methods=["POST"])
def login():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/overseer/blob", methods=["POST"])
@jwt_required()
def overseer_blob():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/servers/<int:id>/blob", methods=["POST"])
@jwt_required()
def server_blob(id):
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/project", methods=["PATCH"])
@jwt_required()
def set_project():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/project", methods=["GET"])
def get_project():
    pass


@app.route(FLARE_DASHBOARD_NAMESPACE + "/api/v1/organizations", methods=["GET"])
def get_orgs():
    pass
