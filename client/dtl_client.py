"""Minimal DTL API client — stdlib only, no dependencies.

Usage:
    from dtl_client import DTLClient
    c = DTLClient(api_key="jv3_live_...")          # keys: jvi3.com/packages
    verdict = c.check("unitgate", "check", {"query": "E = m * a", "mode": "equation"})
    print(verdict["status"], verdict["passed"], verdict["certificate_hash"])

Free tier: 100 tokens/month, no card — enough to evaluate every gate.
Live catalog of gates, actions and per-call prices: GET /api/apigate/catalog
"""
from __future__ import annotations

import json
import urllib.request

DEFAULT_BASE = "https://jvi3.com"


class DTLClient:
    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE, timeout: float = 30.0):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        req = urllib.request.Request(
            self.base_url + path,
            data=json.dumps(body).encode() if body is not None else None,
            method=method,
            headers={
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
            },
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode())

    def catalog(self) -> dict:
        """Live gate catalog: endpoints, actions, per-call token prices."""
        return self._request("GET", "/api/apigate/catalog")

    def check(self, gate: str, action: str, body: dict) -> dict:
        """Run one verification call. Returns a verdict per schemas/verdict.schema.json."""
        return self._request("POST", f"/api/apigate/v1/{gate}/{action}", body)
