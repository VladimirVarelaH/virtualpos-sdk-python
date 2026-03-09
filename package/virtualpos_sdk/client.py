"""Client implementation for VirtualPOS API v3."""

from __future__ import annotations

import base64
import getpass
import hashlib
import hmac
import json
from typing import Any

import requests

from .exceptions import VirtualPOSAPIError, VirtualPOSHTTPError


class VirtualPOSClient:
    """Simple client for VirtualPOS API v3."""

    SANDBOX_BASE_URL = "https://api.virtualpos-sandbox.com"
    PRODUCTION_BASE_URL = "https://api.virtualpos.cl"

    def __init__(
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
        *,
        sandbox: bool = True,
        base_url: str | None = None,
        timeout: int = 30,
    ) -> None:
        # The user requested that credentials are prompted on instantiation.
        self.api_key = (api_key or input("VirtualPOS API KEY: ")).strip()
        self.secret_key = (secret_key or getpass.getpass("VirtualPOS SECRET KEY: ")).strip()
        if not self.api_key or not self.secret_key:
            raise ValueError("Both api_key and secret_key are required.")

        self.base_url = (base_url or (self.SANDBOX_BASE_URL if sandbox else self.PRODUCTION_BASE_URL)).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _base64url(self, data: bytes) -> str:
        encoded = base64.urlsafe_b64encode(data).decode("utf-8")
        return encoded.rstrip("=")

    def _build_signature(self) -> str:
        header = {"typ": "JWT", "alg": "HS256"}
        payload = {"api_key": self.api_key}

        header_encoded = self._base64url(
            json.dumps(header, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        )
        payload_encoded = self._base64url(
            json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        )
        token = f"{header_encoded}.{payload_encoded}"

        digest = hmac.new(
            self.secret_key.encode("utf-8"),
            token.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        signature_encoded = self._base64url(digest)
        return f"{token}.{signature_encoded}"

    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
            "Signature": self._build_signature(),
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}/v3/{path.lstrip('/')}"
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=self._headers(),
                params=params,
                json=json_body,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise VirtualPOSHTTPError(f"HTTP request failed: {exc}", status_code=0, payload=None) from exc

        try:
            data = response.json()
        except ValueError:
            data = {"raw_response": response.text}

        if not response.ok:
            raise VirtualPOSHTTPError(
                message=f"VirtualPOS API error ({response.status_code})",
                status_code=response.status_code,
                payload=data,
            )
        return data

    # Payments
    def create_payment(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "payment", json_body=payload)

    def get_payment(self, payment_id: str) -> dict[str, Any]:
        return self._request("GET", f"payment/{payment_id}")

    def cancel_payment(self, payment_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"payment/{payment_id}")

    def list_payments(self, *, limit: int = 10, page: int = 0) -> dict[str, Any]:
        return self._request("GET", "payments", params={"limit": limit, "page": page})

    def get_webcheckout_link(self, payment_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", f"payment/{payment_id}/webcheckout", json_body=payload)

    def authorize_payment(self, payment_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", f"payment/{payment_id}/authorize", json_body=payload)

    def send_payment(self, payment_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", f"payment/{payment_id}/send", json_body=payload)

    # Plans
    def create_plan(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "plan", json_body=payload)

    def get_plan(self, plan_id: str) -> dict[str, Any]:
        return self._request("GET", f"plan/{plan_id}")

    def list_plans(self, *, limit: int = 10, page: int = 0) -> dict[str, Any]:
        return self._request("GET", "plans", params={"limit": limit, "page": page})

    # Suscriptions
    def create_suscription(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "suscription", json_body=payload)

    def cancel_suscription(self, suscription_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"suscription/{suscription_id}")

    def get_suscription(self, suscription_id: str) -> dict[str, Any]:
        return self._request("GET", f"suscription/{suscription_id}")

    def list_suscriptions(self, *, limit: int = 10, page: int = 0) -> dict[str, Any]:
        return self._request("GET", "suscriptions", params={"limit": limit, "page": page})

    def generate_change_card_link(self, suscription_id: str) -> dict[str, Any]:
        return self._request("PUT", f"suscription/{suscription_id}/changecard")

    # Charges
    def create_charge(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "charge", json_body=payload)

    def cancel_charge(self, charge_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"charge/{charge_id}")

    def get_charge(self, charge_id: str) -> dict[str, Any]:
        return self._request("GET", f"charge/{charge_id}")

    def list_charges(self, suscription_id: str, *, limit: int = 10, page: int = 0) -> dict[str, Any]:
        return self._request(
            "GET",
            f"suscription/{suscription_id}/charges",
            params={"limit": limit, "page": page},
        )

    def cancel_future_charges(self, suscription_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"charges/{suscription_id}")

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> "VirtualPOSClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

