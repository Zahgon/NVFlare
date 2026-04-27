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

"""
This tool is for testing only. Do not use it for production purpose.
This tool automatically provisions a project with relay and client hierarchy based on user provided parameters.
"""

import argparse
import json
import os.path
import shutil

import nvflare.lighter.utils as utils
from nvflare.lighter.ctx import ProvisionContext
from nvflare.lighter.entity import Participant, ParticipantType, Project
from nvflare.lighter.impl.cert import CertBuilder
from nvflare.lighter.impl.edge import EdgeBuilder
from nvflare.lighter.impl.signature import SignatureBuilder
from nvflare.lighter.impl.static_file import StaticFileBuilder
from nvflare.lighter.impl.workspace import WorkspaceBuilder
from nvflare.lighter.provisioner import Provisioner
from nvflare.lighter.spec import Builder, Packager

PROV_KEY_ANALYZE = "analyze"
PROV_KEY_LCP_ONLY = "lcp_only"
PROV_KEY_ROOT_DIR = "root_dir"
PROV_KEY_PROJ_NAME = "project_name"
PROV_KEY_DEPTH = "depth"
PROV_KEY_WIDTH = "width"
PROV_KEY_MAX_SITES = "max_sites"
PROV_KEY_CLIENTS = "clients"
PROV_KEY_RP_PORT = "rp"


def _new_participant(name: str, ptype: str, props: dict) -> Participant:
    pass


def _make_client_name(relay_name: str) -> str:
    pass


class Stats:
    num_relays = 0
    num_leaf_relays = 0
    num_non_leaf_relays = 0

    num_clients = 0
    num_leaf_clients = 0
    num_non_leaf_clients = 0


class PortManager:
    last_port_number = 9000

    @classmethod
    def get_port(cls):
        pass


class _Node:
    def __init__(self):
        self.name = None
        self.client_name = None
        self.parent = None
        self.children = []
        self.port = PortManager.get_port()


LCP_MAP_BASENAME = "lcp_map.json"
LOCAL_HOST = "localhost"
CA_CERT_NAME = "rootCA.pem"
SIMULATION_CONFIG = "simulation_config.json"
RUN_SIMULATOR = "python -m nvflare.edge.simulation.run_device_simulator"


class _Packager(Packager):

    def __init__(self, lcp_map, rp_port):
        self.lcp_map = lcp_map
        self.rp_port = rp_port

    def package(self, project: Project, ctx: ProvisionContext):
        pass


def _build_tree(
    lcp_only: bool,
    depth: int,
    width: int,
    max_depth: int,
    parent: _Node,
    num_clients: int,
    project: Project,
    lcp_map: dict,
):
    """Build relay hierarchy and client hierarchy, recursively.

    Relays are organized hierarchically. Attach a client to each relay. Such clients are non-leaf clients (a.k.a
    aggregation clients). In client hierarchy, the client attached to a relay is the child of the client attached to
    the relay's parent relay. If the relay doesn't have a parent relay, then the client won't have a parent client.

    Create num_clients leaf clients for each leaf relay.

    Stats are collected during the building process.

    Args:
        lcp_only: only generate leaf CPs
        depth: current depth of the tree being built
        width: how many child nodes for each non-leaf node
        max_depth: how deep the relay tree is
        parent: the parent relay node
        num_clients: number of clients to create for each leaf node
        project: the project to add the sites to

    Returns: None

    """
    pass


def hierachical_provision(params: dict, project: Project, builders: list[Builder], admins):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
