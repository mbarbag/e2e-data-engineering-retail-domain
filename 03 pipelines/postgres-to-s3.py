import os
import io
import json
import boto3
import pandas as pd
from sqlalchemy import create_engine

SECRET_NAME = os.getenv("POSTGRES_SECRET_NAME", "retailmax/dev/postgres")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET") # obligatorio — exportar antes de correr

TABLES = [
    "mstr_proveedores",
    "mstr_articulos",
    "mstr_tiendas",
    "crm_miembros",
    "trans_ventas",
    "inv_stock_diario",
    "post_devoluciones",
]

def get_postgres_credentials(secret_name: str, region: str) -> dict:
    client = boto3.client("secretsmanager", region_name=region)
    secret = client.get_secret_value(SecretId=secret_name)
    return json.loads(secret["SecretString"])


def build_engine(creds: dict):
    url = (
        f"postgresql+psycopg2://{creds['username']}:{creds['password']}"
        f"@{creds['host']}:{creds['port']}/{creds['dbname']}"
    )
    return create_engine(url)


def upload_parquet(df: pd.DataFrame, bucket: str, key: str, s3_client):
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False, engine="pyarrow")
    buffer.seek(0)
    s3_client.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue()) # sobreescribe


def main():
    if not S3_BUCKET:
        raise ValueError("S3_BUCKET no está definido. Exporta la variable antes de correr.")

    print(f"Origen: Postgres ({SECRET_NAME})")
    print(f"Destino: s3://{S3_BUCKET}/raw/postgres/\n")

    creds = get_postgres_credentials(SECRET_NAME, AWS_REGION)
    engine = build_engine(creds)
    s3 = boto3.client("s3", region_name=AWS_REGION)

    for table in TABLES:
        print(f"  {table}", end=" ... ", flush=True)
        df = pd.read_sql_table(table, engine)
        key = f"raw/postgres/{table}/{table}.parquet"
        upload_parquet(df, S3_BUCKET, key, s3)
        print(f"{len(df):,} filas → s3://{S3_BUCKET}/{key}")

    print("\n[SUCCESS] Ingesta completada.")


if __name__ == "__main__":
    main()