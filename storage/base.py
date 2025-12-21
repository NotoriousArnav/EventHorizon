# Event Horizon - Futuristic Event Management Platform
# Copyright (C) 2025-2026 Arnav Ghosh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Base storage interface for EventHorizon.

This module defines the abstract interface that all storage backends must implement.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseStorageBackend(ABC):
    """
    Abstract base class for storage backends.

    All storage implementations must inherit from this class and implement
    the required methods to ensure consistent behavior across providers.
    """

    @abstractmethod
    def save(self, name: str, content, max_length: Optional[int] = None) -> str:
        """
        Save a file to storage.

        Args:
            name: The name/path of the file
            content: File content (file-like object or bytes)
            max_length: Maximum length of the filename

        Returns:
            The actual name of the stored file (may differ from input name)
        """
        pass

    @abstractmethod
    def delete(self, name: str) -> None:
        """
        Delete a file from storage.

        Args:
            name: The name/path of the file to delete
        """
        pass

    @abstractmethod
    def exists(self, name: str) -> bool:
        """
        Check if a file exists in storage.

        Args:
            name: The name/path of the file

        Returns:
            True if file exists, False otherwise
        """
        pass

    @abstractmethod
    def url(self, name: str) -> str:
        """
        Get the URL for accessing a file.

        Args:
            name: The name/path of the file

        Returns:
            The URL to access the file
        """
        pass

    @abstractmethod
    def size(self, name: str) -> int:
        """
        Get the size of a file in bytes.

        Args:
            name: The name/path of the file

        Returns:
            Size in bytes
        """
        pass

    @abstractmethod
    def open(self, name: str, mode: str = "rb"):
        """
        Open a file from storage.

        Args:
            name: The name/path of the file
            mode: File open mode (default: 'rb')

        Returns:
            File-like object
        """
        pass

    def get_available_name(self, name: str, max_length: Optional[int] = None) -> str:
        """
        Get an available filename by appending numbers if necessary.

        Args:
            name: The desired filename
            max_length: Maximum length of the filename

        Returns:
            An available filename
        """
        # Default implementation - can be overridden by subclasses
        if max_length and len(name) > max_length:
            raise ValueError(f"Filename too long: {name}")
        return name
