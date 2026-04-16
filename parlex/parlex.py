import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse

MCP_PROTOCOL_VERSION = "2024-11-05"


def normalize_mcp_url(url: str) -> str:
    """Normalize MCP URL by trimming surrounding whitespace."""
    return url.strip()


def alternate_mcp_url(url: str) -> str:
    """Return slash-toggled variant (/mcp <-> /mcp/)."""
    if url.endswith("/"):
        return url[:-1]
    return f"{url}/"


def mcp_jsonrpc_call(
    mcp_url: str,
    method: str,
    params: Optional[Dict[str, Any]] = None,
    request_id: int = 1,
    session_id: Optional[str] = None,
    access_token: Optional[str] = None,
    api_key: Optional[str] = None,
    external_access_token: Optional[str] = None,
    max_redirects: int = 2,
) -> Tuple[Dict[str, Any], Optional[str]]:
    """Call an MCP JSON-RPC endpoint and return response + session id."""
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params or {},
    }
    data = json.dumps(payload).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "parlex-mcp-test-script/0.1",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    if api_key:
        headers["x-api-key"] = api_key
    if external_access_token:
        headers["x-external-access-token"] = external_access_token

    request = urllib.request.Request(mcp_url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            response_payload: Dict[str, Any] = {}
            if body:
                trimmed = body.strip()
                if trimmed.startswith("event:") or "\ndata:" in trimmed:
                    # Parse minimal SSE response and extract the last JSON `data:` payload.
                    data_lines = []
                    for line in body.splitlines():
                        if line.startswith("data:"):
                            data_lines.append(line[len("data:") :].strip())
                    if data_lines:
                        response_payload = json.loads(data_lines[-1])
                else:
                    response_payload = json.loads(body)
            returned_session_id = response.headers.get("Mcp-Session-Id")
            return response_payload, returned_session_id or session_id
    except urllib.error.HTTPError as error:
        if error.code in {307, 308} and max_redirects > 0:
            location = error.headers.get("Location")
            if location:
                return mcp_jsonrpc_call(
                    mcp_url=location,
                    method=method,
                    params=params,
                    request_id=request_id,
                    session_id=session_id,
                    access_token=access_token,
                    api_key=api_key,
                    external_access_token=external_access_token,
                    max_redirects=max_redirects - 1,
                )
        raise


def fetch_parlex_context(topic: str = "artificial intelligence regulation") -> str:
    """Fetch a small MCP context payload for an LLM prompt."""
    mcp_url = normalize_mcp_url(os.getenv("PARLIAMENT_MCP_URL", ""))
    access_token = (
        os.getenv("PARLIAMENT_MCP_ACCESS_TOKEN", "").strip()
        or os.getenv("PARLEX_MCP_ACCESS_TOKEN", "").strip()
        or None
    )
    external_access_token = (
        os.getenv("PARLIAMENT_MCP_EXTERNAL_ACCESS_TOKEN", "").strip()
        or os.getenv("PARLEX_MCP_EXTERNAL_ACCESS_TOKEN", "").strip()
        or os.getenv("PARLIAMENT_MCP_ACCESS_TOKEN", "").strip()
        or None
    )
    api_key = (
        os.getenv("PARLIAMENT_MCP_API_KEY", "").strip()
        or os.getenv("PARLEX_MCP_API_KEY", "").strip()
        or None
    )

    if not mcp_url:
        return (
            "MCP call skipped: PARLIAMENT_MCP_URL is not set. "
            "Set it in .env to call the hosted Parlex MCP."
        )

    parsed_url = urlparse(mcp_url)
    is_local = parsed_url.hostname in {"localhost", "127.0.0.1"}
    if not is_local and not access_token and not api_key and not external_access_token:
        return (
            "MCP call skipped: hosted MCP auth is missing. Add one of "
            "PARLIAMENT_MCP_ACCESS_TOKEN (bearer token) or "
            "PARLIAMENT_MCP_API_KEY (x-api-key) or "
            "PARLIAMENT_MCP_EXTERNAL_ACCESS_TOKEN (x-external-access-token) to .env."
        )

    session_id: Optional[str] = None

    urls_to_try = [mcp_url]
    alt_url = alternate_mcp_url(mcp_url)
    if alt_url != mcp_url:
        urls_to_try.append(alt_url)

    last_error: Optional[str] = None
    for candidate_url in urls_to_try:
        try:
            initialize_response, session_id = mcp_jsonrpc_call(
                mcp_url=candidate_url,
                method="initialize",
                params={
                    "protocolVersion": MCP_PROTOCOL_VERSION,
                    "capabilities": {},
                    "clientInfo": {"name": "max-test-script", "version": "0.1.0"},
                },
                request_id=1,
                access_token=access_token,
                api_key=api_key,
                external_access_token=external_access_token,
            )

            tools_response, session_id = mcp_jsonrpc_call(
                mcp_url=candidate_url,
                method="tools/list",
                params={},
                request_id=2,
                session_id=session_id,
                access_token=access_token,
                api_key=api_key,
                external_access_token=external_access_token,
            )

            tool_call_response: Dict[str, Any] = {"note": "No tool call attempted"}
            tools = tools_response.get("result", {}).get("tools", [])
            tool_names = {tool.get("name") for tool in tools if isinstance(tool, dict)}

            if "search_debate_titles" in tool_names:
                tool_call_response, _ = mcp_jsonrpc_call(
                    mcp_url=candidate_url,
                    method="tools/call",
                    params={
                        "name": "search_debate_titles",
                        "arguments": {"query": topic},
                    },
                    request_id=3,
                    session_id=session_id,
                    access_token=access_token,
                    api_key=api_key,
                    external_access_token=external_access_token,
                )

            context_payload = {
                "endpoint_used": candidate_url,
                "initialize": initialize_response,
                "tools_list_summary": sorted([name for name in tool_names if name]),
                "sample_tool_call": tool_call_response,
            }
            return json.dumps(context_payload, indent=2)
        except urllib.error.HTTPError as error:
            last_error = f"MCP HTTP error {error.code}: {error.reason}"
        except urllib.error.URLError as error:
            last_error = f"MCP URL error: {error.reason}"
        except Exception as error:
            last_error = f"MCP unexpected error: {error}"

    return last_error or "MCP error: unknown failure"
