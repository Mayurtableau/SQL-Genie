import psycopg2
from psycopg2.extras import RealDictCursor

# --- Establish connection ---
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="admin",
        port=5432
    )

# --- Save user query ---
def save_user_query(user_id, query_text, generated_sql):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO queries (user_id, query_text, generated_sql, created_at)
        VALUES (%s, %s, %s, NOW())
        """,
        (user_id, str(query_text), str(generated_sql))
    )
    conn.commit()
    cur.close()
    conn.close()

# --- Fetch all queries for user ---
def get_user_queries(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT id, query_text, generated_sql, created_at 
        FROM queries 
        WHERE user_id = %s 
        ORDER BY created_at DESC
        """,
        (user_id,)
    )
    queries = cur.fetchall()
    cur.close()
    conn.close()
    return queries

# --- Fetch single query by ID (optional, for reloading a specific one) ---
def get_query_by_id(query_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM queries WHERE id = %s", (query_id,))
    query = cur.fetchone()
    cur.close()
    conn.close()
    return query