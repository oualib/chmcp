# Copyright 2025 Badr Ouali
# SPDX-License-Identifier: Apache-2.0

"""HTTP client for ClickHouse Cloud API interactions.

This module provides a centralized HTTP client for making requests to the
ClickHouse Cloud API with proper authentication, error handling, and response processing.
"""

import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException, Timeout

from .cloud_config import get_cloud_config

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CloudAPIResponse:
    """Represents a response from the ClickHouse Cloud API."""

    status: int
    request_id: Optional[str]
    result: Any
    raw_response: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class CloudAPIError:
    """Represents an error response from the ClickHouse Cloud API."""

    status: int
    error: str
    request_id: Optional[str] = None


class ClickHouseCloudClient:
    """HTTP client for ClickHouse Cloud API operations."""

    def __init__(self):
        """Initialize the cloud client."""
        self.config = get_cloud_config()
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create and configure a requests session.

        Returns:
            requests.Session: Configured session with authentication
        """
        session = requests.Session()
        session.auth = self.config.get_auth_tuple()
        session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "chmcp/0.1.0",
            }
        )

        # Add SSL configuration to handle certificate issues
        session.verify = False  # self.config.verify_ssl

        # Alternative: Add retry configuration
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        return session

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Union[CloudAPIResponse, CloudAPIError]:
        """Make a request to the ClickHouse Cloud API.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (e.g., '/v1/organizations')
            params: Query parameters
            data: Request body data

        Returns:
            CloudAPIResponse on success, CloudAPIError on failure
        """
        url = urljoin(self.config.api_url, endpoint)

        try:
            logger.info(f"Making {method} request to {endpoint}")

            response = self.session.request(
                method=method, url=url, params=params, json=data, timeout=self.config.timeout
            )

            return self._process_response(response)

        except Timeout:
            logger.error(f"Request to {endpoint} timed out after {self.config.timeout}s")
            return CloudAPIError(
                status=408, error=f"Request timed out after {self.config.timeout} seconds"
            )
        except RequestException as e:
            logger.error(f"Request to {endpoint} failed: {e}")
            return CloudAPIError(status=0, error=f"Request failed: {str(e)}")

    def _process_response(
        self, response: requests.Response
    ) -> Union[CloudAPIResponse, CloudAPIError]:
        """Process HTTP response and return appropriate result.

        Args:
            response: HTTP response object

        Returns:
            CloudAPIResponse on success, CloudAPIError on failure
        """
        try:
            response_data = response.json() if response.content else {}
        except json.JSONDecodeError:
            response_data = {"error": "Invalid JSON response"}

        request_id = response_data.get("requestId")

        if response.status_code >= 400:
            error_message = response_data.get("error", f"HTTP {response.status_code}")
            logger.warning(
                f"API request failed with status {response.status_code}: {error_message}"
            )

            return CloudAPIError(
                status=response.status_code, error=error_message, request_id=request_id
            )

        logger.info(f"API request successful with status {response.status_code}")

        return CloudAPIResponse(
            status=response.status_code,
            request_id=request_id,
            result=response_data.get("result"),
            raw_response=response_data,
        )

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Union[CloudAPIResponse, CloudAPIError]:
        """Make a GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            API response or error
        """
        return self.request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Union[CloudAPIResponse, CloudAPIError]:
        """Make a POST request.

        Args:
            endpoint: API endpoint
            data: Request body data

        Returns:
            API response or error
        """
        return self.request("POST", endpoint, data=data)

    def patch(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Union[CloudAPIResponse, CloudAPIError]:
        """Make a PATCH request.

        Args:
            endpoint: API endpoint
            data: Request body data

        Returns:
            API response or error
        """
        return self.request("PATCH", endpoint, data=data)

    def delete(self, endpoint: str) -> Union[CloudAPIResponse, CloudAPIError]:
        """Make a DELETE request.

        Args:
            endpoint: API endpoint

        Returns:
            API response or error
        """
        return self.request("DELETE", endpoint)


def create_cloud_client() -> ClickHouseCloudClient:
    """Create a new ClickHouse Cloud API client.

    Returns:
        ClickHouseCloudClient: Configured client instance
    """
    try:
        return ClickHouseCloudClient()
    except ValueError as e:
        logger.error(f"Failed to create cloud client due to missing configuration: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to create cloud client: {e}")
        raise
