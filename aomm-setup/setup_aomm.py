import psycopg2
from psycopg2 import OperationalError
import csv

from functools import lru_cache
import app_config
from app_config import setenv

setenv()

@lru_cache
def get_settings():
    return app_config.Settings()

#Connect DB server and database
# def connect_postgres_db():
#     """create dna postgres DB connection"""
#     try:
#         print('database=',"postgres",
#             'user=',"postgres",
#             'password=',get_settings().postgres_password,
#             'host=',get_settings().db_host,
#             'port=',get_settings().db_port)
#         conn = psycopg2.connect(
#             database="postgres",
#             user="postgres",
#             password=get_settings().postgres_password,
#             host=get_settings().db_host,
#             port=get_settings().db_port
#         )       
#         return conn
#     except Exception as e:
#         print("Error connecting to the database:", e)
#         return None

#Connect DB server and database
def connect_aomm_db():
    """create dna postgres DB connection"""
    try:
        conn = psycopg2.connect(
            database="aomm_data",
            user="aomm_data",
            password="J6FJd85WgTa2Xptg",
            host=get_settings().db_host,
            port=get_settings().db_port
        )       
        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

# def executeScriptsFromFile(filename, c):
#     # Open and read the file as a single buffer
#     fd = open(filename, 'r')
#     sqlFile = fd.read()
#     fd.close()

#     # all SQL commands (split on ';')
#     sqlCommands = sqlFile.split(';')

#     # Execute every command from the input file
#     for command in sqlCommands:
#         # This will skip and report errors
#         # For example, if the tables do not yet exist, this will skip over
#         # the DROP TABLE commands
#         try:
#             if not command.startswith("--") and len(command)>12:
#                 print(command)
#                 c.execute(command)
#             else:
#                 print(command)
#         except OperationalError as oe:
#             print("Command skipped: ", oe)



# connect_postgres = connect_postgres_db()
# cursor_postgres = connect_postgres.cursor()

ROOT_PATH = get_settings().root_path

# executeScriptsFromFile(ROOT_PATH + "postgres/setup_db.sql", cursor_postgres)
# executeScriptsFromFile(ROOT_PATH + "postgres/setup_schema.sql", cursor_postgres)

# cursor_postgres.close()
# connect_postgres.close()

conn = connect_aomm_db()
cursor = conn.cursor()  

queries = [
    {"file":"sub_dimension.csv", "params":4, "sql":"INSERT INTO sub_dimension (sub_dimension_id, sub_dimension_name, sub_dimension_definition, sub_dimension_context, dimension) "},
    {"file":"criteria.csv", "params":3, "sql":"INSERT INTO criteria (criteria_id, criteria_scope, criteria_description, sub_dimension_id) "},
    {"file":"attribute.csv", "params":11, "sql":"INSERT INTO attribute (attribute_id, attribute_id_level1, attribute_level1, attribute_id_level2, attribute_level2, attribute_id_level3, attribute_level3, attribute_id_level4, attribute_level4, attribute_id_level5, attribute_level5, criteria_id) "},
    {"file":"value_stream.csv", "params":3, "sql":"INSERT INTO value_stream (value_stream_id, value_stream_name, operation, operation_sub_group) "}, 
    {"file":"capability.csv", "params":5, "sql":"INSERT INTO capability (capability_id, capability_name, capability_definition, weighting, value_stream_id, sub_dimension_id) "}, 
    {"file":"question.csv", "params":2, "sql":"INSERT INTO question (question_id, question_description, criteria_id) "}, 
    {"file":"capability_question_relation.csv", "params":1, "sql":"INSERT INTO capability_question_relation (capability_id, question_id) "}, 
    {"file":"cla.csv", "params":12, "sql":"INSERT INTO cla (cla_id, cla_level1_id, cla_level1_description, cla_level2_id, cla_level2_description, cla_level3_id, cla_level3_description, cla_level4_id, cla_level4_description, cla_level5_id, cla_level5_description, question_id, criteria_id) "} 
]

#insert_row = tuple()
try:
    for query in queries:   
        #open the csv file
        CSV_FILE : str = query["file"]
        NUM_PARAMS : int = query["params"]
        SQL_INSERT : str = query["sql"]
        cnt = 0
        with open(ROOT_PATH + CSV_FILE, mode='r', encoding='unicode_escape') as csv_file:
            #read csv using reader class
            csv_reader = csv.reader(csv_file)
            #skip header
            header = next(csv_reader)
            #Read csv row wise and insert into table
            for row in csv_reader:
                sql= SQL_INSERT
                sql+= 'VALUES (%s'
                sql+= ',%s'*NUM_PARAMS
                sql+= ')'
                cursor.execute(sql, tuple(row))
                #print(cnt)
                #print(tuple(row))
                #insert_row = tuple(row)
                cnt=cnt+1
        print("Records inserted", CSV_FILE, " :  ", cnt)
    conn.commit()
    cursor.close()
except IndexError as ie:
    #print("Error: ", str(ie), CSV_FILE, insert_row, cnt)
    print("Error: ", str(ie), CSV_FILE, cnt)