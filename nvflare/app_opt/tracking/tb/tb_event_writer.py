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

import io
import os
import time
from typing import Optional

import numpy as np
from tensorboard.compat.proto.event_pb2 import Event
from tensorboard.compat.proto.summary_pb2 import Summary
from tensorboard.plugins.text.summary_v2 import text_pb
from tensorboard.summary.writer.event_file_writer import EventFileWriter


def _create_scalar_summary(tag: str, value: float) -> Summary:
    pass


def _convert_image_to_hwc(value) -> np.ndarray:
    """Normalize HW/HWC/CHW image inputs to HWC uint8 for TensorBoard encoding.

    Float inputs are treated like TensorBoard image helpers typically do: values are
    expected in [0, 1] and scaled up to [0, 255] before PNG encoding. Callers with
    float images already expressed in [0, 255] should convert to uint8 first.
    """
    pass


def _create_image_summary(tag: str, value) -> Summary:
    pass


class TensorBoardEventWriter:
    """Framework-neutral TensorBoard writer backed by tensorboard's EventFileWriter.

    The standalone tensorboard package exposes the low-level event-file writer, but
    not a high-level SummaryWriter that avoids importing PyTorch or TensorFlow.
    This adapter preserves the TensorBoard-like methods used by TBAnalyticsReceiver
    while keeping the dependency surface limited to tensorboard.

    When ``global_step`` is omitted, the event step is left unset and TensorBoard
    treats it as step ``0``. This matches PyTorch's SummaryWriter behavior, so
    callers should provide explicit steps for time-series plots.
    """

    def __init__(self, log_dir: str):
        self.log_dir = log_dir
        self.writer = EventFileWriter(log_dir)
        self.scalar_writers = {}

    def add_scalar(self, tag: str, scalar_value: float, global_step: Optional[int] = None):
        pass

    def add_text(self, tag: str, text_string: str, global_step: Optional[int] = None):
        pass

    def add_image(self, tag: str, img_tensor, global_step: Optional[int] = None):
        pass

    def add_scalars(self, main_tag: str, tag_scalar_dict: dict, global_step: Optional[int] = None):
        pass

    def flush(self):
        pass

    def close(self):
        pass

    @staticmethod
    def _add_summary(writer: EventFileWriter, summary: Summary, global_step: Optional[int] = None):
        pass
