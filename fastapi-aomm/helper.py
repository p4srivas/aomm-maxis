# type: ignore
import psycopg2
import pandas as pd
from decimal import Decimal
# Plotly Express
import plotly.express as px

from models import UserSchema, UserLogin, User, Base
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT, decodeJWT

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from database import engine, get_db

import hashlib
from datetime import datetime, timezone
import uuid

from functools import lru_cache
from app_config import service_dict, dimension_dict, sub_dimension_dict, operation_dict, operation_sub_group_dict
import app_config

@lru_cache
def get_settings():
    return app_config.Settings()

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    # return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    #print("plain_password", plain_password, "hashed_password", hash_password(plain_password), "database", hashed_password)
    return hash_password(plain_password) == hashed_password

async def get_user_by_email(db: AsyncSession, email: str):
    """Retrieve a user by email"""
    #print("user_email",email)
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

# Database connection
def connect_db():
    """create postgres DB connection"""
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


@lru_cache
def get_settings():
    return app_config.Settings()

def populate_operation_dict():
    conn = connect_db()
    cur = conn.cursor() 
    query = "SELECT operation_id, operation_name FROM operation_map;"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return dict(rows)

def populate_operation_sub_group_dict():
    conn = connect_db()
    cur = conn.cursor() 
    query = "SELECT operation_sub_group_id, operation_sub_group_name FROM operation_sub_group_map;"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return dict(rows)

#operation_dict = populate_operation_dict()
#operation_sub_group_dict = populate_operation_sub_group_dict()

def get_display_values(service, operation, operation_sub_group):
    return {'service':service_dict[service], 'operation':operation_dict[operation], 'operation_sub_group':operation_sub_group_dict[operation_sub_group]}

def get_display_text(dimension, sub_dimension):
    return {'dimension':dimension_dict[dimension], 'sub_dimension':sub_dimension_dict[sub_dimension]}

def get_user_role_by_session_id(user_id):
    conn = connect_db()
    cur = conn.cursor() 
    query = "SELECT role FROM public.user WHERE UPPER(user_id) = UPPER('" + user_id + "');"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()
    cur.close()
    conn.close()
    user_role = "user"
    for row in rows:
        user_role = row[0]
    
    #   print(user_role)
    return user_role


def get_capbilities(service, operation, operation_sub_group):
    conn = connect_db()
    cur = conn.cursor() 

    capability_data = list()

    query = "SELECT value_stream_id, value_stream_name FROM value_stream WHERE operation_sub_group = '" + operation_sub_group + "' ORDER BY value_stream_id ASC;"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows_vs = cur.fetchall()
    
    for row_vs in rows_vs:
        query = """SELECT 
                    t3.capability_id AS capability_id,
                    t3.capability_name AS capability_name,
                    t3.capability_definition AS capability_definition,
                    t.question_id AS question_id, 
                    t2.criteria_scope AS question_scope,
                    t1.question_description AS question_description,
                    t3.weighting AS weighting, 
                    t.cla_level1_id, t.cla_level1_description,
                    t.cla_level2_id, t.cla_level2_description,
                    t.cla_level3_id, t.cla_level3_description,
                    t.cla_level4_id, t.cla_level4_description,
                    t.cla_level5_id, t.cla_level5_description
                FROM cla t
                INNER JOIN question t1 ON t1.question_id = t.question_id 
                INNER JOIN criteria t2 ON t2.criteria_id = t1.criteria_id 
                INNER JOIN capability_question_relation t4 ON t4.question_id = t1.question_id  
                INNER JOIN capability t3 ON t3.capability_id = t4.capability_id 
                WHERE t3.value_stream_id = '"""
        query+= row_vs[0]
        query+= "' ORDER BY t3.capability_id, t1.question_id ASC;"
        cur.execute(query)
        # Fetch all rows as a list of tuples
        rows = cur.fetchall()

        #i is keys for dict 
        i = [
            'capability_id', 'capability_name', 'capability_definition', 'question_id', 'question_scope','question_description', 'weighting',
            'cla_level1_id', 'cla_level1_description', 'cla_level2_id', 'cla_level2_description', 'cla_level3_id', 'cla_level3_description',
            'cla_level4_id', 'cla_level4_description', 'cla_level5_id', 'cla_level5_description'
        ]
        show_vs = True
        #each j is the row value
        for j in rows:
            if show_vs:
                capability_data.append(
                    {
                        "value_stream_id":row_vs[0], "value_stream_name":row_vs[1], i[0]:j[0], i[1]:j[1], i[2]:j[2], i[3]:j[3], i[4]:j[4], i[5]:j[5], i[6]:j[6], 
                        i[7]:str(j[7]), i[8]:j[8], i[9]:j[9], i[10]:j[10], i[11]:j[11], i[12]:j[12], 
                        i[13]:j[13], i[14]:j[14], i[15]:j[15], i[16]:j[16]
                    }
                )
            else:
                capability_data.append(
                    {
                        "value_stream_id":row_vs[0], "value_stream_name":"", i[0]:j[0], i[1]:j[1], i[2]:j[2], i[3]:j[3], i[4]:j[4], i[5]:j[5], i[6]:j[6], 
                        i[7]:str(j[7]), i[8]:j[8], i[9]:j[9], i[10]:j[10], i[11]:j[11], i[12]:j[12], 
                        i[13]:j[13], i[14]:j[14], i[15]:j[15], i[16]:j[16]
                    }
                )                
            show_vs = False

    cur.close()
    conn.close()

    return capability_data 

def insert_update_user_response(
                                user_id, service, operation, operation_sub_group, 
                                no_of_capabilities, user_response):
    conn = connect_db()
    cur = conn.cursor() 
    self_assessment_id = str(uuid.uuid4())
    dt = datetime.now(timezone.utc)
    cur.execute("INSERT INTO self_assessment (self_assessment_id, creation_time, update_time, user_id, service, operation, operation_sub_group, is_archived) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (self_assessment_id, dt, dt, user_id, service_dict[service], operation, operation_sub_group, 'f'))
    conn.commit()

    for item in user_response:
        cla_response_list = item.split('_', 5)
        value_stream_id = cla_response_list[0]
        weighting = cla_response_list[1]
        capability_id = cla_response_list[2]
        question_id = cla_response_list[3]
        selected_cla_level_id = cla_response_list[4]
        cla_level = selected_cla_level_id.split('.')[3]
        criteria_id = question_id
        sub_dimension_id = criteria_id.split('.')[0]+'.'+criteria_id.split('.')[1]
        capability_score = int(cla_level)
        insertQuery = """INSERT INTO sa_question_relation 
                        (self_assessment_id, question_id, weighting, selected_cla_level_id, cla_level, 
                        capability_id, value_stream_id, criteria_id, sub_dimension_id, capability_score, is_archived) VALUES """
        cur.execute(insertQuery + "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                    (self_assessment_id, question_id, weighting, selected_cla_level_id, cla_level, capability_id, value_stream_id, criteria_id, sub_dimension_id, capability_score, 'f'))
        conn.commit()        

    cur.close()
    conn.close()    
    return self_assessment_id 

def get_capbilities_for_user_response(user_id, service, operation, operation_sub_group):
    conn = connect_db()
    cur = conn.cursor() 

    capability_data = list()

    query = """SELECT t1.value_stream_id AS value_stream_id, 
                    t1.value_stream_name AS value_stream_name,
                    t.self_assessment_id
                FROM self_assessment t
                INNER JOIN sa_question_relation t2 ON t2.self_assessment_id = t.self_assessment_id 
                INNER JOIN value_stream t1 ON t1.value_stream_id = t2.value_stream_id
                WHERE t.self_assessment_id = (SELECT self_assessment_id FROM self_assessment WHERE 
                operation_sub_group = '"""
    query+= operation_sub_group
    query+= "' AND operation = '" + operation 
    query+= "' AND service = '" + service_dict[service]
    query+= "' AND UPPER(user_id) = UPPER('" + user_id
    query+= "') AND is_archived = 'f' ORDER BY update_time DESC LIMIT 1)"
    query+= "  GROUP BY t1.value_stream_id, t1.value_stream_name, t.self_assessment_id"
    query+= "  ORDER BY t1.value_stream_id ASC;"    
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows_vs = cur.fetchall()

    for row_vs in rows_vs:

        query = """SELECT 
                        t4.capability_id AS capability_id,
                        t4.capability_name AS capability_name,
                        t4.capability_definition AS capability_definition,
                        t2.question_id AS question_id, 
                        t3.criteria_scope AS question_scope, 
                        t2.question_description AS question_description, 
                        t4.weighting AS weighting,                    
                        t1.cla_level1_id, t1.cla_level1_description,
                        t1.cla_level2_id, t1.cla_level2_description,
                        t1.cla_level3_id, t1.cla_level3_description,
                        t1.cla_level4_id, t1.cla_level4_description,
                        t1.cla_level5_id, t1.cla_level5_description,
                        t.cla_level, t.capability_score 
                    FROM sa_question_relation t
                    INNER JOIN cla t1 ON t1.question_id = t.question_id
                    INNER JOIN question t2 ON t2.question_id = t.question_id 
                    INNER JOIN criteria t3 ON t3.criteria_id = t2.criteria_id 
                    INNER JOIN capability t4 ON t4.capability_id = t.capability_id 
                    WHERE t.self_assessment_id = '"""
        query+= row_vs[2] + "'"
        query+= "  AND t.value_stream_id = '" + row_vs[0] + "'"
        query+= "  ORDER BY t4.capability_id, t2.question_id ASC;"
        cur.execute(query)
        # Fetch all rows as a list of tuples
        rows = cur.fetchall()

        show_vs = True

        #i is keys for dict 
        i = [
            'capability_id', 'capability_name', 'capability_definition', 'question_id', 'question_scope', 'question_description', 'weighting',
            'cla_level1_id', 'cla_level1_description', 'cla_level2_id', 'cla_level2_description', 'cla_level3_id', 'cla_level3_description',
            'cla_level4_id', 'cla_level4_description', 'cla_level5_id', 'cla_level5_description', 'cla_level', 'capability_score'
        ]

        #each j is the row value
        for j in rows:
            if show_vs:
                capability_data.append(
                    {
                        'value_stream_id':row_vs[0], 'value_stream_name':row_vs[1], i[0]:j[0], i[1]:j[1], i[2]:j[2], i[3]:j[3], i[4]:j[4], i[5]:j[5], i[6]:j[6], 
                        i[7]:str(j[7]), i[8]:j[8], i[9]:j[9], i[10]:j[10], i[11]:j[11], i[12]:j[12],
                        i[13]:j[13], i[14]:j[14], i[15]:j[15], i[16]:j[16], i[17]:j[17], i[18]:j[18] 
                    }
                )
            else:
                capability_data.append(
                    {
                        'value_stream_id':row_vs[0], 'value_stream_name':"", i[0]:j[0], i[1]:j[1], i[2]:j[2], i[3]:j[3], i[4]:j[4], i[5]:j[5], i[6]:j[6], 
                        i[7]:str(j[7]), i[8]:j[8], i[9]:j[9], i[10]:j[10], i[11]:j[11], i[12]:j[12], 
                        i[13]:j[13], i[14]:j[14], i[15]:j[15], i[16]:j[16], i[17]:j[17], i[18]:j[18] 
                    }
                )
            show_vs = False
            
    cur.close()
    conn.close()

    return capability_data 

def get_dashboard_index_table(service, operation, operation_sub_group):
    conn = connect_db()
    cur = conn.cursor() 

    # query = """SELECT 
    #                 value_stream_id AS value_stream_id,
    #                 value_stream_name AS value_stream_name
    #             FROM value_stream
    #             WHERE operation_sub_group = '"""
    # query+= operation_sub_group
    # query+= "' ORDER BY value_stream_id ASC;"
    # cur.execute(query)
    # # Fetch all rows as a list of tuples
    # rows = cur.fetchall()

    # # Create DataFrame from the list of tuples
    # df1 = pd.DataFrame(rows, columns=[
    #                                     'Id', 'Name'
    #                                 ])

    query = """SELECT 
                    t.capability_id AS capability_id,
                    t.capability_name AS capability_name
                FROM capability t 
                INNER JOIN value_stream t1 ON t1.value_stream_id = t.value_stream_id 
                AND t1.operation_sub_group = '"""
    query+= operation_sub_group
    query+= "' ORDER BY t.capability_id ASC;"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()

    # Create DataFrame from the list of tuples
    df2 = pd.DataFrame(rows, columns=[
                                        'Id', 'Name'
                                    ])

    cur.close()
    conn.close()

    #return pd.concat([df1, df2])
    return df2

def get_user_capability_scores(user_id, service, operation, operation_sub_group, is_admin):
    conn = connect_db()
    cur = conn.cursor() 

    df = None

    if is_admin:
        query = """SELECT 
                        t2.capability_id AS capability_id,
                        t.user_id AS comparison,
                        t1.capability_score::INT AS score 
                    FROM self_assessment t
                    INNER JOIN sa_question_relation t1 ON t1.self_assessment_id = t.self_assessment_id AND t1.is_archived = 'f' 
                    INNER JOIN capability t2 ON t2.capability_id = t1.capability_id 
                    WHERE t.self_assessment_id = (SELECT self_assessment_id FROM self_assessment WHERE 
                        operation_sub_group = '"""
        query+= operation_sub_group
        query+= "' AND operation = '" + operation 
        query+= "' AND service = '" + service_dict[service]
        query+= "' AND UPPER(user_id) = UPPER('" + user_id
        query+= "') AND is_archived = 'f' ORDER BY update_time DESC LIMIT 1)"
        query+= "  ORDER BY t2.capability_id ASC;"

        cur.execute(query)
        # Fetch all rows as a list of tuples
        rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=["capability_id", "comparison", "score"])
    else:
        query = """SELECT 
                        t2.capability_id AS capability_id,
                        t1.capability_score::INT AS score 
                    FROM self_assessment t
                    INNER JOIN sa_question_relation t1 ON t1.self_assessment_id = t.self_assessment_id AND t1.is_archived = 'f' 
                    INNER JOIN capability t2 ON t2.capability_id = t1.capability_id 
                    WHERE t.self_assessment_id = (SELECT self_assessment_id FROM self_assessment WHERE 
                        operation_sub_group = '"""
        query+= operation_sub_group
        query+= "' AND operation = '" + operation 
        query+= "' AND service = '" + service_dict[service]
        query+= "' AND UPPER(user_id) = UPPER('" + user_id
        query+= "') AND is_archived = 'f' ORDER BY update_time DESC LIMIT 1)"
        query+= "  ORDER BY t2.capability_id ASC;"

        cur.execute(query)
        # Fetch all rows as a list of tuples
        rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=["capability_id", "score"])

    cur.close()
    conn.close()


    return df

def get_average_capability_scores(service, operation, operation_sub_group):
    conn = connect_db()
    cur = conn.cursor() 

    query = """SELECT 
                    t2.capability_id AS capability_id,
                    'average' AS comparison,
                    AVG(t1.capability_score::INT)::NUMERIC(5,2) AS score  
                FROM self_assessment t
                INNER JOIN sa_question_relation t1 ON t1.self_assessment_id = t.self_assessment_id AND t1.is_archived = 'f' 
                INNER JOIN capability t2 ON t2.capability_id = t1.capability_id 
                WHERE t.self_assessment_id IN (SELECT self_assessment_id FROM self_assessment WHERE 
                    operation_sub_group = '"""
    query+= operation_sub_group
    query+= "' AND operation = '" + operation 
    query+= "' AND service = '" + service_dict[service]
    query+= "' AND is_archived = 'f')"
    query+= "  GROUP BY t2.capability_id "
    query+= "  ORDER BY t2.capability_id ASC;"

    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()

    cur.close()
    conn.close()

    df = pd.DataFrame(rows, columns=["capability_id", "comparison", "score"])

    return df

def get_user_value_stream_scores(user_id, service, operation, operation_sub_group, is_admin):
    conn = connect_db()
    cur = conn.cursor() 

    df = None

    if is_admin:
        query = """SELECT 
                        t2.value_stream_id AS value_stream_id,
                        t.user_id AS comparison,
                        SUM(t1.capability_score*t1.weighting/100)::NUMERIC(5,2) AS score 
                    FROM self_assessment t
                    INNER JOIN sa_question_relation t1 ON t1.self_assessment_id = t.self_assessment_id AND t1.is_archived = 'f' 
                    INNER JOIN value_stream t2 ON t2.value_stream_id = t1.value_stream_id  
                    WHERE t.self_assessment_id = (SELECT self_assessment_id FROM self_assessment WHERE 
                        operation_sub_group = '"""
        query+= operation_sub_group
        query+= "' AND operation = '" + operation 
        query+= "' AND service = '" + service_dict[service]
        query+= "' AND UPPER(user_id) = UPPER('" + user_id
        query+= "') AND is_archived = 'f' ORDER BY update_time DESC LIMIT 1)"
        query+= "  GROUP BY t2.value_stream_id, t.user_id"
        query+= "  ORDER BY t2.value_stream_id ASC;"

        cur.execute(query)
        # Fetch all rows as a list of tuples
        rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=["value_stream_id", "comparison", "score"])
    else:
        query = """SELECT 
                        t2.value_stream_id AS value_stream_id,
                        SUM(t1.capability_score*t1.weighting/100)::NUMERIC(5,2) AS score 
                    FROM self_assessment t
                    INNER JOIN sa_question_relation t1 ON t1.self_assessment_id = t.self_assessment_id AND t1.is_archived = 'f' 
                    INNER JOIN value_stream t2 ON t2.value_stream_id = t1.value_stream_id  
                    WHERE t.self_assessment_id = (SELECT self_assessment_id FROM self_assessment WHERE 
                        operation_sub_group = '"""
        query+= operation_sub_group
        query+= "' AND operation = '" + operation 
        query+= "' AND service = '" + service_dict[service]
        query+= "' AND UPPER(user_id) = UPPER('" + user_id
        query+= "') AND is_archived = 'f' ORDER BY update_time DESC LIMIT 1)"
        query+= "  GROUP BY t2.value_stream_id, t.user_id"
        query+= "  ORDER BY t2.value_stream_id ASC;"

        cur.execute(query)
        # Fetch all rows as a list of tuples
        rows = cur.fetchall()

        df = pd.DataFrame(rows, columns=["value_stream_id", "score"])


    cur.close()
    conn.close()
    return df

def get_average_value_stream_scores(service, operation, operation_sub_group):
    conn = connect_db()
    cur = conn.cursor() 

    query = """SELECT 
                    t2.value_stream_id AS value_stream_id,
                    'average' AS comparison,
                    ((SUM(t1.capability_score*t1.weighting/100))/ 
                    (SELECT count(self_assessment_id) FROM self_assessment WHERE operation_sub_group = '"""
    query+= operation_sub_group
    query+= "' AND operation = '" + operation 
    query+= "' AND service = '" + service_dict[service]
    query+= "' AND is_archived = 'f'))::NUMERIC(5,3) AS score" 
    query+= " FROM self_assessment t"
    query+= " INNER JOIN sa_question_relation t1 ON t1.self_assessment_id = t.self_assessment_id AND t1.is_archived = 'f'"
    query+= " INNER JOIN value_stream t2 ON t2.value_stream_id = t1.value_stream_id"
    query+= " WHERE t.self_assessment_id IN (SELECT self_assessment_id FROM self_assessment WHERE" 
    query+= " operation_sub_group = '"
    query+= operation_sub_group
    query+= "' AND operation = '" + operation 
    query+= "' AND service = '" + service_dict[service]
    query+= "' AND is_archived = 'f')"
    query+= "  GROUP BY t2.value_stream_id "
    query+= "  ORDER BY t2.value_stream_id ASC;"


    # query = """SELECT 
    #                 t2.value_stream_id AS value_stream_id,
    #                 'average' AS comparison,
    #                 AVG(t1.capability_score)::NUMERIC(5,3) AS score 
    #             FROM self_assessment t
    #             INNER JOIN sa_question_relation t1 ON t1.self_assessment_id = t.self_assessment_id AND t1.is_archived = 'f' 
    #             INNER JOIN value_stream t2 ON t2.value_stream_id = t1.value_stream_id  
    #             WHERE t.self_assessment_id IN (SELECT self_assessment_id FROM self_assessment WHERE 
    #                 operation_sub_group = '"""
    # query+= operation_sub_group
    # query+= "' AND operation = '" + operation 
    # query+= "' AND service = '" + service_dict[service]
    # query+= "' AND is_archived = 'f')"
    # query+= "  GROUP BY t2.value_stream_id "
    # query+= "  ORDER BY t2.value_stream_id ASC;"

    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()

    cur.close()
    conn.close()      

    df = pd.DataFrame(rows, columns=["value_stream_id", "comparison", "score"])

    return df

def get_dashboard_graphs(user_id, service, operation, operation_sub_group): 
    role = get_user_role_by_session_id(user_id)
    df1 = pd.DataFrame({
                        "value_stream_id": ["6.1", "6.2", "6.3", "6.1", "6.2", "6.3"],
                        "comparison": ["user", "user", "user", "average", "average", "average"],
                        "score": [2, 1, 3, 1.4, 3.1, 2.5],
                    })
    fig1 = px.bar(df1, x="value_stream_id", y="score", color="comparison", barmode="group")
    if role == "admin":
        df1 = pd.concat([get_user_value_stream_scores(user_id, service, operation, operation_sub_group, True), get_average_value_stream_scores(service, operation, operation_sub_group)], axis=0, join='outer', ignore_index=True) 
        fig1 = px.bar(df1, x="value_stream_id", y="score", color="comparison", barmode="group")
        # Increase the height of the graph
        if df1.shape[0] and df1.shape[0] > 4 and df1.shape[0] < 9:
            fig1.update_layout(height=360, width=df1.shape[0]*100)
        elif df1.shape[0] and df1.shape[0] < 5:
            fig1.update_layout(height=360, width=df1.shape[0]*160)
        else:    
            fig1.update_layout(height=360, width=460)
    else:
        df1 = get_user_value_stream_scores(user_id, service, operation, operation_sub_group, False)
        fig1 = px.bar(df1, x="value_stream_id", y="score")
        # Increase the height of the graph
        if df1.shape[0] and df1.shape[0] > 2 and df1.shape[0] < 5:
            fig1.update_layout(height=360, width=df1.shape[0]*100)
        elif df1.shape[0] and df1.shape[0] < 3:
            fig1.update_layout(height=360, width=df1.shape[0]*160)
        else:    
            fig1.update_layout(height=360, width=460)
    #print(df1.shape)
    #print(df1.columns)
    
    fig1.update_layout(yaxis_range=[0,5.0])
    fig1.update_layout(showlegend=True)

    df2 = pd.DataFrame({
                        "capability_id": ["6.1.1", "6.2.2", "6.3.1", "6.1.3", "6.2.3", "6.3.2", "6.1.1", "6.2.2", "6.3.1", "6.1.3", "6.2.3", "6.3.2"],
                        "comparison": ["user", "user", "user", "user", "user", "user", "average", "average", "average", "average", "average", "average"],
                        "score": [2, 1, 3, 2, 1, 3, 1.4, 3.1, 2.5, 1.4, 3.1, 2.5]
                    })
    fig2 = px.bar(df2, x="capability_id", y="score", color="comparison", barmode="group")
    if role == "admin":
        df2 = pd.concat([get_user_capability_scores(user_id, service, operation, operation_sub_group, True), get_average_capability_scores(service, operation, operation_sub_group)], axis=0, join='outer', ignore_index=True)
        fig2 = px.bar(df2, x="capability_id", y="score", color="comparison", barmode="group")
        # Increase the height of the graph
        if df2.shape[0] and df2.shape[0] > 8 and df2.shape[0] < 15:
            fig2.update_layout(height=360, width=df2.shape[0]*50)
        elif df2.shape[0] and df2.shape[0] < 9:
            fig2.update_layout(height=360, width=df2.shape[0]*80)
        else:
            fig2.update_layout(height=360, width=960)
    else:
        df2 = get_user_capability_scores(user_id, service, operation, operation_sub_group, False)
        fig2 = px.bar(df2, x="capability_id", y="score")
        if df2.shape[0] and df2.shape[0] > 4 and df2.shape[0] < 7:
            fig2.update_layout(height=360, width=df2.shape[0]*50)
        elif df2.shape[0] and df2.shape[0] < 5:
            fig2.update_layout(height=360, width=df2.shape[0]*80)
        else:
            fig2.update_layout(height=360, width=960)

    #print(df2.shape)
    #print(df2.columns)
    
    fig2.update_layout(yaxis_range=[0,5.0])
    fig2.update_layout(showlegend=False)

    return fig1, fig2

def get_autotext(user_id, service, operation, operation_sub_group):
    conn = connect_db()
    cur = conn.cursor() 
    query = """SELECT 
                    t2.value_stream_id AS value_stream_id,
                    t2.value_stream_name AS value_stream_name,
                    SUM(t1.capability_score*t1.weighting/100)::NUMERIC(5,2) AS score 
                FROM self_assessment t
                INNER JOIN sa_question_relation t1 ON t1.self_assessment_id = t.self_assessment_id AND t1.is_archived = 'f' 
                INNER JOIN value_stream t2 ON t2.value_stream_id = t1.value_stream_id  
                WHERE t.self_assessment_id = (SELECT self_assessment_id FROM self_assessment WHERE 
                    operation_sub_group = '"""
    query+= operation_sub_group
    query+= "' AND operation = '" + operation 
    query+= "' AND service = '" + service_dict[service]
    query+= "' AND UPPER(user_id) = UPPER('" + user_id
    query+= "') AND is_archived = 'f' ORDER BY update_time DESC LIMIT 1)"
    query+= "  GROUP BY t2.value_stream_id, t.user_id"
    query+= "  ORDER BY t2.value_stream_id ASC;"

    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()

    autotext = ""
    for row in rows:
        autotext+= row[0]+" "+row[1]+" : "+str(row[2])+"|"
    cur.close()
    conn.close()      

    return autotext



def get_capbilities_for_review(service, operation, operation_sub_group):
    conn = connect_db()
    cur = conn.cursor() 

    query = """SELECT 
                    t4.value_stream_id AS value_stream_id,
                    t4.value_stream_name AS value_stream_name,
                    t2.capability_id AS capability_id,
                    t2.capability_name AS capability_name,
                    t2.capability_definition AS capability_definition, 
                    t.question_id AS question_id, 
                    t1.question_description AS question_description, 
                    t2.weighting AS weighting,                    
                    t.cla_level1_id, t.cla_level1_description,
                    t.cla_level2_id, t.cla_level2_description,
                    t.cla_level3_id, t.cla_level3_description,
                    t.cla_level4_id, t.cla_level4_description,
                    t.cla_level5_id, t.cla_level5_description
                FROM cla t
                INNER JOIN question t1 ON t1.question_id = t.question_id 
                INNER JOIN capability_question_relation t3 ON t3.question_id = t1.question_id  
                INNER JOIN capability t2 ON t2.capability_id = t3.capability_id 
                INNER JOIN value_stream t4 ON t4.value_stream_id = t2.value_stream_id  
                WHERE t4.operation_sub_group = '"""
    query+= operation_sub_group
    query+= "' ORDER BY t4.value_stream_id, t2.capability_id, t1.question_id ASC;"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()
    cur.close()
    conn.close()

    review_data = list()
    #i is keys for dict 
    i = [
        'value_stream_id', 'value_stream_name', 'capability_id', 'capability_name', 'capability_definition', 'question_id', 'question_description', 'weighting',
        'cla_level1_id', 'cla_level1_description', 'cla_level2_id', 'cla_level2_description', 'cla_level3_id', 'cla_level3_description',
        'cla_level4_id', 'cla_level4_description', 'cla_level5_id', 'cla_level5_description'
    ]
    #each j is the row value
    for j in rows:
        review_data.append(
            {
                i[0]:j[0], i[1]:j[1], i[2]:j[2], i[3]:j[3], i[4]:j[4], i[5]:j[5], i[6]:j[6], i[7]:str(j[7]), 
                i[8]:j[8], i[9]:j[9], i[10]:j[10], i[11]:j[11], i[12]:j[12], i[13]:j[13],
                i[14]:j[14], i[15]:j[15], i[16]:j[16], i[17]:j[17]
            }
        )

    return review_data 

def get_sub_dimensions():
    conn = connect_db()
    cur = conn.cursor() 
    query = """SELECT 
                    sub_dimension_id AS sub_dimension_id, 
                    sub_dimension_name AS sub_dimension_name, 
                    sub_dimension_definition AS sub_dimension_definition, 
                    sub_dimension_context AS sub_dimension_context, 
                    dimension AS dimension
                FROM sub_dimension
                WHERE 
                dimension = 'Technology'
                ORDER BY sub_dimension_id ASC"""
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # Create DataFrame from the list of tuples
    df = pd.DataFrame(rows, columns=[
    'Sub Dimension Id', 'Name', 'Definition', 'AO Context', 'Dimension'
    ])
    return df 

def get_attributes(sub_dimension_id):  
    conn = connect_db()
    cur = conn.cursor() 
    #print("sub_dimension_id =", sub_dimension_id)
    query = """SELECT 
                    t.criteria_id AS criteria_id, 
                    t1.criteria_scope AS criteria_scope, 
                    t1.criteria_description AS criteria_description, 
                    t.attribute_level1,
                    t.attribute_level2,
                    t.attribute_level3,
                    t.attribute_level4,
                    t.attribute_level5
                FROM attribute t
                INNER JOIN criteria t1 ON t1.criteria_id = t.criteria_id  
                WHERE 
                t1.sub_dimension_id = '"""
    query+= sub_dimension_id
    query+= "' ORDER BY t1.criteria_id ASC"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()

    cur.close()
    conn.close()
        
    # Create DataFrame from the list of tuples
    df = pd.DataFrame(rows, columns=[
    'Criteia Id', 'Scope', 'Description', 'Attribute Level 1 (Initiating)', 'Attribute Level 2 (Emerging)', 
    'Attribute Level 3 (Performing)', 'Attribute Level 4 (Advancing)', 'Attribute Level 5 (Leading)'
    ])
    return df 


def get_questions(capability_id):  
    conn = connect_db()
    cur = conn.cursor() 
    #print("capability_id =", capability_id)
    query = """SELECT 
                    t.question_id AS question_id, 
                    t1.question_description AS question_description, 
                    t.cla_level1_id,
                    t.cla_level1_description,
                    t.cla_level2_id,
                    t.cla_level2_description,
                    t.cla_level3_id,
                    t.cla_level3_description,
                    t.cla_level4_id,
                    t.cla_level4_description,
                    t.cla_level5_id,
                    t.cla_level5_description
                FROM cla t
                INNER JOIN question t1 ON t1.question_id = t.question_id  
                INNER JOIN value_stream t2 ON t2.value_stream_id = t1.value_stream_id 
                AND t2.capability_id = '"""
    query+= capability_id
    query+= "' ORDER BY t.question_id ASC"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()

    cur.close()
    conn.close()
        
    # Create DataFrame from the list of tuples
    df = pd.DataFrame(rows, columns=[
    'Criteia Id', 'Scope', 'Description', 'Attribute Level 1 (Initiating)', 'Attribute Level 2 (Emerging)', 
    'Attribute Level 3 (Performing)', 'Attribute Level 4 (Advancing)', 'Attribute Level 5 (Leading)'
    ])
    return df 

def get_all_users():
    conn = connect_db()
    cur = conn.cursor() 
    #CONCAT('&lt;input type="radio" name="selected_user_id" value="',user_id,'" id="selected_user_id"&gt;') AS Edit,
    query = """SELECT 
                    user_id AS user_id, 
                    fname AS fname, 
                    lname AS lname, 
                    email,
                    role,
                    creation_time,
                    last_login_time
                FROM public.user
                WHERE id > 1
                ORDER BY user_id ASC"""
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()

    user_data = None
    df = None

    if rows is None or len(rows) == 0:
        print("No result for users. Check if database is working.")
    else:
        #print("#rows in get_all_users().", len(rows))
        # Create DataFrame from the list of tuples
        df = pd.DataFrame(rows, columns=[
                                        'User Id', 'First Name', 'Last Name', 'Email', 'Role', 'Creation time', 'Last login time'
                                        ])

        user_data = list()
        #i is keys for dict 
        i = [
            'user_id', 'fname', 'lname', 'email', 'role', 'creation_time', 'last_login_time'
        ]
        #each j is the row value
        for j in rows:
            user_data.append(
                {
                    i[0]:j[0], i[1]:j[1], i[2]:j[2], i[3]:j[3], i[4]:j[4], i[5]:j[5], i[6]:j[6], 
                }
            )
    cur.close()
    conn.close()
    print(df)
    print(user_data)
    return df, user_data 

def get_users():
    conn = connect_db()
    cur = conn.cursor() 
    query = """SELECT 
                    user_id AS user_id, 
                    fname AS fname, 
                    lname AS lname, 
                    email,
                    role,
                    hashed_password,
                    creation_time
                FROM public.user
                WHERE id > 1
                ORDER BY user_id ASC"""
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()

    cur.close()
    conn.close()
    if rows is None or len(rows) == 0:
        print("No result for users. Check if database is working.")
    #else:        
    #    print(rows[0]) 
        
    # Create DataFrame from the list of tuples
    df = pd.DataFrame(rows, columns=[
        'user_id', 'fname', 'lname', 'email', 'role', 'hashed_password', 'creation_time'
    ])
    return df 

def get_user(user_id):
    conn = connect_db()
    cur = conn.cursor() 
    query = """SELECT 
                    user_id AS user_id, 
                    fname AS fname, 
                    lname AS lname, 
                    email,
                    role,
                    hashed_password,
                    creation_time
                FROM public.user
                WHERE UPPER(user_id) = UPPER('"""
    query+= user_id + "');"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()

    cur.close()
    conn.close()
        
    # Create DataFrame from the list of tuples
    df = pd.DataFrame(rows, columns=[
        'user_id', 'fname', 'lname', 'email', 'role', 'hashed_password', 'creation_time'
    ])
    return df 

def get_user_data(user_id):
    conn = connect_db()
    cur = conn.cursor() 
    query = """SELECT 
                    user_id AS user_id, 
                    fname AS fname, 
                    lname AS lname, 
                    email,
                    role,
                    hashed_password,
                    creation_time
                FROM public.user
                WHERE UPPER(user_id) = UPPER('"""
    query+= user_id + "')"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()
       
    # Create DataFrame from the list of tuples
    user_data = {'user_id':rows[0][0], 'fname':rows[0][1], 'lname':rows[0][2], 'email':rows[0][3], 'role':rows[0][4], 'hashed_password':rows[0][5], 'creation_time':rows[0][6]}

    query = """SELECT 
                    operation_id
                FROM public.user_operation_map 
                WHERE UPPER(user_id) = UPPER('"""
    query+= user_id + "');"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()    

    user_ops_list = list()
    for row in rows:
        user_ops_list.append(row[0])
    
    cur.close()
    conn.close()
    
    return user_data, user_ops_list 

def get_user_ops_data(user_id):
    conn = connect_db()
    cur = conn.cursor() 
    query = """SELECT 
                    operation_id
                FROM public.user_operation_map 
                WHERE UPPER(user_id) = UPPER('"""
    query+= user_id + "');"
    cur.execute(query)
    # Fetch all rows as a list of tuples
    rows = cur.fetchall()    

    user_ops_list = list()
    for row in rows:
        user_ops_list.append(row[0])

    cur.close()
    conn.close()
    
    return user_ops_list        

def insert_new_user(role, fname, lname, email, ha256_hashed_password, user_ops_map):
    conn = connect_db()
    cur = conn.cursor() 
    dt = datetime.now(timezone.utc)
    cur.execute("INSERT INTO public.user (user_id, fname, lname, email, role, hashed_password, creation_time, is_active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (email, fname, lname, email, role, ha256_hashed_password, dt, 't'))
    conn.commit()

    # Insert OP_AO for Autonomous Operations as the default for every user.
    cur.execute("INSERT INTO public.user_operation_map (user_id, operation_id) VALUES (UPPER('"+ email +"'),'OP_AO')")
    conn.commit()

    user_operations = user_ops_map.split(",")
    for user_op in user_operations:
        if user_op in ("OP_TM", "OP_NOC", "OP_NA", "OP_FO", "OP_IM", "OP_SO", "OP_CX", "OP_NO", "OP_OT"):
            cur.execute("INSERT INTO public.user_operation_map (user_id, operation_id) VALUES (UPPER(%s),%s)", (email, user_op))
    conn.commit()

    cur.close()
    conn.close()    
    return get_users()

def update_user(user_id, role, fname, lname, ha256_hashed_password, is_active, user_ops_map):
    conn = connect_db()
    cur = conn.cursor() 
    #print("In update user: ", user_id, role, fname, lname, ha256_hashed_password, is_active)
    cur.execute("UPDATE public.user SET fname = %s, lname = %s, role = %s, hashed_password = %s, is_active = %s WHERE UPPER(user_id) = UPPER(%s);",
                (fname, lname, role, ha256_hashed_password, is_active, user_id))
    conn.commit()

    cur.execute("DELETE FROM public.user_operation_map WHERE UPPER(user_id) = UPPER('" + user_id + "') AND operation_id <> 'OP_AO';")
    conn.commit() 

    user_operations = user_ops_map.split(",")
    for user_op in user_operations:
        if user_op in ("OP_TM", "OP_NOC", "OP_NA", "OP_FO", "OP_IM", "OP_SO", "OP_CX", "OP_NO", "OP_AO", "OP_OT"):
            cur.execute("INSERT INTO public.user_operation_map (user_id, operation_id) VALUES (UPPER(%s),%s)", (user_id, user_op))
    conn.commit()    

    cur.close()
    conn.close()    
    return get_user_data(user_id)         

def change_password(user_id, sha256_hashed_password): 
    conn = connect_db()
    cur = conn.cursor() 

    cur.execute("UPDATE public.user SET hashed_password = %s WHERE UPPER(user_id) = UPPER(%s);",
                (sha256_hashed_password, user_id))

    conn.commit()
    cur.close()
    conn.close()  
 
    return get_user(user_id) 


def update_last_login(user_id): 
    conn = connect_db()
    cur = conn.cursor() 

    cur.execute("UPDATE public.user SET last_login_time = %s WHERE UPPER(user_id) = UPPER(%s);",
                (datetime.now(timezone.utc), user_id))

    conn.commit()
    cur.close()
    conn.close()  
 
    return get_user(user_id) 

