"""Helper for schema validation. Clean file."""

def get_table_info(conn, table_name):
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    return [dict(zip(['cid','name','type','notnull','dflt','pk'], row)) for row in cursor.fetchall()]

def get_indexes(conn, table_name):
    cursor = conn.execute(f"PRAGMA index_list({table_name})")
    return [row[1] for row in cursor.fetchall()]
