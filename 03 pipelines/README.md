# Pipeline y Orquestación

Para extraer la BD en Postgres y cargarla a S3 primero debes cargar las credenciales reales en Secrets Manager, en */02 infra* ejecuta: 
```
aws secretsmanager put-secret-value \
  --secret-id "retailmax/dev/postgres" \
  --secret-string '{"host":"...","password":"..."}'
```
Luego, exporta el bucket
```
export S3_BUCKET=$(terraform output -raw datalake_bucket_name)
```
Finalmente, ejecuta *postgres-to-s3.py*

**NOTA: El resto del pipeline es orquestado dentro de Databricks usando Jobs & Pipelines.**

## Decisión sobre Slowly Changing Dimensions (SCD)

Este pipeline no implementa explícitamente estrategias SCD Tipo 2 o Tipo 3. En su lugar, adopta un enfoque diferenciado por capa alineado con el propósito de la arquitectura Medallion y el alcance del caso de estudio.

En la capa **Bronze**, los datos se almacenan en modo *append-only* con metadatos de auditoría (`ingestion_timestamp`, `source_system`, `batch_id`). Esto preserva el histórico técnico completo del dato fuente.

En la capa **Silver**, las tablas se recalculan completamente en cada ejecución mediante *overwrite*. Esta decisión garantiza consistencia ante cambios en reglas de limpieza, tipificación o validación, evitando la persistencia de errores derivados de ejecuciones anteriores.

En la capa **Gold**, las dimensiones se mantienen mediante operaciones `MERGE` por clave primaria, lo que equivale funcionalmente a una estrategia **SCD Tipo 1** (sobrescritura del valor anterior sin conservación de versiones históricas). Esta aproximación es suficiente para los requerimientos analíticos del escenario, ya que no es necesario conservar el historial de cambios en los atributos de las dimensiones para responder las preguntas de negocio planteadas.

Aunque en esta versión del pipeline no se implementó SCD Tipo 2, tablas como dim_clientes y dim_productos podrían beneficiarse de historización en una evolución futura del modelo. Por ejemplo, cambios en atributos como el canal preferido del cliente, su estado activo o el precio de lista de un producto pueden ser relevantes para análisis longitudinales de comportamiento o de margen. En ese caso, sería necesario agregar columnas de vigencia (fec_inicio, fec_fin, es_vigente) e incorporar lógica para cerrar versiones anteriores de los registros durante las cargas incrementales.

## Evidencia:
- postgres-to-s3.py
<img alt="Captura de pantalla 2026-03-23 a la(s) 10 02 00 a m" src="https://github.com/user-attachments/assets/2c98eba5-1f4d-4a51-81b0-797524354bb9" />

- tabla de logs
<img alt="image" src="https://github.com/user-attachments/assets/ac820b8e-3014-4b86-b822-f6e104b386c1" />

- tabla de integridad referencial
<img alt="image" src="https://github.com/user-attachments/assets/47dc3ab2-763d-4f54-b453-094a40d5ca0e" />

- agg_ventas_diarias
<img alt="image" src="https://github.com/user-attachments/assets/b8ac9734-67ee-49f4-bebf-23655d0f89a8" />

- agg_top10_articulos_diarios
<img alt="image" src="https://github.com/user-attachments/assets/10f4941c-bfd2-4179-8004-3a4302be7616" />

- agg_conversion_canal
<img alt="image" src="https://github.com/user-attachments/assets/6625857c-09b9-4680-b59f-28b94233622d" />

- informes de calidad
<img alt="image" src="https://github.com/user-attachments/assets/2fe4b72d-ec12-43cf-ae34-c53bd7cc030c" />

- orquestación
<img alt="image" src="https://github.com/user-attachments/assets/9f06d7d3-2e1c-4de0-a167-91305d2119b8" />

