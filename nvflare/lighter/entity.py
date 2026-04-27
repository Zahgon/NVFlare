# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
from typing import Any, List, Optional, Union

from nvflare.apis.utils.format_check import name_check

from .constants import DEFINED_PARTICIPANT_TYPES, DEFINED_ROLES, ConnSecurity, ParticipantType, PropKey


class ListeningHost:
    def __init__(self, scheme, host_names, default_host, port, conn_sec):
        self.scheme = scheme
        self.host_names = host_names
        self.default_host = default_host
        self.port = port
        self.conn_sec = conn_sec

    def __str__(self):
        scheme, host_names, default_host, port, conn_sec = (
            self.scheme,
            self.host_names,
            self.default_host,
            self.port,
            self.conn_sec,
        )
        return f"ListeningHost[{scheme=} {host_names=} {default_host=} {port=} {conn_sec=}]"


class ConnectTo:
    def __init__(self, name, host, port, conn_sec):
        self.name = name
        self.host = host
        self.port = port
        self.conn_sec = conn_sec

    def __str__(self):
        name, host, port, conn_sec = self.name, self.host, self.port, self.conn_sec
        return f"ConnectTo[{name=} {host=} {port=} {conn_sec=}]"


def _check_host_name(scope: str, prop_key: str, value):
    pass


def _check_host_names(scope: str, prop_key: str, value):
    pass


def _check_admin_role(scope: str, prop_key: str, value):
    pass


def parse_connect_to(value, scope=None, prop_key=None) -> ConnectTo:
    """Parse the "connect_to" property.

    Args:
        value: value to be parsed. It is either a str or a dict.
        scope: scope of the property
        prop_key: key of the property

    Returns: a ConnectTo object

    """
    pass


def _check_connect_to(scope: str, prop_key: str, value):
    pass


def _check_conn_security(scope: str, prop_key: str, value):
    pass


def parse_listening_host(value, scope=None, prop_key=None) -> ListeningHost:
    """Parse the "listening_host" property. It must be either str or a dict

    Args:
        value: value to be parsed
        scope: scope of the prop
        prop_key: key of the property

    Returns: a ListeningHost object
    """
    pass


def _check_listening_host(scope: str, prop_key: str, value):
    pass


# validator functions for common properties
# Validator function must follow this signature:
# func(scope: str, prop_key: str, value)
_PROP_VALIDATORS = {
    PropKey.HOST_NAMES: _check_host_names,
    PropKey.CONNECT_TO: _check_connect_to,
    PropKey.LISTENING_HOST: _check_listening_host,
    PropKey.DEFAULT_HOST: _check_host_name,
    PropKey.ROLE: _check_admin_role,
    PropKey.CONN_SECURITY: _check_conn_security,
}


class Entity:
    def __init__(self, scope: str, name: str, props: dict, parent=None):
        if not props:
            props = {}

        for k, v in props.items():
            validator = _PROP_VALIDATORS.get(k)
            if validator is not None:
                validator(scope, k, v)
        self.name = name
        self.props = props
        self.parent = parent

    def get_prop(self, key: str, default=None):
        pass

    def set_prop(self, key: str, value: Any):
        pass

    def get_prop_fb(self, key: str, fb_key=None, default=None):
        """Get property value with fallback.
        If I have the property, then return it.
        If not, I return the fallback property of my parent. If I don't have parent, return default.

        Args:
            key: key of the property
            fb_key: key of the fallback property.
            default: value to return if no one has the property

        Returns: property value

        """
        pass

    def __str__(self):
        return f"Entity[{self.name=}, {self.props=}, {self.parent=}]"

    def __repr__(self):
        return self.__str__()


class Participant(Entity):
    def __init__(self, type: str, name: str, org: str, props: Optional[dict] = None, project: Entity = None):
        """Class to represent a participant.

        Each participant communicates to other participant.  Therefore, each participant has its
        own name, type, organization it belongs to, rules and other information.

        Args:
            type (str): server, client, admin, relay or other string that builders can handle
            name (str): system-wide unique name
            org (str): system-wide unique organization
            props (dict): properties
            project: the project that the participant belongs to

        Raises:
            ValueError: if name or org is not compliant with characters or format specification.
        """
        Entity.__init__(self, f"{type}::{name}", name, props, parent=project)

        if type in DEFINED_PARTICIPANT_TYPES:
            err, reason = name_check(name, type)
            if err:
                raise ValueError(reason)
        else:
            err, reason = name_check(type, "simple_name")
            if err:
                raise ValueError(reason)
            print(f"Warning: participant type '{type}' of {name} is not a defined type {DEFINED_PARTICIPANT_TYPES}")

        err, reason = name_check(org, "org")
        if err:
            raise ValueError(reason)

        if type == ParticipantType.ADMIN:
            if not props:
                raise ValueError(f"missing role for admin '{name}'")

            role = props.get(PropKey.ROLE)
            if not role:
                raise ValueError(f"missing role for admin '{name}'")

            err, reason = name_check(role, "simple_name")
            if err:
                raise ValueError(f"bad role value '{role}' for admin '{name}': {reason}")

            if role not in DEFINED_ROLES:
                print(f"Warning: '{role}' of admin '{name}' is not a defined role {DEFINED_ROLES}")

        self.type = type
        self.org = org
        self.subject = name

    def get_default_host(self) -> str:
        """Get the default host name for accessing this participant (server).
        If the "default_host" attribute is explicitly specified, then it's the default host.
        If the "default_host" attribute is not explicitly specified, then use the "name" attribute.

        Returns: a host name

        """
        pass

    def get_listening_host(self) -> Optional[ListeningHost]:
        """Get listening host property of the participant

        Returns: a ListeningHost object, or None if the property is not defined.

        """
        pass

    def get_connect_to(self) -> Optional[ConnectTo]:
        """Get the connect_to property of the participant

        Returns: a ConnectTo object

        """
        pass


def _must_get(d: dict, key: str):
    """Must get property of the specified key from the dict

    Args:
        d: the dict that contains participant properties
        key: key of the property to get

    Returns: the value of the property. If the property does not exist, ValueError exception is raised.

    """
    pass


def participant_from_dict(participant_def: dict) -> Participant:
    """Create a Participant from a dict that contains participant property definitions.

    Args:
        participant_def: the dict that contains participant definition

    Returns: a Participant object

    """
    pass


class Project(Entity):
    def __init__(
        self,
        name: str,
        description: str,
        participants=None,
        props: Optional[dict] = None,
        serialized_root_cert=None,
        root_private_key=None,
    ):
        """A container class to hold information about this FL project.

        This class only holds information.  It does not drive the workflow.

        Args:
            name (str): the project name
            description (str): brief description on this name
            participants: if provided, list of participants of the project
            props: properties of the project
            serialized_root_cert: if provided, the root cert to be used for the project
            root_private_key: if provided, the root private key for signing certs of sites and admins

        Raises:
            ValueError: when participant criteria is violated
        """
        Entity.__init__(self, "project", name, props)

        if serialized_root_cert:
            if not root_private_key:
                raise ValueError("missing root_private_key while serialized_root_cert is provided")

        self.description = description
        self.serialized_root_cert = serialized_root_cert
        self.root_private_key = root_private_key
        self.server = None
        self._participants_by_types = {}  # participant type => list of participants
        self._all_names = {}  # name => participant

        if participants:
            if not isinstance(participants, list):
                raise ValueError(f"participants must be a list of Participant but got {type(participants)}")

            for p in participants:
                if not isinstance(p, Participant):
                    raise ValueError(f"bad item in participants: must be Participant but got {type(p)}")
                self.add_participant(p)

    def set_server(self, name: str, org: str, props: dict) -> Participant:
        """Set the server of the project.

        Args:
            name: name of the server.
            org: org of the server
            props: additional server properties.

        Returns: a Participant object for the server

        """
        pass

    def get_server(self) -> Optional[Participant]:
        """Get the server definition. Only one server is supported!

        Returns: server participant

        """
        pass

    def get_overseer(self) -> Optional[Participant]:
        """Get the overseer definition.

        Note: overseer is deprecated.

        Returns: None

        """
        pass

    def add_participant(self, participant: Participant) -> Participant:
        """Add a participant to the project.
        Before adding the participant, this method checks the following conditions:
        - All participants in the project must have unique names
        - Only one server is allowed in the project
        - Role must be specified for admin type of participant

        Args:
            participant: the participant to be added.

        Returns: the participant object added.

        """
        pass

    def add_client(self, name: str, org: str, props: dict) -> Participant:
        """Add a client to the project

        Args:
            name: name of the client
            org: org of the client
            props: additional properties of the client

        Returns: the Participant object of the client

        """
        pass

    def get_clients(self) -> List[Participant]:
        """Get all clients of the project

        Returns: a list of clients

        """
        pass

    def add_relay(self, name: str, org: str, props: dict) -> Participant:
        """Add a relay to the project

        Args:
            name: name of the relay
            org: org of the relay
            props: additional properties of the relay

        Returns: the relay Participant object

        """
        pass

    def get_relays(self) -> List[Participant]:
        """Get all relays of the project

        Returns: the list of relays of the project

        """
        pass

    def add_admin(self, name: str, org: str, props: dict) -> Participant:
        """Add an admin user to the project

        Args:
            name: name of the admin user.
            org: org of the admin user.
            props: properties of the user definition

        Returns: a Participant object of the admin user

        """
        pass

    def get_admins(self) -> List[Participant]:
        """Get the list of admin users

        Returns: list of admin users

        """
        pass

    def get_all_participants(self, types: Union[None, str, List[str]] = None):
        """Get all participants of the project of specified types.

        Args:
            types: types of the participants to be returned.

        Returns: all participants of the project of specified types.
            If 'types' is not specified (None), it returns all participants of the project;
            If 'types' is a str, it is treated as a single type and participants of this type is returned;
            If 'types' is a list of types, participants of these types are returned;

        """
        pass
