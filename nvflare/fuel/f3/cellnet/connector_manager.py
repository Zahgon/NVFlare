# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
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
import os
import time
from typing import Union

from nvflare.apis.fl_constant import ConnectionSecurity
from nvflare.fuel.common.excepts import ConfigError
from nvflare.fuel.f3.cellnet.defs import ConnectorRequirementKey
from nvflare.fuel.f3.cellnet.fqcn import FqcnInfo
from nvflare.fuel.f3.comm_config import CommConfigurator
from nvflare.fuel.f3.communicator import CommError, Communicator, Mode
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception, secure_format_traceback

_KEY_RESOURCES = "resources"
_KEY_INT = "internal"
_KEY_ADHOC = "adhoc"
_KEY_SCHEME = "scheme"
_KEY_HOST = "host"
_KEY_PORTS = "ports"


class _Defaults:

    ALLOW_ADHOC_CONNECTIONS = False
    SCHEME_FOR_INTERNAL_CONNECTIONS = "tcp"
    SCHEME_FOR_ADHOC_CONNECTIONS = "tcp"


class ConnectorData:
    def __init__(self, handle, connect_url: str, active: bool, params: dict):
        self.handle = handle
        self.connect_url = connect_url
        self.active = active
        self.params = params

    def get_connection_url(self):
        pass

    def get_connection_params(self):
        pass


class ConnectorManager:
    """
    Manages creation of connectors
    """

    def __init__(self, communicator: Communicator, secure: bool, comm_configurator: CommConfigurator):
        self._name = self.__class__.__name__
        self.logger = get_obj_logger(self)

        self.communicator = communicator
        self.secure = secure

        self.bb_conn_gen = comm_configurator.get_backbone_connection_generation(2)

        # set up default drivers
        self.int_scheme = comm_configurator.get_internal_connection_scheme(_Defaults.SCHEME_FOR_INTERNAL_CONNECTIONS)
        self.int_resources = {
            _KEY_HOST: "localhost",
        }
        self.adhoc_allowed = comm_configurator.allow_adhoc_connections(_Defaults.ALLOW_ADHOC_CONNECTIONS)
        self.adhoc_scheme = comm_configurator.get_adhoc_connection_scheme(_Defaults.SCHEME_FOR_ADHOC_CONNECTIONS)
        self.adhoc_resources = {}

        # load config if any
        comm_config = comm_configurator.get_config()
        if comm_config:
            int_conf = self._validate_conn_config(comm_config, _KEY_INT)
            if int_conf:
                self.int_scheme = int_conf.get(_KEY_SCHEME)
                self.int_resources = int_conf.get(_KEY_RESOURCES)

            adhoc_conf = self._validate_conn_config(comm_config, _KEY_ADHOC)
            if adhoc_conf:
                self.adhoc_scheme = adhoc_conf.get(_KEY_SCHEME)
                self.adhoc_resources = adhoc_conf.get(_KEY_RESOURCES)

        # default conn sec
        conn_sec = self.int_resources.get(DriverParams.CONNECTION_SECURITY)
        if not conn_sec:
            self.int_resources[DriverParams.CONNECTION_SECURITY] = ConnectionSecurity.CLEAR

        self.logger.debug(f"internal scheme={self.int_scheme}, resources={self.int_resources}")
        self.logger.debug(f"adhoc scheme={self.adhoc_scheme}, resources={self.adhoc_resources}")
        self.comm_config = comm_config

    def get_config_info(self):
        pass

    def should_connect_to_server(self, fqcn_info: FqcnInfo) -> bool:
        pass

    def is_adhoc_allowed(self, c1: FqcnInfo, c2: FqcnInfo) -> bool:
        """
        Is ad-hoc connection allowed between the two cells?

        Args:
            c1: FQCN info of cell one
            c2: FQCN info of cell two. c2 will offer listener if ad-hoc is allowed.

        Returns: whether ad-hoc connection is allowed between the two cells

        """
        pass

    @staticmethod
    def _validate_conn_config(config: dict, key: str) -> Union[None, dict]:
        pass

    def _get_connector(
        self, url: str, active: bool, internal: bool, adhoc: bool, secure: bool, conn_resources=None
    ) -> Union[None, ConnectorData]:
        pass

    def get_external_listener(self, url: str, adhoc: bool) -> Union[None, ConnectorData]:
        """
        Try to get an external listener.

        Args:
            url:
            adhoc:
        """
        pass

    def get_external_connector(self, url: str, adhoc: bool) -> Union[None, ConnectorData]:
        """
        Try to get an external listener.

        Args:
            url:
            adhoc:
        """
        pass

    def get_internal_listener(self) -> Union[None, ConnectorData]:
        """
        Try to get an internal listener.
        """
        pass

    def get_internal_connector(self, url: str, conn_resources=None) -> Union[None, ConnectorData]:
        """
        Try to get an internal listener.

        Args:
            url:
        """
        pass
