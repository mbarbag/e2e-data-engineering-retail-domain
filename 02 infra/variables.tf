variable "aws_region" {
  description = "Región AWS."
  type = string
  default = "us-east-1"
}

variable "s3_bucket_prefix" {
  description = "Prefijo del bucket S3. Resultado final: <prefix>-dev / <prefix>-prod."
  type = string
  default = "retailmax-datalake"
}

variable "s3_force_destroy" {
  description = "Permite destruir el bucket con objetos. true solo en dev."
  type = bool
  default = false
}

variable "postgres_secret_name" {
  description = "Nombre del secreto en Secrets Manager para las credenciales de PostgreSQL."
  type = string
  default = "retailmax/postgres"
}
