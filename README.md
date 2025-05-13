# MCP ArgoCD Server

This project implements an MCP server that integrates with the ArgoCD API, exposing application management actions as MCP tools. It supports listing, creating, deleting, syncing, rolling back applications, listing events, and showing pod logs.

## Project Structure

- `src/` - Source code for the MCP server and tools
- `config/` - Environment configuration
- `tests/` - Pytest-based tests
- `docs/` - Documentation

## Setup

1. **Install dependencies** (requires Python 3.10+ and [uv](https://github.com/astral-sh/uv)):

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt  # or use `uv pip install .` if using pyproject.toml
```

2. **Configure environment**:

Create `config/.env` with:

```
ARGOCD_API_URL=https://cd.apps.argoproj.io
ARGOCD_USERNAME=admin
ARGOCD_PASSWORD=yourpassword
```

## Usage

Run the server (default: stdio):

```bash
uv run src/server.py
```

To use SSE or HTTP transport, set `MCP_TRANSPORT=sse` or `MCP_TRANSPORT=http` in your environment.

## Tools

- `list_applications`: List all ArgoCD applications
- `create_application`: Create a new ArgoCD application
- `delete_application`: Delete an ArgoCD application
- `force_sync_application`: Force sync an ArgoCD application
- `list_event_applications`: List events for an ArgoCD application
- `show_pod_logs`: Show pod logs for an application
- `rollback_application`: Rollback an ArgoCD application

## Testing

Run tests with pytest:

```bash
pytest tests/
```

## References

- [MCP Server Quickstart](https://modelcontextprotocol.io/quickstart/server)
- [ArgoCD ApplicationService API](https://cd.apps.argoproj.io/swagger-ui#tag/ApplicationService)
- [ArgoCD AccountService_CreateToken](https://cd.apps.argoproj.io/swagger-ui#operation/AccountService_CreateToken) 