"""Load credentials from .env and run VirtualPOS test calls.

Usage:
    python sandbox/env_test_calls.py
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from virtualpos_sdk import VirtualPOSClient, VirtualPOSHTTPError


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Missing required env var: {name}")
    return value


def main() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)

    api_key = _require_env("VIRTUALPOS_API_KEY")
    secret_key = _require_env("VIRTUALPOS_SECRET_KEY")
    env_name = os.getenv("VIRTUALPOS_ENV", "sandbox").strip().lower()
    timeout = int(os.getenv("VIRTUALPOS_TIMEOUT", "30").strip())
    sandbox = env_name != "production"

    payment_id = os.getenv("VIRTUALPOS_PAYMENT_ID", "").strip()
    plan_id = os.getenv("VIRTUALPOS_PLAN_ID", "").strip()
    suscription_id = os.getenv("VIRTUALPOS_SUSCRIPTION_ID", "").strip()
    charge_id = os.getenv("VIRTUALPOS_CHARGE_ID", "").strip()

    print(f"Using env: {'sandbox' if sandbox else 'production'}")
    with VirtualPOSClient(api_key=api_key, secret_key=secret_key, sandbox=sandbox, timeout=timeout) as client:
        try:
            print("\n[1] list_payments(limit=1, page=0)")
            print(client.list_payments(limit=1, page=0))
        except VirtualPOSHTTPError as exc:
            print(f"list_payments failed: {exc} | status={exc.status_code} payload={exc.payload}")

        try:
            print("\n[2] list_plans(limit=1, page=0)")
            print(client.list_plans(limit=1, page=0))
        except VirtualPOSHTTPError as exc:
            print(f"list_plans failed: {exc} | status={exc.status_code} payload={exc.payload}")

        try:
            print("\n[3] list_suscriptions(limit=1, page=0)")
            print(client.list_suscriptions(limit=1, page=0))
        except VirtualPOSHTTPError as exc:
            print(f"list_suscriptions failed: {exc} | status={exc.status_code} payload={exc.payload}")

        if payment_id:
            try:
                print(f"\n[4] get_payment({payment_id})")
                print(client.get_payment(payment_id))
            except VirtualPOSHTTPError as exc:
                print(f"get_payment failed: {exc} | status={exc.status_code} payload={exc.payload}")

        if plan_id:
            try:
                print(f"\n[5] get_plan({plan_id})")
                print(client.get_plan(plan_id))
            except VirtualPOSHTTPError as exc:
                print(f"get_plan failed: {exc} | status={exc.status_code} payload={exc.payload}")

        if suscription_id:
            try:
                print(f"\n[6] get_suscription({suscription_id})")
                print(client.get_suscription(suscription_id))
            except VirtualPOSHTTPError as exc:
                print(f"get_suscription failed: {exc} | status={exc.status_code} payload={exc.payload}")

            try:
                print(f"\n[7] list_charges({suscription_id}, limit=1, page=0)")
                print(client.list_charges(suscription_id, limit=1, page=0))
            except VirtualPOSHTTPError as exc:
                print(f"list_charges failed: {exc} | status={exc.status_code} payload={exc.payload}")

        if charge_id:
            try:
                print(f"\n[8] get_charge({charge_id})")
                print(client.get_charge(charge_id))
            except VirtualPOSHTTPError as exc:
                print(f"get_charge failed: {exc} | status={exc.status_code} payload={exc.payload}")


if __name__ == "__main__":
    main()

