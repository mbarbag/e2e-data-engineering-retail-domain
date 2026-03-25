# Infrastructura como Código: Terraform

El *init-backend.sh* debe ser ejecutado antes que todo, ya que crea el bucket en S3 para guardar el .tfstate. Consideraciones tenidas en cuenta: se bloqueó el public access, se agregó configuración de encriptación y se habilitó el versionamiento.

En el *main.tf* encontrarás los recursos a aprovisional: S3 y Secrets Manager para conectarse a la Postgres DB. Junto con configuraciones particulares según el ambiente definido en */envs.

### Evidencia
- init-backend.sh

<img alt="Captura de pantalla 2026-03-22 a la(s) 11 34 59 a m" src="https://github.com/user-attachments/assets/5acea36e-9a12-495a-998d-2afcf31f264b" />

- terraform apply

<img alt="Captura de pantalla 2026-03-22 a la(s) 11 54 25 a m" src="https://github.com/user-attachments/assets/1c08a9d7-ef68-444f-bdff-2ee76ee6c530" />
