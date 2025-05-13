"""
Tool to show pod logs for a pod in an ArgoCD application.
"""
from typing import Any, Optional
from src.argocd_client import argocd_request, ArgoCDApiError

async def show_pod_logs(app_name: str, pod_name: str, container_name: Optional[str] = None, tailLines: Optional[int] = None) -> Any:
    """
    Show pod logs for a pod in an ArgoCD application.
    Args:
        app_name: The name of the application.
        pod_name: The name of the pod.
        container_name: The name of the container (optional).
        tailLines: The number of lines to tail the logs (optional).
    Returns:
        Pod logs or error information.
    """
    params = {}
    if container_name:
        params["container"] = container_name
    if tailLines:
        params["tailLines"] = tailLines
    try:
        return await argocd_request("GET", f"/api/v1/applications/{app_name}/pods/{pod_name}/logs", params=params)
    except ArgoCDApiError as e:
        return {"error": str(e), "status_code": getattr(e, "status_code", None), "response": getattr(e, "response", None)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"} 