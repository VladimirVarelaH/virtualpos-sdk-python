# Sandbox de pruebas

Esta carpeta contiene scripts para probar el SDK instalado desde `../package`.

## 1) Instalar el SDK y dependencias de pruebas

Desde el root del proyecto:

```bash
pip install -e ./package
pip install -r ./sandbox/requirements.txt
```

## 2) Crear archivo de entorno

Copia `sandbox/env.example` a `sandbox/.env` y completa:

- `VIRTUALPOS_API_KEY`
- `VIRTUALPOS_SECRET_KEY`

Variables opcionales:

- `VIRTUALPOS_ENV` (`sandbox` o `production`)
- `VIRTUALPOS_TIMEOUT`
- IDs de recursos para pruebas `get_*`

## 3) Ejecutar pruebas

```bash
python sandbox/env_test_calls.py
```

