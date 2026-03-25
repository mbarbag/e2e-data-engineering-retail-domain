# Infrastructura como Código: Terraform

El *init-backend.sh* debe ser ejecutado antes que todo, ya que crea el bucket en S3 para guardar el .tfstate. Consideraciones tenidas en cuenta: se bloqueó el public access, se agregó configuración de encriptación y se habilitó el versionamiento.

En el *main.tf* encontrarás los recursos a aprovisional: S3 y Secrets Manager para conectarse a la Postgres DB. Junto con configuraciones particulares según el ambiente definido en */envs.
