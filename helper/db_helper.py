import pandas as pd
import numpy as np

## postgresql
from sqlalchemy import text
from psycopg2 import OperationalError, errorcodes, errors
from psycopg2 import extras, sql

## BigQuery
import pandas_gbq
from google.cloud import bigquery

## fix json encoder
from json import JSONEncoder
from uuid import UUID
old_default = JSONEncoder.default
def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    return old_default(self, obj)
JSONEncoder.default = new_default
## fix json encoder


from config import config
from helper import time_helper
from helper import log_helper as log
import sys, re, traceback, os

def convert_cols_to_local(df,cols_timepstamp):
    for col in cols_timepstamp:
        try:
            df[col] = df[col].dt.tz_convert(config.DWH_TIMEZONE)
            df[col] = df[col].dt.strftime(config.DWH_TIME_FORMAT)
            df[col] = pd.to_datetime(df[col],errors='coerce',utc=True,format="%Y-%m-%d %H:%M:%S")
        except:
            df[col] = None
    return df

def pii_process(info, sub_fix = 2, pre_fix = 3):
    if info is None:
        return None
    if len(info) > 4:
        return info[:sub_fix] + '*****' + info[-pre_fix:]
    else:
        return None

def print_psycopg2_exception(err):
    err_type, err_obj, traceback = sys.exc_info()
    # get the line number when exception occured
    line_num = traceback.tb_lineno
    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)
    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)
    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

def postgres_get_primary_key_of(connection, table_name = 'users',db_schema = config.DWH_DB_SCHEMA):
    # pkey_query =  f""" SELECT c.conrelid::regclass AS table_name, c.conname, pg_get_constraintdef(c.oid) constraintdef, a.attname column_name
    #     FROM pg_constraint c
    #     INNER JOIN pg_namespace n ON n.oid = c.connamespace CROSS JOIN LATERAL unnest(c.conkey) ak(k)
    #     INNER JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ak.k
    #     WHERE c.conrelid::regclass::text = '{table_name}'
    #     ORDER BY c.contype;
    # """
    pkey_query =  f""" select kcu.table_schema,
                       kcu.table_name,
                       tco.constraint_name,
                       kcu.ordinal_position as position,
                       kcu.column_name as key_column
                from information_schema.table_constraints tco
                join information_schema.key_column_usage kcu
                     on kcu.constraint_name = tco.constraint_name
                     and kcu.constraint_schema = tco.constraint_schema
                     and kcu.constraint_name = tco.constraint_name
                where tco.constraint_type = 'PRIMARY KEY'
                    AND kcu.table_name = '{table_name}'
                    AND kcu.table_schema = '{db_schema}'
                order by kcu.table_schema,
                         kcu.table_name,
                         position;
    """
    pkey = pd.read_sql(pkey_query, connection)['key_column'].values
    # pkey = " ,".join(pkey)
    return pkey

def postgres_check_table_exits(connection, table_name = 'product', db_schema = config.DWH_DB_SCHEMA):
    pkey_query =  f""" SELECT EXISTS (
           SELECT FROM information_schema.tables
           WHERE  table_schema = '{db_schema}'
           AND    table_name   = '{table_name}'
           );
    """
    pkey = pd.read_sql(pkey_query, connection)['exists'].values[0]
    # print(pkey_query,pkey)
    return pkey

def postgres_upsert(write_connection, update_data, table_name, db_schema, pk_array  =[], update_array = [],if_exists='append'):
    ## clean update_data
    # update_data = update_data.where(pd.notnull(update_data), None)
    update_data = update_data.replace({np.nan: None})

    ## Check if table exist then create if do not exists
    if if_exists == 'replace':
        if postgres_check_table_exits(write_connection, table_name = table_name, db_schema = db_schema) == False:
            update_data.to_sql(table_name, write_connection, schema = db_schema, index=False, if_exists='replace', chunksize=1000)
            ## Add primary key for new table
            pk_string = None
            if len(pk_array) > 0:
                pk_array = list(dict.fromkeys(pk_array))
                pk_string = ", ".join(pk_array)
            else:
                if 'id' in update_data.columns:
                    pk_string = 'id'
            if len(pk_string) > 0:
                execute_query = f'ALTER TABLE "{db_schema}"."{table_name}" ADD PRIMARY KEY ({pk_string});'
                write_connection.execute(text(execute_query))
            # write_connection.execute()
            return

    ## Insert and Update row
    fields = ", ".join(update_data.columns)

    if len(update_array) == 0:
        excluded_fields = 'EXCLUDED.' + ", EXCLUDED.".join(update_data.columns)
        update_array = fields
    else:
        excluded_fields = 'EXCLUDED.' + ", EXCLUDED.".join(update_array)
        update_array = ", ".join(update_array)

    if update_array == False:
        sql_string = f"INSERT INTO {db_schema}.{table_name} ({fields}) VALUES %s ON CONFLICT ({pk_array}) DO NOTHING  "
    elif len(pk_array) == 0:
        excluded_fields = 'EXCLUDED.' + ", EXCLUDED.".join(update_data.columns)
        update_array = fields
        sql_string = f"INSERT INTO {db_schema}.{table_name} ({fields}) VALUES %s ON CONFLICT (id) DO UPDATE SET ({update_array}) = ({excluded_fields})"
    else:
        pk_array = list(dict.fromkeys(pk_array))
        pk_array = ' ,'.join(pk_array)
        sql_string = f"INSERT INTO {db_schema}.{table_name} ({fields}) VALUES %s ON CONFLICT ({pk_array}) DO UPDATE SET ({update_array}) = ({excluded_fields})"

    raw_connection = write_connection.raw_connection()
    cursor = raw_connection.cursor()

    rows_data = [list(row) for row in update_data.itertuples(index=False)]

    # query = sql.SQL(sql_string)
    # extras.execute_values(cursor, sql.SQL(sql_string).as_string(cursor), rows_data, page_size=100)
    try:
        extras.execute_values(cursor, sql.SQL(sql_string).as_string(cursor), rows_data, page_size=100)
        raw_connection.commit()
        raw_connection.close()
    except Exception as err:
        raw_connection.rollback()
        raw_connection.close()
        print(sql_string,err)
        return False
        # print_psycopg2_exception(err)

def postgres_alter_table_check(connection, data, table_name, db_schema = 'public', data_type_array = []):
    table_struct_query = f"""     SELECT table_schema, table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = '{db_schema}' and table_name = '{table_name}'
    """
    table_struct = pd.read_sql(table_struct_query,connection)
    if table_struct is None or table_struct.shape[0] == 0:
        print(f"Table '{table_name}' does not exist in schema '{db_schema}'")

        return True
    for col in data.columns:
        if table_struct[table_struct['column_name'] == col].shape[0] == 0:
            data_type = dict(data.dtypes)[col]
            if str(data_type) == "object":
                data_type = 'TEXT'
            for dt in data_type_array:
                if dt['col'] == col:
                    data_type = dt['data_type']
                    break
            alter_query = f'''ALTER TABLE {db_schema}.{table_name} ADD COLUMN {col} {data_type} '''
            connection.execute(alter_query)
    # postgres_upsert(connection, data, table_name, db_schema)
    return True

def bigquery_execute(query):
    client = bigquery.Client()
    query_job = client.query(query)
    results = query_job.result()
    return results

def bigquery_upsert(bq_connection, update_data, table_name, db_schema, pk_array  =[], update_array = [], if_exists='append'):
    if update_data is None or update_data.shape[0] == 0:
        return "Empty DataFrame"

    table_id = '{dataset}.{table}'.format(dataset=db_schema,table=table_name)
    project_id=bq_connection['project_id']

    # table_schema:list of dicts, optional
    # https://pandas-gbq.readthedocs.io/en/latest/api.html#pandas_gbq.to_gbq
    key = update_data[pk_array].copy()
    for c in key.columns:
        key[c] = key[c].apply(str)

    update_data['insertID'] = key.agg('-'.join, axis=1)
    update_data['loadTime'] = time_helper.get_now()

    try:
        update_data=update_data.dropna(axis=1,how='all')

        for c in update_data.columns:
            type = str(update_data[c].dtypes)
            if type  == 'object':
                update_data[c] = update_data[c].astype("string")

        pandas_gbq.to_gbq(update_data,destination_table=table_id, project_id=project_id,chunksize=50000,if_exists=if_exists,progress_bar=True)

        # table = client.get_table(table_id)
        # errors = client.insert_rows_from_dataframe(table, update_data)
        # if len(errors) > 0:
        #     for chunk in errors:
        #         print(f"encountered {len(chunk)} errors: {chunk}")

        ## Deduplicate
        if if_exists == 'append':
            deduplicate_query = f"""
                DELETE FROM `{project_id}.{table_id}`
                    WHERE STRUCT(insertID, loadTime) NOT IN (
                            SELECT AS STRUCT insertID, MAX(loadTime) loadTime
                            FROM `{project_id}.{table_id}`
                            GROUP BY insertID)
            """
            bigquery_execute(deduplicate_query)
    except Exception as e:
        exception_message = project_id + '.' + table_id + ' ' + str(e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[1]
        detail={'exception_message':exception_message,"exception_type":str(exception_type)
            ,"filename":str(filename),'line':str(exception_traceback.tb_lineno)
            ,"log_message":f"{exception_type} {exception_message} '{filename}', Line {exception_traceback.tb_lineno}"}
        log.error(name="BigQuery Update",action=exception_message,detail=detail)



def upsert(connection, update_data, table_name, db_schema = 'public', pk_array = [], update_array = [],if_exists='append'):
    if connection['driver'] == 'bigquery':
        bigquery_upsert(bq_connection = connection
               , update_data = update_data
               , table_name = table_name
               , db_schema = db_schema
               , pk_array = pk_array
               , update_array = update_array
               , if_exists = if_exists
            )
    elif connection['driver'] == 'psycopg2':
        return postgres_upsert(write_connection = connection['engine']
               , update_data = update_data
               , table_name = table_name
               , db_schema = db_schema
               , pk_array = pk_array
               , update_array = update_array
               , if_exists = if_exists
           )


def alter_table_check(connection,data, table_name, db_schema = 'public', data_type_array = []):
    if connection['driver'] == 'psycopg2':
         postgres_alter_table_check(connection = connection['engine']
            , data = data
            , table_name = table_name
            , db_schema = db_schema
            , data_type_array =  data_type_array
            )
