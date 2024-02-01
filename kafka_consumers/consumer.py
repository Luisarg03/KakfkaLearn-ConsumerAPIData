import json
from confluent_kafka import Consumer, KafkaError
from sqlalchemy import create_engine, text, exc


config = {
    'bootstrap.servers': 'localhost:9094',
    'group.id': 'consumer_autos_usados',
    'auto.offset.reset': 'latest'
}

consumer = Consumer(**config)
consumer.subscribe(['autos_usados'])


DBNAME = "AIRFLOW_DB"
USER = "USER_ADMIN"
PASSWORD = "USER_ADMIN_PASSWORD"
HOST = "localhost"
SCHEMA_NAME = "AIRFLOW_DATA"
engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:5433/{DBNAME}')
sql_file_path = './init.sql'


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

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        register_id = json.loads(msg.value().decode('utf-8'))['id']
        msg = msg.value().decode('utf-8')

        replacements = {
            '{{{REGISTER_ID}}}': register_id,
            '{{{DATA}}}': msg
        }

        execute_sql_script(engine, sql_file_path, replacements)

finally:
    consumer.close()
