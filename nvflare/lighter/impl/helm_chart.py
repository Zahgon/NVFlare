# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
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

import logging
import os
import shutil

import yaml

import nvflare.lighter as prov
from nvflare.lighter.constants import CommConfigArg, ConnSecurity, CtxKey, PropKey, ProvFileName
from nvflare.lighter.entity import Participant
from nvflare.lighter.spec import Builder, Project, ProvisionContext
from nvflare.lighter.utils import update_storage_locations

_HELM_TEMPLATES_DIR = os.path.join(os.path.dirname(prov.__file__), "templates", "helm")
logger = logging.getLogger(__name__)


def _split_image(docker_image: str):
    """Split ``'repo:tag'`` into ``(repo, tag)``.  Returns ``('repo', '')`` when no tag."""
    pass


def _helm_src(role: str, filename: str) -> str:
    """Return the absolute path of a Helm template file shipped with this package."""
    pass


class HelmChartBuilder(Builder):
    def __init__(
        self,
        docker_image: str,
        parent_port: int = 8102,
        workspace_pvc: str = "nvflws",
        workspace_mount_path: str = "/var/tmp/nvflare/workspace",
    ):
        """Build Helm charts for the FL server and all FL clients.

        Both the server chart and client charts follow the same construction
        pattern: ``Chart.yaml`` and ``values.yaml`` are built from Python dicts,
        and Kubernetes manifests are copied from package template files.

        **Server chart** — written to ``<wip>/<server-name>/helm_chart/``.  Uses a
        Kubernetes Deployment backed by PersistentVolumeClaims.  A tcp-services
        ConfigMap instructs the nginx ingress controller to open ``fedLearnPort``
        for raw TCP passthrough to the ``nvflare-server`` Service on the same port.

        **Client charts** — one chart per client, written to
        ``<wip>/<client-name>/helm_chart/``.  Uses a Kubernetes Pod
        backed by PersistentVolumeClaims.  The ``uid=`` argument that identifies
        the client to the FL server is rendered via ``{{ .Values.name }}`` in
        the pod template so a single ``--set name=<site>`` override is
        sufficient to re-target the chart.

        ``COMM_CONFIG_ARGS`` on each client participant is updated with
        ``host=client.name`` and ``port=parent_port`` (when pre-seeded by
        ``StaticFileBuilder``) so that ``comm_config.json`` uses the Kubernetes
        Service DNS name and the matching port.

        Args:
            docker_image: container image used for all participants, e.g.
                ``myregistry/nvflare:2.7.0``.
            parent_port: port job pods use to talk back to the client process
                (default 8102).  Exposed as ``containerPort`` in the Pod and
                as ``port``/``targetPort`` in the client Service.
            workspace_pvc: PVC claim name for the runtime workspace volume.
            workspace_mount_path: in-container mount path for the workspace PVC.
        """
        self.docker_image = docker_image
        self.parent_port = parent_port
        self.workspace_pvc = workspace_pvc
        self.workspace_mount_path = workspace_mount_path

    # ------------------------------------------------------------------
    # Builder lifecycle
    # ------------------------------------------------------------------

    def build(self, project: Project, ctx: ProvisionContext):
        """Generate the server Helm chart and one chart per client."""
        pass

    # ------------------------------------------------------------------
    # Server chart
    # ------------------------------------------------------------------

    def _build_server_chart(self, project: Project, ctx: ProvisionContext):
        pass

    def _write_server_chart_yaml(self, chart_dir: str, server: Participant):
        pass

    def _write_server_values_yaml(self, chart_dir: str, server: Participant, fed_learn_port: int, admin_port: int):
        pass

    def _write_server_template_files(self, templates_dir: str):
        pass

    # ------------------------------------------------------------------
    # Client charts
    # ------------------------------------------------------------------

    def _build_client_charts(self, project: Project, ctx: ProvisionContext):
        pass

    def _build_one_client_chart(self, client: Participant, ctx: ProvisionContext):
        pass

    def _write_client_chart_yaml(self, chart_dir: str, client: Participant):
        pass

    def _write_client_values_yaml(self, chart_dir: str, client: Participant):
        pass

    def _write_client_template_files(self, templates_dir: str):
        pass

    def _relocate_storage_to_workspace_pvc(self, ctx: ProvisionContext, participant: Participant):
        """Rewrite server resources so job and snapshot state live on the workspace PVC."""
        pass
