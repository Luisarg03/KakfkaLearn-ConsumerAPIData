CREATE TABLE IF NOT EXISTS test.autos_usados (
	id serial NOT NULL PRIMARY KEY,
    register_id varchar NOT NULL,
	json_data json NOT NULL
);
INSERT INTO test.autos_usados (register_id, json_data)
VALUES('{{{REGISTER_ID}}}', '{{{DATA}}}');