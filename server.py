"""
MCP server exposing ArgoCD tools.
"""
from mcp.server.fastmcp import FastMCP
from src.tools import (
    list_applications,
    create_application,
    delete_application,
    force_sync_application,
    list_event_applications,
    show_pod_logs,
    rollback_application,
    get_manifests_application,
    describe_application,
)
from typing import Any, Dict, Optional
import logging
import sys
import os
from dotenv import load_dotenv

# Configure logging for robust error and transport event tracking
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("mcp-argocd-server")

mcp = FastMCP("argocd")

@mcp.tool()
async def list_applications_tool() -> Any:
    """
    List all ArgoCD applications.
    """
    return await list_applications.list_applications()

@mcp.tool()
async def create_application_tool(app_spec: Dict[str, Any]) -> Any:
    """
    Create a new ArgoCD application.
    Args:
        app_spec: The application specification as a dictionary.
    """
    return await create_application.create_application(app_spec)

@mcp.tool()
async def delete_application_tool(app_name: str) -> Any:
    """
    Delete an ArgoCD application by name.
    Args:
        app_name: The name of the application to delete.
    """
    return await delete_application.delete_application(app_name)

@mcp.tool()
async def force_sync_application_tool(app_name: str) -> Any:
    """
    Force sync an ArgoCD application by name.
    Args:
        app_name: The name of the application to sync.
    """
    return await force_sync_application.force_sync_application(app_name)

@mcp.tool()
async def list_event_applications_tool(app_name: str) -> Any:
    """
    List events for an ArgoCD application by name.
    Args:
        app_name: The name of the application.
    """
    return await list_event_applications.list_event_applications(app_name)

@mcp.tool()
async def show_pod_logs_tool(app_name: str, pod_name: str, container_name: Optional[str] = None, tailLines: Optional[int] = None) -> Any:
    """
    Show pod logs for a pod in an ArgoCD application.
    Args:
        app_name: The name of the application.
        pod_name: The name of the pod.
        container_name: The name of the container (optional).
        tailLines: The number of lines to tail the logs (optional).
    """
    return await show_pod_logs.show_pod_logs(app_name, pod_name, container_name, tailLines)

@mcp.tool()
async def rollback_application_tool(app_name: str, revision: str) -> Any:
    """
    Rollback an ArgoCD application to a specific revision.
    Args:
        app_name: The name of the application.
        revision: The revision to rollback to.
    """
    return await rollback_application.rollback_application(app_name, revision)

@mcp.tool()
async def get_manifests_application_tool(app_name: str) -> Any:
    """
    Get manifests details of an ArgoCD application.
    Args:
        app_name: The name of the application.
    """
    return await get_manifests_application.get_manifests_application(app_name)

@mcp.tool()
async def describe_application_tool(app_name: str) -> Any:
    """
    Describe an ArgoCD application.
    """
    return await describe_application.describe_application(app_name)
if __name__ == "__main__":
    try:
        # Load environment variables from config/.env
        # load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../config/.env'))
        transport = os.getenv("MCP_TRANSPORT", "sse")
        logger.info(f"Starting MCP server with transport: {transport}")
        mcp.run(transport=transport)
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}", exc_info=True)
        sys.exit(1)