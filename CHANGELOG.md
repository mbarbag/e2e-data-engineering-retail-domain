# Changelog

All notable changes to the RetailMax data pipeline are documented here.

---

## [0.4.0] - 2026-03-24

### Added — Medallion Architecture (Databricks)
**Author:** Manuela Barba Guerra

- `common.py` — utilidades compartidas: logging de ejecución, tabla de errores referenciales y función `upsert()` genérica con MERGE para idempotencia en gold
- `quality.py` — cinco validaciones automatizadas de calidad de datos: nulos, duplicados, integridad referencial, rango de valores y valores negativos
- `ingest.py` — ingesta incremental S3 → bronze con metadatos de auditoría (`_ingested_at`, `_source_system`, `_batch_id`) y registro de ejecución en `pipeline_log`
- `silver/dimensions.py` — limpieza y conformación de `mstr_proveedores`, `mstr_articulos`, `mstr_tiendas` y `crm_miembros`; enmascaramiento SHA-256 de PII en `id_miembro`
- `silver/facts.py` — limpieza de `trans_ventas`, `inv_stock_diario` y `post_devoluciones`; deduplicación (A1), corrección de stock negativo (A3) y rechazo de fechas inválidas (A2)
- `gold/dimensions.py` — construcción de `dim_productos`, `dim_tiendas` y `dim_clientes` con campos calculados: jerarquía de categorías, margen estimado, zona de distribución y antigüedad del cliente
- `gold/facts.py` — construcción de `fact_ventas`, `fact_inventario` (alerta de quiebre y cobertura de días), `fact_devoluciones`, `fact_rfm_clientes` (segmentación en 5 grupos), `agg_conversion_canal` y `agg_ventas_diarias` con comparativo semana anterior

---

## [0.3.0] - 2026-03-23

### Added — Ingesta Postgres → S3
**Author:** Manuela Barba Guerra

- `postgres-to-s3.py` — lee cada tabla desde PostgreSQL y sube snapshot completo a `s3://<bucket>/raw/postgres/<tabla>/` en formato Parquet

---

## [0.2.0] - 2026-03-22

### Added — Infrastructure as Code (Terraform + AWS)
**Author:** Manuela Barba Guerra

- `02 infra/main.tf` — bucket S3 data lake con estructura medallón (`raw/`, `bronze/`, `silver/`, `gold/`), cifrado AES-256, bloqueo de acceso público y versionado en prod
- `02 infra/variables.tf` — parámetros documentados: región, prefijo de bucket, modo de destrucción y nombre de secretos
- `02 infra/outputs.tf` — exporta ARN del bucket y ARN del secreto de PostgreSQL para consumo externo
- `02 infra/envs/dev/terraform.tfvars` — configuración del entorno de desarrollo
- `02 infra/envs/prod/terraform.tfvars` — configuración del entorno de producción
- `02 infra/bootstrap/init-backend.sh` — script de inicialización del backend S3 remoto para estado de Terraform
- `02 infra/.gitignore` — excluye `.tfstate`, `.terraform/` y archivos de variables locales del repositorio

---

## [0.1.0] - 2026-03-21

### Added — Generación de datos sintéticos
**Author:** Manuela Barba Guerra

- `synthetic-data-generator.py` — pipeline PySpark que genera datos sintéticos para 7 tablas (MSTR_PROVEEDORES, MSTR_ARTICULOS, MSTR_TIENDAS, CRM_MIEMBROS, TRANS_VENTAS, INV_STOCK_DIARIO, POST_DEVOLUCIONES) con distribuciones realistas, integridad referencial, 5% de nulos controlados y tres anomalías documentadas (A1: duplicados, A2: fechas inválidas, A3: stock negativo)
- `config.yml` — configuración externalizada: seed, rango de fechas, tasa de nulos y volúmenes por tabla
- `load-data.py` — carga archivos CSV, Parquet y JSON desde el output local hacia PostgreSQL con estrategia idempotente TRUNCATE + append
- `Dockerfile` — imagen de ingesta con pandas, SQLAlchemy y pyarrow
- `docker-compose.yml` — servicio `pgdatabase` (Postgres 16) y `ingest-service` con healthcheck y espera de conexión
