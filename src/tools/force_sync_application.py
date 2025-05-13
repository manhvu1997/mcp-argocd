"""
Tool to force sync an ArgoCD application by name.
"""
from typing import Any
from src.argocd_client import argocd_request, ArgoCDApiError

async def force_sync_application(app_name: str) -> Any:
    """
    Force sync an ArgoCD application by name.
    Args:
        app_name: The name of the application to sync.
    Returns:
        Sync result or error information.
    """
    try:
        return await argocd_request("POST", f"/api/v1/applications/{app_name}/sync")
    except ArgoCDApiError as e:
        return {"error": str(e), "status_code": getattr(e, "status_code", None), "response": getattr(e, "response", None)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"} 