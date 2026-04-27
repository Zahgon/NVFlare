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

from typing import Dict

from nvflare.fuel.utils.import_utils import optional_import


def convert_data(feature_metrics) -> dict:
    pass


class Visualization:
    def import_modules(self):
        pass

    def show_stats(self, data, white_list_features=None):
        pass

    def show_histograms(self, data, display_format="sample_count", white_list_features=None, plot_type="both"):
        pass

    def show_dataframe_plots(self, feature_dfs, plot_type="both"):
        pass

    def get_histogram_dataframes(self, data, display_format="sample_count", white_list_features=None) -> Dict:
        pass

    def _prepare_histogram_data(self, data, display_format="sample_count", white_list_features=None):
        pass

    def sum_counts_in_histogram(self, hist):
        pass

    def _get_target_features(self, all_features, white_list_features=None):
        pass
