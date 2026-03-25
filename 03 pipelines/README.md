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

