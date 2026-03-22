#!/bin/bash
# Crea el bucket S3 para el estado de Terraform.
# Ejecutar UNA SOLA VEZ antes del primer terraform init.
set -e

REGION="us-east-1"
STATE_BUCKET="mg-retailmax-tfstate"

echo "=== Creando bucket S3 para estado de Terraform ==="
aws s3api create-bucket \
  --bucket "$STATE_BUCKET" \
  --region "$REGION"

aws s3api put-public-access-block \
  --bucket "$STATE_BUCKET" \
  --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

aws s3api put-bucket-encryption \
  --bucket "$STATE_BUCKET" \
  --server-side-encryption-configuration \
    '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

aws s3api put-bucket-versioning \
  --bucket "$STATE_BUCKET" \
  --versioning-configuration Status=Enabled

echo ""
echo "[SUCCESS] Backend listo."
