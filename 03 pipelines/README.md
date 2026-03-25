# Pipeline

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

El resto del pipeline es orquestrado dentro de Databricks usando Jobs & Pipelines.
