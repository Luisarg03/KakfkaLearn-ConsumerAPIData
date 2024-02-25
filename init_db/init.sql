DO $$
BEGIN
    BEGIN
        EXECUTE 'DROP SCHEMA public CASCADE;';
    EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'No se pudo eliminar el esquema público. Error: %', SQLERRM;
    END;

    BEGIN
        EXECUTE format('CREATE SCHEMA %I;', {{{SCHEMA_NAME}}});
    EXCEPTION WHEN OTHERS THEN
        RAISE NOTICE 'No se pudo crear el esquema. Error: %', SQLERRM;
    END;
END
$$;
