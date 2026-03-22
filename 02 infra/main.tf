# ──────────────────────────────────────────────────────────────
# RetailMax — Terraform
# ──────────────────────────────────────────────────────────────
# Uso:
#   bash init-backend.sh # una sola vez
#   terraform init
#   terraform workspace new dev # primera vez
#   terraform workspace select dev
#   terraform apply -var-file="envs/dev/terraform.tfvars"
# ──────────────────────────────────────────────────────────────

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.37.0"
    }
  }

  backend "s3" {
    bucket = "mg-retailmax-tfstate"
    key = "retailmax/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project = "RetailMax"
      Environment = terraform.workspace
      ManagedBy = "Terraform"
    }
  }
}

locals {
  name_prefix = "retailmax-${terraform.workspace}"
  bucket_name = "${var.s3_bucket_prefix}-${terraform.workspace}"
}

# ══════════════════════════════════════════════════════════════
# S3 — Data Lake
# ══════════════════════════════════════════════════════════════
resource "aws_s3_bucket" "datalake" {
  bucket = local.bucket_name
  force_destroy = var.s3_force_destroy
  tags = { Name = local.bucket_name }
}

resource "aws_s3_bucket_public_access_block" "datalake" {
  bucket = aws_s3_bucket.datalake.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}

# Cifrado con clave administrada por AWS (SSE-S3) — sin costo adicional
resource "aws_s3_bucket_server_side_encryption_configuration" "datalake" {
  bucket = aws_s3_bucket.datalake.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "datalake" {
  bucket = aws_s3_bucket.datalake.id
  versioning_configuration {
    status = terraform.workspace == "prod" ? "Enabled" : "Disabled"
  }
}

# Estructura de carpetas medallón
resource "aws_s3_object" "prefixes" {
  for_each = toset([
    "raw/postgres/mstr_proveedores/",
    "raw/postgres/mstr_articulos/",
    "raw/postgres/mstr_tiendas/",
    "raw/postgres/crm_miembros/",
    "raw/postgres/trans_ventas/",
    "raw/postgres/inv_stock_diario/",
    "raw/postgres/post_devoluciones/",
    "bronze/",
    "silver/",
    "gold/",
    "logs/ingestion/",
  ])
  bucket = aws_s3_bucket.datalake.id
  key = each.value
  content = ""
}

resource "aws_s3_bucket_lifecycle_configuration" "datalake" {
  count = terraform.workspace == "prod" ? 1 : 0
  bucket = aws_s3_bucket.datalake.id
  rule {
    id = "expire-noncurrent-versions"
    status = "Enabled"
    filter { prefix = "" }
    noncurrent_version_expiration { noncurrent_days = 90 }
  }
}

# ══════════════════════════════════════════════════════════════
# Secrets Manager — Credenciales de PostgreSQL
# Terraform crea el contenedor. El valor real se carga con:
#   aws secretsmanager put-secret-value \
#     --secret-id <nombre> \
#     --secret-string '{"host":"...","password":"..."}'
# ══════════════════════════════════════════════════════════════
resource "aws_secretsmanager_secret" "postgres" {
  name = var.postgres_secret_name
  description = "Credenciales PostgreSQL RetailMax ${terraform.workspace}"
  recovery_window_in_days = terraform.workspace == "prod" ? 30 : 0
  tags = { Name = var.postgres_secret_name }
}

resource "aws_secretsmanager_secret_version" "postgres_template" {
  secret_id = aws_secretsmanager_secret.postgres.id
  secret_string = jsonencode({
    host = "REPLACE_WITH_POSTGRES_HOST"
    port = "5432"
    dbname = "REPLACE_WITH_DB_NAME"
    username = "REPLACE_WITH_USERNAME"
    password = "REPLACE_WITH_PASSWORD"
  })
  lifecycle { ignore_changes = [secret_string] }
}
