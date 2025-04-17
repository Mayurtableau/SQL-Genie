import psycopg2
from psycopg2.extras import RealDictCursor

def run_query(query):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="admin"
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            # Convert each RealDictRow to regular dict
            result = [dict(row) for row in rows]
            columns = list(result[0].keys())
            return columns, [list(row.values()) for row in result]
        else:
            return [], []
    except Exception as e:
        return [], str(e)
    finally:
        conn.close()
