import json

import pandas as pd

from service.util.db_utils import get_db_connection, close_db_connection
from service.util.unify_logger import unify_printer


def execute_query(db_name, host, port, user, password, query, database):
    try:
        con = get_db_connection(db_name, host, port, user, password, database)
        # cur = con.cursor()
        # cur.execute(query)
        # for row in cur:
        #     ""

        # rows = cur.fetchall()
        # rows = rows.to_json()
        # rows = json.loads(rows)
        rows = pd.read_sql(query, con)

    except Exception as ex:
        raise
    finally:
        close_db_connection(con)
    return rows


def process_mssql_query(db_name, host, port, user, password, query, database):
    try:
        con = get_db_connection(db_name, host, port, user, password, database)
        # cur = con.cursor()
        # cur.execute(query)
        # for row in cur:
        #     ""
        rows = pd.read_sql(query, con)
        # rows = cur.fetchall()
        # rows = rows.to_json()
        # rows = json.loads(rows)
    except Exception as ex:
        raise
    finally:
        close_db_connection(con)
    return rows


def get_mssql_table_describe(db_name, host, port, user, password, query, database, schema=None):
    try:
        con = get_db_connection(db_name, host, port, user, password, database)
        cur = con.cursor()
        if schema:
            cur.execute("SET SCHEMA '{}'".format(schema))
        # if 'LIMIT' not in query.upper():
        #     query = f'{query} limit 1'
        # cur.execute(query)
        # for row in cur:
        #     ""
        # rows = cur.fetchall()
        rows = pd.read_sql(query, con).to_json(orient='records', date_format='iso')
        rows = json.loads(rows)
    except Exception as ex:
        raise
    finally:
        close_db_connection(con)
    return rows


def get_meta_info(meta_data, host, port, user, password, database=None):
    try:
        condition = meta_data.replace('DATABASE', 'lower(table_catalog)').replace('TABLE', 'lower(table_name)') \
            .replace('SCHEMA', 'lower(table_schema)').replace("COLUMN", 'lower(column_name)')
        query = f'select table_catalog as database, table_schema as schema, table_name as table, column_name as ' \
                f'column from information_schema.columns where {condition} '

        con = get_db_connection('MSSQL', host, port, user, password, database)
        unify_printer(message=f"Meta search query: {query}")
        rows_df = pd.read_sql(query, con)
    except Exception as ex:
        raise
    finally:
        close_db_connection(con)
    return rows_df
