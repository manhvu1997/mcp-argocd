"""
Tool to create a new ArgoCD application.
"""
from typing import Any, Dict
from src.argocd_client import argocd_request, ArgoCDApiError

async def create_application(app_spec: Dict[str, Any]) -> Any:
    """
    Create a new ArgoCD application.
    Args:
        app_spec: The application specification as a dictionary.
    Returns:
        Application creation result or error information.
    """
    try:
        return await argocd_request("POST", "/api/v1/applications", json=app_spec)
    except ArgoCDApiError as e:
        return {"error": str(e), "status_code": getattr(e, "status_code", None), "response": getattr(e, "response", None)}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"} 