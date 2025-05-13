"""
Tool to rollback an ArgoCD application to a specific revision.
"""
from typing import Any
from src.argocd_client import argocd_request, ArgoCDApiError

async def rollback_application(app_name: str, revision: str) -> Any:
    """
    Rollback an ArgoCD application to a specific revision.
    Args:
        app_name: The name of the application.
        revision: The revision to rollback to.
    Returns:
        Rollback result or error information.
    """
    data = {"id": app_name, "revision": revision}
    try:
        return await argocd_request("POST", f"/api/v1/applications/{app_name}/rollback", json=data)
    except ArgoCDApiError as e:
        return {"error": str(e), "status_code": getattr(e, "status_code", None), "response": getattr(e, "response", None)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"} 