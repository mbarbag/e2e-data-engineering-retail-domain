from sqlalchemy import create_engine, text
import time
import os
import pandas as pd
import glob
import sys

OUTPUT_BASE = os.getenv("OUTPUT_BASE")
CHUNK_SIZE = 10_000

TABLES = [
    ("mstr_proveedores", "MSTR_PROVEEDORES", "csv"),
    ("mstr_articulos", "MSTR_ARTICULOS", "csv"),
    ("mstr_tiendas", "MSTR_TIENDAS", "csv"),
    ("crm_miembros", "CRM_MIEMBROS", "parquet"),
    ("trans_ventas", "TRANS_VENTAS", "parquet"),
    ("inv_stock_diario", "INV_STOCK_DIARIO", "parquet"),
    ("post_devoluciones", "POST_DEVOLUCIONES", "json"),
]

DATE_COLUMNS = {
    "mstr_proveedores": [],
    "mstr_articulos": ["fec_alta"],
    "mstr_tiendas": ["fec_apertura"],
    "crm_miembros": ["fec_registro", "fec_ultima_compra"],
    "trans_ventas": ["fec_trans"],
    "inv_stock_diario": ["fec_snapshot"],
    "post_devoluciones": ["fec_devolucion"],
}

def read_table(folder: str, fmt: str, table_name: str) -> pd.DataFrame:
    ext_map = {"csv": "*.csv", "parquet": "*.parquet", "json": "*.json"}
    if fmt == "parquet":
        df = pd.read_parquet(folder)

    elif fmt == "csv":
        # glob para encontrar los part-files que genera Spark
        files = sorted(glob.glob(os.path.join(folder, ext_map[fmt])))
        files = [f for f in files if not os.path.basename(f).startswith("_")]
        df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

    elif fmt == "json":
        files = sorted(glob.glob(os.path.join(folder, ext_map[fmt])))
        files = [f for f in files if not os.path.basename(f).startswith("_")]
        df = pd.concat(
            [pd.read_json(f, lines=True) for f in files], ignore_index=True
        )
    else:
        raise ValueError(f"Formato no soportado: {fmt}")
    
    # Convertir columnas de fecha a datetime (vienen como string en CSV/JSON)
    for col in DATE_COLUMNS.get(table_name, []):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col],  errors="coerce").dt.date #errors="coerce" convierte fechas nulas a NaT en vez de lanzar error

    return df

def table_exists(engine, table_name: str) -> bool:
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT EXISTS ("
            "  SELECT 1 FROM information_schema.tables"
            "  WHERE table_name = :t"
            ")", 
        ), {"t": table_name})
        return result.scalar()

def load_table(df: pd.DataFrame, table_name: str, engine):
    # idempotencia si existe: TRUNCATE -> append
    if table_exists(engine, table_name):
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table_name}"))
        if_exists = "append"
    else:
        if_exists = "replace" # solo en la primera ejecución
 
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists=if_exists,
        index=False,
        chunksize=CHUNK_SIZE,
        method="multi", # INSERT en batch, mucho más rápido
    )


def main():

    # Use the environment variable defined in docker-compose.yml
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL no está definida.")
        sys.exit(1)
    engine = create_engine(db_url)

    for table_name, subpath, fmt in TABLES:
        folder = os.path.join(OUTPUT_BASE, subpath)
        print(f"\n  Cargando -> {table_name}  (formato: {fmt})")
        t0 = time.time()

        try:
            df = read_table(folder, fmt, table_name)
            #Escribe el DataFrame en la tabla Postgres en chunks
            n_rows = len(df)
            print(f"Filas a cargar : {n_rows:,}")
            print(f"Columnas : {list(df.columns)}")
            load_table(df, table_name, engine)
            elapsed = time.time() - t0
            print(f"[SUCCESS] Cargada en {elapsed:.1f}s")
        except Exception as e:
            print(f"[ERROR] {e}")
            sys.exit(1)
    print("[SUCCESS] Todas las tablas cargadas")

if __name__ == "__main__":
    main()