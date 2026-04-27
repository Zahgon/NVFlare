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

import json
import os
import shutil

from nvflare.lighter import utils
from nvflare.lighter.constants import (
    CommConfigArg,
    ConnSecurity,
    CtxKey,
    ParticipantType,
    PropKey,
    ProvFileName,
    ProvisionMode,
    TemplateSectionKey,
)
from nvflare.lighter.entity import Participant
from nvflare.lighter.spec import Builder, Project, ProvisionContext


class StaticFileBuilder(Builder):
    def __init__(
        self,
        config_folder="",
        scheme="http",
        app_validator="",
        download_job_url="",
        docker_image="",
        **kwargs,
    ):
        """Build all static files from template.

        Uses the information from project.yml through project to go through the participants and write the contents of
        each file with the template, and replacing with the appropriate values from project.yml.

        Usually, two main categories of files are created in all FL participants, static and dynamic. Static files
        have similar contents among different participants, with small differences.  For example, the differences in
        sub_start.sh are client name and python module.  Those are basically static files.  This builder uses template
        file and string replacement to generate those static files for each participant.

        Args:
            config_folder: usually "config"
            app_validator: optional path to an app validator to verify that uploaded app has the expected structure
            docker_image: when docker_image is set to a docker image name, docker.sh will be generated on
            server/client/admin
        """
        if not isinstance(scheme, str):
            raise ValueError(f"invalid scheme: must be str but got {type(scheme)}")
        scheme = scheme.lower().strip()
        if not scheme:
            raise ValueError("scheme is not specified")

        builtin_schemes = ["grpc", "tcp", "http"]
        if scheme not in builtin_schemes:
            # we only issue warning since it could be a custom scheme
            print(f"WARNING: {scheme} is not a builtin scheme {builtin_schemes}")
        self.config_folder = config_folder
        self.scheme = scheme
        self.docker_image = docker_image
        self.download_job_url = download_job_url
        self.app_validator = app_validator
        self.aio_schemes = {
            "tcp": "atcp",
            "grpc": "agrpc",
            "http": "http",
        }

    @staticmethod
    def _build_conn_properties(site: Participant, ctx: ProvisionContext):
        pass

    def _determine_scheme(self, participant: Participant, scheme=None) -> str:
        pass

    def _build_server(self, server: Participant, ctx: ProvisionContext):
        pass

    def _build_comm_config_for_internal_listener(self, participant: Participant):
        """Build template args for comm_config, which will be used to create internal listener

        Args:
            participant:the participant that will create internal listener

        Returns: None

        Note: we only build template args but do not build the comm_config.json here. This is because
        comm_config.json contains multiple sections that are built in different places. The creation of
        comm_config.json happens during "finalize" of this builder, which will apply all template args
        to the "comm_config" template.

        """
        pass

    def _build_client(self, client: Participant, ctx: ProvisionContext):
        pass

    def _modify_system_log_streamer(self, section: str, client: Participant) -> str:
        """Modify the local resources section and remove the "system_log_streamer" component if necessary.
        By default, the "system_log_streamer" component is included in local resources.
        However, if the project does not allow errors to be sent, then this component must be removed.

        Args:
            section: the local resources section generated from template
            client: the client being provisioned

        Returns: modified section content

        """
        pass

    @staticmethod
    def _check_host_name_against_server(host_name: str, server: Participant) -> str:
        pass

    @staticmethod
    def _validate_host_name_against_listener(
        host_name: str, listener_name: str, listener_default_host: str, listener_available_host_names: list
    ) -> str:
        """Validate specified host_name against default host and available host names of the listener.
        This is to make sure that host_name used by a connector is valid.

        Args:
            host_name: the host name to be validated
            listener_name: name of the listener
            listener_default_host: the default host of the listener
            listener_available_host_names: other available host names of the listener

        Returns: error message if any

        """
        pass

    def _determine_conn_target(self, participant, ctx: ProvisionContext):
        pass

    def _build_admin(self, admin: Participant, ctx: ProvisionContext):
        pass

    def prepare_admin_config(self, admin: Participant, ctx: ProvisionContext):
        pass

    def _build_relay(self, relay: Participant, ctx: ProvisionContext):
        pass

    def build(self, project: Project, ctx: ProvisionContext):
        pass

    @staticmethod
    def _determine_relay_hierarchy(project: Project, ctx: ProvisionContext):
        """Relays are organized hierarchically. Relay hierarchy must be determined before we can generate
        their FQCNs properly. This method determines relay hierarchy based on the connect_to properties
        in all specified relays. Circular refs are not allowed. FQCN for each relay is determined.

        Args:
            project: the project being provisioned
            ctx: the ProvisionContext object

        Returns:

        """
        pass

    @staticmethod
    def _determine_client_hierarchy(project: Project, ctx: ProvisionContext):
        """Client hierarchy is used to enable hierarchical FL algorithms.
        This method determines client hierarchy based on the "parent" property.
        FQSN (fully qualified site name) defines the position of the client in the hierarchy.
        FQSN is computed for each client.

        Args:
            project: the project being provisioned
            ctx: a ProvisionContext object

        Returns:

        """
        pass

    def initialize(self, project: Project, ctx: ProvisionContext):
        pass

    def finalize(self, project: Project, ctx: ProvisionContext):
        pass

    @staticmethod
    def _append(content: str, participant: Participant) -> str:
        pass

    def _create_start_all(self, project: Project, ctx: ProvisionContext):
        """Create the start_all.sh script to be used for starting all sites (server, relays and clients).
        This is a convenience script and not part of any site's startup kit.

        Args:
            project: project being provisioned
            ctx: a ProvisionContext object

        Returns: None

        """
        pass


def _remove_undefined_port(section: str) -> str:
    """This is the callback for checking and removing undefined port number for comm_config.
    Since the templating system does not allow conditional args, each arg must have a value when
    generating the section from the template. We used port 0 to represent undefined port number.
    We must remove undefined port number from comm_config; otherwise Flare wouldn't work in run time.

    Args:
        section: the section data to be checked

    Returns: modified section data

    """
    pass


def check_parent(c: Participant, path: list):
    pass
