"""
Tool to list ArgoCD applications.
"""
from typing import Any
from src.argocd_client import argocd_request, ArgoCDApiError

async def list_applications() -> Any:
    """
    List all ArgoCD applications.
    Returns:
        List of applications or error information.
    """
    try:
        return await argocd_request("GET", "/api/v1/applications")
    except ArgoCDApiError as e:
        return {"error": str(e), "status_code": getattr(e, "status_code", None), "response": getattr(e, "response", None)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"} 