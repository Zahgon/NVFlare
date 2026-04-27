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

import io
import os
from pathlib import Path
from zipfile import ZipFile


def normpath_for_zip(path):
    """Normalizes the path for zip file.

    Args:
        path (str): the path to be normalized
    """
    pass


def remove_leading_dotdot(path: str) -> str:
    pass


def split_path(path: str) -> (str, str):
    """Splits a path into a pair of head and tail.

    It removes trailing `os.path.sep` and call `os.path.split`

    Args:
        path: Path to split

    Returns:
        A tuple of `(head, tail)`
    """
    pass


def get_all_file_paths(directory):
    """Gets all file paths in the directory.

    Args:
        directory: directory to get all paths for

    Returns:
        A list of paths of all the files in the provided directory
    """
    pass


def _zip_directory(root_dir: str, folder_name: str, output_file):
    """Creates a zip archive file for the specified directory.

    Args:
        root_dir: root path that contains the folder to be zipped
        folder_name: path to the folder to be zipped, relative to root_dir
        output_file: file to write to
    """
    pass


def zip_directory_to_bytes(root_dir: str, folder_name: str) -> bytes:
    """Compresses a directory and return the bytes value of it.

    Args:
        root_dir: root path that contains the folder to be zipped
        folder_name: path to the folder to be zipped, relative to root_dir
    """
    pass


def zip_directory_to_file(root_dir: str, folder_name: str, output_file):
    """Compresses a directory and return the bytes value of it.

    Args:
        root_dir: root path that contains the folder to be zipped
        folder_name: path to the folder to be zipped, relative to root_dir
        output_file: path of the output file
    """
    pass


def ls_zip_from_bytes(zip_data: bytes):
    """Returns info of a zip.

    Args:
        zip_data: the input zip data
    """
    pass


def unzip_single_file_from_bytes(zip_data: bytes, output_dir_name: str, file_path: str):
    """Decompresses a zip and extracts single specified file to the specified output directory.

    Args:
        zip_data: the input zip data
        output_dir_name: the output directory for extracted content
        file_path: file path to file to unzip
    """
    pass


def unzip_all_from_bytes(zip_data: bytes, output_dir_name: str):
    """Decompresses a zip and extracts all files to the specified output directory.

    Args:
        zip_data: the input zip data
        output_dir_name: the output directory for extracted content
    """
    pass


def unzip_all_from_file(zip_file_path: str, output_dir_name: str):
    pass
