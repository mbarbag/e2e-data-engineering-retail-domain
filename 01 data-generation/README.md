# Generación de Datos Sintéticos y carga en Postgres

En *synthetic-data-generator.ipynb* se generan los datos sintéticos que serán cargados a Postgres. En el *config.yaml* verás definidos las variables globales utilizadas: la semilla, las fechas de inicio y fin, y los volúmenes por tabla. El generador debes ejecutarlo manualmente antes de levantar docker-compose.

En el *docker-compose.yaml* verás implementados los containers que correran juntos: la postgres DB y el script de Pyhton que ingesta los datos sintéticos generados a Postgres desde el Dockerfile.

Para injestar los datos ejecuta el comando **docker-compose up** en tu terminal.

Puedes consultar los datos desde tu terminal con **pgcli -h localhost -U root -d myretail**. 
