import sqlite3
import psycopg

SQLITE_DB = "nexus_one.db"

POSTGRES_URL = (
    "postgresql://nexus_admin:nexus_local_password"
    "@127.0.0.1:5432/nexus_one"
)

TABLES = [
    "users",
    "refresh_tokens",
    "blacklist_tokens",
    "chat_history",
    "audit_logs",
    "security_events",
    "password_reset_tokens",
]

sqlite_conn = sqlite3.connect(SQLITE_DB)
sqlite_conn.row_factory = sqlite3.Row

pg_conn = psycopg.connect(POSTGRES_URL)

try:
    print("Starting SQLite -> PostgreSQL migration...")
    
    # Clear PostgreSQL tables first so this migration is repeatable.
    with pg_conn.cursor() as cur:
        for table in reversed(TABLES):
            cur.execute(f'DELETE FROM "{table}"')

    for table in TABLES:
        print(f"\nMigrating: {table}")

        rows = sqlite_conn.execute(
            f'SELECT * FROM "{table}"'
        ).fetchall()

        if not rows:
            print("  SQLite rows: 0")
            continue

        columns = rows[0].keys()
        column_list = ", ".join(f'"{c}"' for c in columns)
        placeholders = ", ".join(["%s"] * len(columns))

        sql = (
            f'INSERT INTO "{table}" '
            f'({column_list}) VALUES ({placeholders})'
        )

        with pg_conn.cursor() as cur:
            for row in rows:
                values = []

                for value in row:
                    # SQLite stores booleans as 0/1.
                    if table in (
                        "users",
                        "refresh_tokens",
                    ):
                        column_name = list(columns)[len(values)]

                        if column_name in ("is_active",):
                            value = bool(value) if value is not None else None

                    # PostgreSQL audit_logs.status is NOT NULL.
                    # Older SQLite records may contain NULL.
                    if table == "audit_logs":
                        column_name = list(columns)[len(values)]

                        if column_name == "status" and value is None:
                            value = "SUCCESS"

                        if column_name == "severity" and value is None:
                            value = "INFO"

                    values.append(value)

                cur.execute(sql, values)

        print(f"  Migrated rows: {len(rows)}")

    pg_conn.commit()

    print("\n===================================")
    print("MIGRATION COMPLETED SUCCESSFULLY")
    print("===================================")

finally:
    sqlite_conn.close()
    pg_conn.close()
