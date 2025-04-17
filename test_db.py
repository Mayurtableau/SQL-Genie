import psycopg2

def get_table_schema():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Get all tables from all schemas except system schemas
    cursor.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
        AND table_schema NOT IN ('pg_catalog', 'information_schema');
    """)
    tables = cursor.fetchall()

    schema = {}
    for table_schema, table_name in tables:
        full_table_name = f"{table_schema}.{table_name}"
        cursor.execute(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s;
        """, (table_schema, table_name))
        columns = [row[0] for row in cursor.fetchall()]
        schema[full_table_name] = columns

    conn.close()
    return schema
