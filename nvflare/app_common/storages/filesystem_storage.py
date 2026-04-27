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

import ast
import json
import logging
import os
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import List, Tuple

from nvflare.apis.storage import DATA, META, StorageException, StorageSpec
from nvflare.apis.utils.format_check import validate_class_methods_args
from nvflare.fuel.utils.zip_utils import zip_directory_to_file
from nvflare.security.logging import secure_format_exception

log = logging.getLogger(__name__)


def _write(path: str, content, mv_file=True):
    """Create a file at the specified 'path' with the specified 'content'.

    Args:
        path: the path of the file to be created
        content: content for the file to be created. It could be either bytes, or path (str) to the source file that
            contains the content.
        mv_file: whether the destination file should be created simply by moving the source file. This is applicable
            only when the 'content' is the path of the source file. If mv_file is False, the destination is created
            by copying from the source file, and the source file will remain intact; If mv_file is True, the
            destination file is created by "move" the source file, and the original source file will no longer exist.

    Returns:

    """
    pass


def _write_multi(output_zip_file_name: str, content: List[str]):
    pass


def _read(path: str) -> bytes:
    pass


def _object_exists(uri: str):
    """Checks whether an object exists at specified directory."""
    pass


def _encode_meta(meta: dict) -> bytes:
    pass


def _decode_meta(data: bytes) -> dict:
    pass


@validate_class_methods_args
class FilesystemStorage(StorageSpec):
    def __init__(self, root_dir=os.path.abspath(os.sep), uri_root="/"):
        """Init FileSystemStorage.

        Uses local filesystem to persist objects, with absolute paths as object URIs.

        Args:
            root_dir: the absolute path on the filesystem to store things
            uri_root: serving as the root of the storage. All URIs are rooted at this uri_root.
        """
        if not os.path.isabs(root_dir):
            raise ValueError(f"root_dir {root_dir} must be an absolute path.")
        if os.path.exists(root_dir) and not os.path.isdir(root_dir):
            raise ValueError(f"root_dir {root_dir} exists but is not a directory.")
        if not os.path.exists(root_dir):
            os.makedirs(root_dir, exist_ok=False)
        self.root_dir = root_dir
        self.uri_root = uri_root

    def _object_path(self, uri: str):
        pass

    def create_object(self, uri: str, data, meta: dict, overwrite_existing: bool = False):
        """Creates an object.

        Args:
            uri: URI of the object
            data: content of the object; bytes or file name that contains data
            meta: meta of the object
            overwrite_existing: whether to overwrite the object if already exists

        Raises:
            TypeError: if invalid argument types
            StorageException:
                - if error creating the object
                - if object already exists and overwrite_existing is False
                - if object will be at a non-empty directory
            IOError: if error writing the object

        """
        pass

    def clone_object(self, from_uri: str, to_uri: str, meta: dict, overwrite_existing: bool = False):
        pass

    def update_object(self, uri: str, data, component_name: str = DATA):
        """Update the object

        Args:
            uri: URI of the object
            data: content data of the component
            component_name: component name

        Raises StorageException when the object does not exit.

        """
        pass

    def update_meta(self, uri: str, meta: dict, replace: bool):
        """Updates the meta of the specified object.

        Args:
            uri: URI of the object
            meta: value of new meta
            replace: whether to replace the current meta completely or partial update

        Raises:
            TypeError: if invalid argument types
            StorageException: if object does not exist
            IOError: if error writing the object

        """
        pass

    def list_objects(self, path: str, without_tag=None) -> List[str]:
        """List all objects in the specified path.

        Args:
            path: the path uri to the objects
            without_tag: if set, skip the objects with this specified tag

        Returns:
            list of URIs of objects

        Raises:
            TypeError: if invalid argument types
            StorageException: if path does not exist or is not a valid directory.

        """
        pass

    def get_meta(self, uri: str) -> dict:
        """Gets meta of the specified object.

        Args:
            uri: URI of the object

        Returns:
            meta of the object.

        Raises:
            TypeError: if invalid argument types
            StorageException: if object does not exist

        """
        pass

    def list_components_of_object(self, uri: str) -> List[str]:
        """Gets all components of the specified object.

        Args:
            uri: URI of the object

        Returns:
            list of component names

        Raises:
            TypeError: if invalid argument types
            StorageException: if object does not exist

        """
        pass

    def get_data(self, uri: str, component_name: str = DATA) -> bytes:
        """Gets data of the specified object.

        Args:
            uri: URI of the object
            component_name: storage component name

        Returns:
            data of the object.

        Raises:
            TypeError: if invalid argument types
            StorageException: if object does not exist

        """
        pass

    def get_data_for_download(self, uri: str, component_name: str = DATA, download_file: str = None):
        pass

    def get_detail(self, uri: str) -> Tuple[dict, bytes]:
        """Gets both data and meta of the specified object.

        Args:
            uri: URI of the object

        Returns:
            meta and data of the object.

        Raises:
            TypeError: if invalid argument types
            StorageException: if object does not exist

        """
        pass

    def delete_object(self, uri: str):
        """Deletes the specified object.

        Args:
            uri: URI of the object

        Raises:
            TypeError: if invalid argument types
            StorageException: if object does not exist

        """
        pass

    def tag_object(self, uri: str, tag: str, data=None):
        pass
