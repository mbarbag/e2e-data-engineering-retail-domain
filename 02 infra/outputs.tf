output "datalake_bucket_name" {
  description = "Nombre del bucket S3 data lake."
  value = aws_s3_bucket.datalake.id
}

output "datalake_bucket_arn" {
  description = "ARN del bucket S3 data lake."
  value = aws_s3_bucket.datalake.arn
}

output "postgres_secret_arn" {
  description = "ARN del secreto de PostgreSQL en Secrets Manager."
  value = aws_secretsmanager_secret.postgres.arn
}
