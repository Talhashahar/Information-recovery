import mysql.connector
import datetime
from dateutil.relativedelta import relativedelta

cnx = None


def get_connection():
    global cnx
    if cnx is None:
        cnx = mysql.connector.connect(user='root', password='Password1',
                                      host='127.0.0.1',
                                      database='googlev2', port=3306)
    return cnx


def disconnectDB():
    db = get_connection()
    db.close()


def get_unuse_word_from_db():
    query = "SELECT * FROM googlev2.unuse_words;"
    cursor = get_connection().cursor()
    cursor.execute(query)
    return_values = []
    return_values = cursor.fetchall()
    return return_values