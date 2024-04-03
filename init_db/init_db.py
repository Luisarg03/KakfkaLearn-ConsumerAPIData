import os
import psycopg2
from time import sleep
from sqlalchemy import create_engine, text, exc


DBNAME = os.environ['DATABASE_NAME']
USER = os.environ['DATABASE_USER']
PASSWORD = os.environ['DATABASE_PASSWORD']
HOST = os.environ['DATABASE_HOST']
PORT = os.environ['DATABASE_PORT']
SCHEMA_NAME = os.environ['SCHEMA_NAME']

# PORT = '5433'
# USER = 'USER_ADMIN'
# PASSWORD = 'USER_ADMIN_PASSWORD'
# DBNAME = 'AIRFLOW_DB'
# SCHEMA_NAME = 'AIRFLOW_DATA'
# HOST = 'localhost'


def connect_to_database(dbname, user, password, host, port, retries=4, delay=15):
    while retries:
        try:
            return psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
        except psycopg2.OperationalError as e:
            retries -= 1
            print(e)
            print("Error al conectar a la base de datos, reintentando...")
            sleep(delay)

    raise Exception("No se pudo conectar a la base de datos")


conn = connect_to_database(DBNAME, USER, PASSWORD, HOST, PORT, retries=5, delay=10)
engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}')


def execute_sql_script(engine, script_path, replacements):
    with open(script_path, 'r') as file:
        sql_script = file.read()
        file.close()

        for old_value, new_value in replacements.items():
            sql_script = sql_script.replace(old_value, new_value)

        # Ejecuta el script completo en una sola transacción
        with engine.begin() as connection:
            try:
                connection.execute(text(sql_script))
            except (Exception, exc.SQLAlchemyError) as e:
                print(f"Error al ejecutar el script SQL: {e}")
                raise e


files_paths = [
    {
        'path': './init.sql',
        'replacements': {
            '{{{DB_NAME}}}': DBNAME,
            '{{{SCHEMA_NAME}}}': SCHEMA_NAME
        }
    }
]

for file in files_paths:
    sql_file_path = file['path']
    replacements = file['replacements']
    execute_sql_script(engine, sql_file_path, replacements)
    print(f"Script {sql_file_path} ejecutado correctamente")
