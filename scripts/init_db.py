import os
import psycopg2
from time import sleep
from sqlalchemy import create_engine, text, exc


DBNAME = os.environ['DATABASE_NAME']
USER = os.environ['DATABASE_USER']
PASSWORD = os.environ['DATABASE_PASSWORD']
HOST = os.environ['DATABASE_HOST']
SCHEMA_NAME = os.environ['SCHEMA_NAME']

# DBNAME = "mydatabase"
# USER = "myuser"
# PASSWORD = "mypassword"
# HOST = "localhost"
# SCHEMA_NAME = "myschemadata2"

sql_file_path = './init.sql'
replacements = {
    '{{{DB_NAME}}}': DBNAME,
    '{{{SCHEMA_NAME}}}': SCHEMA_NAME
}


def connect_to_database(dbname, user, password, host, retries=4, delay=15):
    while retries:
        try:
            return psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host
            )
        except psycopg2.OperationalError as e:
            retries -= 1
            print(e)
            print("Error al conectar a la base de datos, reintentando...")
            sleep(delay)

    raise Exception("No se pudo conectar a la base de datos")


conn = connect_to_database(DBNAME, USER, PASSWORD, HOST, retries=5, delay=10)
engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:5432/{DBNAME}')


def execute_sql_script(engine, script_path, replacements):
    with open(script_path, 'r') as file:
        sql_script = file.read()
        file.close()

        for old_value, new_value in replacements.items():
            sql_script = sql_script.replace(old_value, new_value)

        commands = sql_script.split(';')

        for command in commands:
            if command.strip() != '':
                command = command + ';'
                command = command.strip().replace('\n', ' ')
                with engine.connect() as connection:
                    connection.execution_options(isolation_level="AUTOCOMMIT")
                    try:
                        connection.execute(text(command))
                    except (Exception, exc.ProgrammingError) as e:
                        print(f"COMMAND: {command} >>> FAILED EXEC\n")
                        print(e)


execute_sql_script(engine, sql_file_path, replacements)
