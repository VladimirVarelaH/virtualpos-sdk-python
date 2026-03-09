# VirtualPOS SDK for Python

SDK para simplificar la integracion con VirtualPOS API v3, basado en la coleccion `VirtualPOS-APIs-V3.postman_collection.json`.

## Instalacion

Desde la carpeta `package/`:

```bash
pip install .
```

## Uso rapido

```python
from virtualpos_sdk import VirtualPOSClient

# Si no pasas las credenciales, el constructor las solicita por consola.
client = VirtualPOSClient()

payload = {
    "amount": 9990,
    "email": "user@example.com",
    "social_id": "12345678-9",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "912345678",
    "description": "pago de prueba",
    "merchant_internal_code": "OC_TEST_1234",
    "merchant_internal_channel": "portal_pagos",
    "return_url": "aHR0cHM6Ly9odHRwYmluLm9yZy9wb3N0",
    "callback_url": "aHR0cHM6Ly9odHRwYmluLm9yZy9wb3N0",
}

response = client.create_payment(payload)
print(response)
```

Para scripts de pruebas con `.env`, revisa `../sandbox/README.md`.

## Credenciales y firmado

La clase genera automaticamente el header `Signature` como JWT HS256 firmado con `secret_key`, con payload:

```json
{"api_key":"..."}
```

Y envia los headers requeridos por la documentacion:

- `Content-Type: application/json`
- `Authorization: <api_key>`
- `Signature: <jwt_firmado>`

Referencia oficial: https://virtualpos.readme.io/reference/getting-started-with-your-api

