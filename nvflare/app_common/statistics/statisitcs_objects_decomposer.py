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
from typing import Any, Type

from nvflare.app_common.abstract.statistics_spec import (
    Bin,
    BinRange,
    DataType,
    Feature,
    Histogram,
    HistogramType,
    StatisticConfig,
)
from nvflare.fuel.utils import fobs
from nvflare.fuel.utils.fobs.datum import DatumManager


class StatisticConfigDecomposer(fobs.Decomposer):
    def supported_type(self) -> Type[Any]:
        pass

    def decompose(self, statistic_config: StatisticConfig, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: list, manager: DatumManager = None) -> StatisticConfig:
        pass


class FeatureDecomposer(fobs.Decomposer):
    def supported_type(self) -> Type[Any]:
        pass

    def decompose(self, f: Feature, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: list, manager: DatumManager = None) -> Feature:
        pass


class BinDecomposer(fobs.Decomposer):
    def supported_type(self) -> Type[Any]:
        pass

    def decompose(self, b: Bin, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: list, manager: DatumManager = None) -> Bin:
        pass


class BinRangeDecomposer(fobs.Decomposer):
    def supported_type(self) -> Type[Any]:
        pass

    def decompose(self, b: BinRange, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: list, manager: DatumManager = None) -> BinRange:
        pass


class HistogramDecomposer(fobs.Decomposer):
    def supported_type(self) -> Type[Any]:
        pass

    def decompose(self, b: Histogram, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: list, manager: DatumManager = None) -> Histogram:
        pass


class HistogramTypeDecomposer(fobs.Decomposer):
    def supported_type(self) -> Type[HistogramType]:
        pass

    def decompose(self, target: HistogramType, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: Any, manager: DatumManager = None) -> HistogramType:
        pass


class DataTypeDecomposer(fobs.Decomposer):
    def supported_type(self) -> Type[DataType]:
        pass

    def decompose(self, target: DataType, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: Any, manager: DatumManager = None) -> DataType:
        pass


def fobs_registration():
    pass
