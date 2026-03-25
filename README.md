# End-to-End Data Pipeline - Retail Domain

En el siguiente repositorio encontrarás un **pipeline de datos e2e en el dominio Retail**.

Considerando el tiempo (*7 días para implementarlo*), los recursos limitados (*sólo tengo mi computador, AWS y Databricks limited editions*), y conocimientos básicos de cada uno de los negocios, decidí ejecutar el escenario en Retail con el objetivo de **maximizar la calidad arquitectónica con el menor riesgo de complejidad innecesaria**. Tanto salud como banca, tienen dominios relativamente complejos que 7 días de trabajo pueden quedarse cortos. Además introducen retos de privacidad más estrictos que pueden complicar la implementación. Y aunque el esenario de logística tiene un dominio relativamente fácil de entender, el escenario de Retail tiene un dominio más intuitivo, las métricas y los modelos dimensionales están bastante estandarizados, lo que me permite enfocarme en la **arquitectura y calidad del pipeline**.

Se buscó implementar un pipeline idempotente en la fase de carga incremental, después del historical backfill. 
Para esto se usó merge/upsert en lugar de append, Overwrite según la capa Medallón, y Timestamps de la última actualización. 

La arquitectura usada fue la siguiente:

- **Docker: Generación de Datos Sintéticos y carga a Postgres -> IaC: terraform -> Lago de datos en S3 -> Procesamiento, workflows y gobernanza: Databricks.**

Se implementó Data Quality Checks a lo largo de toda la arquitectura medallón para asegurar la integridad de los datos.

Y encontrarás aplicados principios SOLID en el código que facilitan la modularidad y el reuso. 

También verás implementación de logs estructurados y tabla de erores que permiten observabilidad del pipeline.
