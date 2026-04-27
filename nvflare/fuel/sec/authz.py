# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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

import time
from abc import ABC, abstractmethod
from enum import Enum

_KEY_PERMISSIONS = "permissions"
_KEY_FORMAT_VERSION = "format_version"
_TARGET_SITE = "site"
_TARGET_SUBMITTER = "submitter"
_ANY_RIGHT = "*"


class FieldNames(str, Enum):

    USER_NAME = "User name"
    USER_ORG = "User org"
    USER_ROLE = "User role"
    EXP = "Expression"
    TARGET_TYPE = "Target type"
    TARGET_VALUE = "Target value"
    SITE_ORG = "Site org"
    ROLE_NAME = "Role name"
    RIGHT = "Right"
    CATEGORY_RIGHT = "Right for Category"


class Person(object):
    def __init__(self, name: str, org: str, role: str):
        self.name = _normalize_str(name, FieldNames.USER_NAME)
        self.org = _normalize_str(org, FieldNames.USER_ORG)
        self.role = _normalize_str(role, FieldNames.USER_ROLE)

    def __str__(self):
        name = self.name if self.name else "None"
        org = self.org if self.org else "None"
        role = self.role if self.role else "None"
        if (not name) and (not org) and (not role):
            return "None"
        else:
            return f"{name}:{org}:{role}"


class AuthzContext(object):
    def __init__(self, right: str, user: Person, submitter: Person = None):
        """Base class to contain context data for authorization."""
        if not isinstance(user, Person):
            raise ValueError(f"user needs to be of type Person but got {type(user)}")
        if submitter and not isinstance(submitter, Person):
            raise ValueError(f"submitter needs to be of type Person but got {type(submitter)}")
        self.right = right
        self.user = user
        self.submitter = submitter
        self.attrs = {}
        if submitter is None:
            self.submitter = Person("", "", "")

    def set_attr(self, key: str, value):
        pass

    def get_attr(self, key: str, default=None):
        pass


class ConditionEvaluator(ABC):
    @abstractmethod
    def evaluate(self, site_org: str, ctx: AuthzContext) -> bool:
        pass


class UserOrgEvaluator(ConditionEvaluator):
    def __init__(self, target):
        self.target = target

    def evaluate(self, site_org: str, ctx: AuthzContext):
        pass


class UserNameEvaluator(ConditionEvaluator):
    def __init__(self, target: str):
        self.target = target

    def evaluate(self, site_org: str, ctx: AuthzContext):
        pass


class TrueEvaluator(ConditionEvaluator):
    def evaluate(self, site_org: str, ctx: AuthzContext) -> bool:
        pass


class FalseEvaluator(ConditionEvaluator):
    def evaluate(self, site_org: str, ctx: AuthzContext) -> bool:
        pass


class _RoleRightConditions(object):
    def __init__(self):
        self.allowed_conditions = []
        self.blocked_conditions = []
        self.exp = None

    def _any_condition_matched(self, conds: [ConditionEvaluator], site_org: str, ctx: AuthzContext):
        # if any condition is met, return True
        # only when all conditions fail to match, return False
        pass

    def evaluate(self, site_org: str, ctx: AuthzContext):
        # first evaluate blocked list
        pass

    def _parse_one_expression(self, exp) -> str:
        pass

    def parse_expression(self, exp):
        """Parses the value expression into a list of condition(s).

        Args:
            exp: expression to be parsed

        Returns:
            An error string if value is invalid.
        """
        pass


class Policy(object):
    def __init__(self, config: dict, role_right_map: dict, roles: list, rights: list, role_rights: dict):
        self.config = config
        self.role_right_map = role_right_map
        self.roles = roles
        self.rights = rights
        self.roles.sort()
        self.rights.sort()
        self.role_rights = role_rights

    def get_rights(self):
        pass

    def get_roles(self):
        pass

    def _eval_for_role(self, role: str, site_org: str, ctx: AuthzContext):
        pass

    def evaluate(self, site_org: str, ctx: AuthzContext) -> (bool, str):
        """

        Args:
            site_org:
            ctx:

        Returns:
            A tuple of (result, error)
        """
        pass


def _normalize_str(s: str, field_name: FieldNames) -> str:
    pass


def _role_right_key(role_name: str, right_name: str):
    pass


def _add_role_right_conds(role, right, conds, rr_map: dict, rights, right_conds):
    pass


def parse_policy_config(config: dict, right_categories: dict):
    """Validates that an authorization policy configuration has the right syntax.

    Args:
        config: configuration dictionary to validate
        right_categories: a dict of right => category mapping

    Returns: a Policy object if no error, a string describing the error encountered

    """
    pass


class Authorizer(object):
    def __init__(self, site_org: str, right_categories: dict = None):
        """Base class containing the authorization policy."""
        self.site_org = _normalize_str(site_org, FieldNames.SITE_ORG)
        self.right_categories = right_categories
        self.policy = None
        self.last_load_time = None

    def get_policy(self) -> Policy:
        pass

    def authorize(self, ctx: AuthzContext) -> (bool, str):
        pass

    def evaluate(self, ctx: AuthzContext) -> (bool, str):
        pass

    def load_policy(self, policy_config: dict) -> str:
        pass


class AuthorizationService(object):

    the_authorizer = None

    @staticmethod
    def initialize(authorizer: Authorizer) -> (Authorizer, str):
        pass

    @staticmethod
    def get_authorizer():
        pass

    @staticmethod
    def authorize(ctx: AuthzContext):
        pass
