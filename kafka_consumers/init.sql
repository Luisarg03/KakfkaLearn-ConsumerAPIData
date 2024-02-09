CREATE TABLE IF NOT EXISTS {{{SCHEMA_NAME}}}.{{{TABLE_NAME}}} (
	id serial NOT NULL PRIMARY KEY,
    register_id varchar NOT NULL,
	json_data json NOT NULL
);
INSERT INTO {{{SCHEMA_NAME}}}.{{{TABLE_NAME}}} (register_id, json_data)
VALUES('{{{REGISTER_ID}}}', '{{{DATA}}}');