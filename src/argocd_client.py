"""
ArgoCD API client for authentication and application management.
"""
import os
from typing import Any, Dict, Optional
import httpx
from dotenv import load_dotenv
import logging
import sys
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("mcp-argocd-server")

class ArgoCDApiError(Exception):
    """
    Custom exception for ArgoCD API errors, providing rich error context.
    """
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Any] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

# Load environment variables from config/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../config/.env'))

ARGOCD_API_URL = os.getenv("ARGOCD_API_URL")
ARGOCD_USERNAME = os.getenv("ARGOCD_USERNAME")
ARGOCD_PASSWORD = os.getenv("ARGOCD_PASSWORD")
ARGOCD_TOKEN = os.getenv("ARGOCD_TOKEN")
async def get_token() -> str:
    """
    Obtain a short-lived ArgoCD API token for authentication.
    Raises:
        ArgoCDApiError: If authentication fails or the API returns an error.
    """
    url = f"{ARGOCD_API_URL}/api/v1/session"
    headers = {"Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json={"username": ARGOCD_USERNAME, "password": ARGOCD_PASSWORD}, timeout=10.0)
            response.raise_for_status()
            return response.json()["token"]
    except httpx.HTTPStatusError as e:
        raise ArgoCDApiError(f"Failed to get ArgoCD token: {e.response.text}", status_code=e.response.status_code, response=e.response.text) from e
    except Exception as e:
        raise ArgoCDApiError(f"Unexpected error during token retrieval: {str(e)}") from e

async def argocd_request(
    method: str,
    path: str,
    *,
    json: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Make an authenticated request to the ArgoCD API.
    Raises:
        ArgoCDApiError: If the API call fails or returns an error.
    """
    try:
        # token = await get_token()
        token = ARGOCD_TOKEN
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"{ARGOCD_API_URL}{path}"
        logger.info(f"Making ArgoCD API request to: {url} and token: {token}")
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=headers, json=json, params=params, timeout=30.0)
            response.raise_for_status()
            logger.info(f"ArgoCD API response: {response.text}")
            return response.text
    except httpx.HTTPStatusError as e:
        raise ArgoCDApiError(f"ArgoCD API request failed: {e.response.text}", status_code=e.response.status_code, response=e.response.text) from e
    except Exception as e:
        raise ArgoCDApiError(f"Unexpected error during ArgoCD API request: {str(e)}") from e 