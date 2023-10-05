import typing
import pymysql
import os


def get_sql_connection() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = pymysql.connections.Connection(
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        database=os.environ.get('DB_DATABASE')
    )
    return conn


def get_row(statement, values=None) -> typing.Optional[typing.Dict]:
    connection = get_sql_connection()
    cursor = connection.cursor()
    cursor.execute(statement, values)
    result = cursor.fetchone()
    columns = [x[0] for x in cursor.description]
    cursor.close()
    connection.close()
    if result is None:
        return None
    return dict(zip(columns, result))


def get_all_rows(statement, values=None) -> typing.List[typing.Dict]:
    connection = get_sql_connection()
    cursor = connection.cursor()
    cursor.execute(statement, values)
    results = cursor.fetchall()
    columns = [x[0] for x in cursor.description]
    cursor.close()
    connection.close()
    return [dict(zip(columns, row)) for row in results]


def insert(statement, values):
    connection = get_sql_connection()
    cursor = connection.cursor()
    cursor.execute(statement, values)
    row_id = cursor.lastrowid
    cursor.close()
    connection.commit()
    connection.close()
    return row_id


def insert_many(statement, values):
    connection = get_sql_connection()
    cursor = connection.cursor()
    cursor.executemany(statement, values)
    row_id = cursor.lastrowid
    cursor.close()
    connection.commit()
    connection.close()
    return row_id


def update(statement, value):
    connection = get_sql_connection()
    cursor = connection.cursor()
    cursor.execute(statement, value)
    rows_affected = cursor.rowcount
    cursor.close()
    connection.commit()
    connection.close()
    return rows_affected


def update_many(statement, values):
    connection = get_sql_connection()
    cursor = connection.cursor()
    cursor.executemany(statement, values)
    rows_affected = cursor.rowcount
    cursor.close()
    connection.commit()
    connection.close()
    return rows_affected