"""
Tool to list events for an ArgoCD application by name.
"""
from typing import Any
from src.argocd_client import argocd_request, ArgoCDApiError

async def list_event_applications(app_name: str) -> Any:
    """
    List events for an ArgoCD application by name.
    Args:
        app_name: The name of the application.
    Returns:
        List of events or error information.
    """
    try:
        return await argocd_request("GET", f"/api/v1/applications/{app_name}/events")
    except ArgoCDApiError as e:
        return {"error": str(e), "status_code": getattr(e, "status_code", None), "response": getattr(e, "response", None)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"} 