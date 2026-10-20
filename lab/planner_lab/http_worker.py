"""Private subprocess boundary so deadlines/cancellation can stop a blocking HTTPS call."""
import json
import os
import socket
import sys
import urllib.error
import urllib.request


def main():
    # This worker is invoked by the adapter, never as a credential-management tool.
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return {"error": "missing_api_key"}
    try:
        data = json.loads(sys.stdin.read(131072))
        body = json.dumps(data["payload"]).encode("utf-8")
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses", data=body, method="POST",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=data["timeout"]) as response:
            raw = response.read(1_000_001)
        if len(raw) > 1_000_000:
            return {"error": "malformed_output"}
        return {"response": json.loads(raw)}
    except urllib.error.HTTPError as error:
        if error.code == 429:
            return {"error": "rate_limit"}
        if error.code in (408, 504):
            return {"error": "provider_timeout"}
        if 500 <= error.code <= 599:
            return {"error": "provider_unavailable"}
        return {"error": "provider_http_error"}
    except (TimeoutError, socket.timeout):
        return {"error": "provider_timeout"}
    except urllib.error.URLError:
        return {"error": "provider_network_error"}
    except Exception:
        return {"error": "provider_transport_error"}


if __name__ == "__main__":
    print(json.dumps(main()))
