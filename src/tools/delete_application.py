"""
Tool to delete an ArgoCD application by name.
"""
from typing import Any
from src.argocd_client import argocd_request, ArgoCDApiError

async def delete_application(app_name: str) -> Any:
    """
    Delete an ArgoCD application by name.
    Args:
        app_name: The name of the application to delete.
    Returns:
        Deletion result or error information.
    """
    try:
        return await argocd_request("DELETE", f"/api/v1/applications/{app_name}")
    except ArgoCDApiError as e:
        return {"error": str(e), "status_code": getattr(e, "status_code", None), "response": getattr(e, "response", None)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"} 