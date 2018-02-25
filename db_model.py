import mysql.connector
import datetime
from dateutil.relativedelta import relativedelta

cnx = None


def get_connection():
    global cnx
    if cnx is None:
        cnx = mysql.connector.connect(user='root', password='Password1',
                                      host='127.0.0.1',
                                      database='db_final_project', port=3306)
    return cnx


def disconnectDB():
    db = get_connection()
    db.close()

