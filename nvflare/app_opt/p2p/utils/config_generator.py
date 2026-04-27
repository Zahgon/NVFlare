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
import networkx as nx
import numpy as np

from nvflare.app_opt.p2p.types import Neighbor, Network, Node
from nvflare.app_opt.p2p.utils.topology import doubly_stochastic_adjacency


def generate_random_network(
    num_clients: int,
    seed: int = 42,
    connection_probability: float = 0.3,
) -> Network:
    """Generate a random configuration for the given number of clients.
    The configuration includes the number of iterations, the network topology,
    and the initial values for each node.

    Args:
        num_clients (int): The number of clients in the network.

    Returns:
        BaseConfig: The generated configuration.
        np.ndarray: The weighted adjacency matrix of the network.
    """
    pass
