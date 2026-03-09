# virtualpos-sdk-python

Proyecto organizado en dos carpetas:

- `package/`: codigo del SDK listo para publicar/instalar por `pip`.
- `sandbox/`: scripts y configuracion para probar integraciones localmente.

## Instalacion local (modo desarrollo)

```bash
pip install -e ./package
```

## Instalacion desde GitHub

Reemplaza `TU_USUARIO/TU_REPO` por tu repositorio publico:

```bash
pip install "git+https://github.com/TU_USUARIO/TU_REPO.git@main#subdirectory=package"
```

Recomendado para version estable con tag:

```bash
pip install "git+https://github.com/TU_USUARIO/TU_REPO.git@v0.1.0#subdirectory=package"
```

## Pruebas de integracion (sandbox)

```bash
pip install -r ./sandbox/requirements.txt
python sandbox/env_test_calls.py
```

Antes de ejecutar, copia `sandbox/env.example` a `sandbox/.env` y completa tus credenciales.

