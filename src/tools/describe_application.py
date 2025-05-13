"""
Tool to describe an ArgoCD application.
"""
from src.argocd_client import argocd_request, ArgoCDApiError
from typing import Any

async def describe_application(app_name: str) -> Any:
    """
    Describe an ArgoCD application.
    """
    try:
        return await argocd_request("GET", f"/api/v1/applications/{app_name}")
    except ArgoCDApiError as e:
        return {"error": str(e), "status_code": getattr(e, "status_code", None), "response": getattr(e, "response", None)}