import sqlite3


def get_connection():

    conn = sqlite3.connect(
        "database/nifty100.db"
    )

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


def get_table_count():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT count(*)
        FROM sqlite_master
        WHERE type='table'
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


if __name__ == "__main__":

    print(
        f"Tables: {get_table_count()}"
    )
