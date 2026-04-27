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

import json
import logging

from werkzeug.security import check_password_hash, generate_password_hash

from .cert import Entity, make_root_cert
from .models import Client, Organization, Project, Role, User, db

log = logging.getLogger(__name__)

_PROJECT_WRITABLE = {
    "title",
    "description",
    "app_location",
    "ha_mode",
    "starting_date",
    "end_date",
    "overseer",
    "server1",
    "server2",
    "frozen",
    "public",
    "cc_mode",
}


def check_role(id, claims, requester):
    pass


def _dict_or_empty(item):
    pass


def get_or_create(session, model, **kwargs):
    pass


def add_ok(obj):
    pass


def inc_dl(model, id):
    pass


class Store(object):
    @classmethod
    def ready(cls):
        pass

    @classmethod
    def seed_user(cls, email, pwd, org):
        pass

    @classmethod
    def init_db(cls):
        pass

    @classmethod
    def create_project(cls):
        pass

    @classmethod
    def build_project(cls, project):
        pass

    @classmethod
    def _add_registered_info(cls, project_dict):
        pass

    @classmethod
    def set_project(cls, req):
        pass

    @classmethod
    def get_project(cls):
        pass

    @classmethod
    def get_orgs(cls):
        pass

    @classmethod
    def _is_approved_by_client_id(cls, id):
        pass

    @classmethod
    def _is_approved_by_user_id(cls, id):
        pass

    @classmethod
    def create_client(cls, req, creator):
        pass

    @classmethod
    def get_clients(cls, org=None):
        pass

    @classmethod
    def get_creator_id_by_client_id(cls, id):
        pass

    @classmethod
    def get_client(cls, id):
        pass

    @classmethod
    def patch_client_by_project_admin(cls, id, req):
        pass

    @classmethod
    def patch_client_by_creator(cls, id, req):
        pass

    @classmethod
    def delete_client(cls, id):
        pass

    @classmethod
    def create_user(cls, req, seeding=False):
        pass

    @classmethod
    def verify_user(cls, email, password):
        pass

    @classmethod
    def get_users(cls, org_name=None):
        pass

    @classmethod
    def _get_email_by_id(cls, id):
        pass

    @classmethod
    def get_user(cls, id):
        pass

    @classmethod
    def patch_user_by_project_admin(cls, id, req):
        pass

    @classmethod
    def patch_user_by_creator(cls, id, req):
        pass

    @classmethod
    def delete_user(cls, id):
        pass
