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


def init_unuse_words():
    db = get_connection()
    cursor = db.cursor()
    query = "insert into googlev2.unuse_words(term) VALUES ('or'), ('and'), ('if'), ('when'), ('than'), ('what'), ('else'), ('tal');"
    cursor.execute(query)
    db.commit()


def insert_words_to_db(word, count, doc_id):
    db = get_connection()
    cursor = db.cursor()
    query = ("insert into googlev2.term VALUES (%s, %s, %s)")
    data = (word, count, doc_id)
    try:
        cursor.execute(query, data)
        db.commit()
    except Exception as e:
        print 'write to log, failed to get word'
        db.rollback()



def retrive_doc_index_from_db():
    db = get_connection()
    cursor = db.cursor()
    query = ("SELECT * FROM googlev2.file_index")
    try:
        cursor.execute(query)
    except Exception as e:
        print 'write to log, failed to get word'
    res = cursor.fetchall()
    return res[0][0]


def inc_doc_index():
    db = get_connection()
    cursor = db.cursor()
    current_index = retrive_doc_index_from_db()
    current_index += 1
    query = ("""
            update googlev2.file_index
            set index_file=%s
            where index_file=%s
            """)
    data = (current_index, current_index-1)
    try:
        cursor.execute(query, data)
        db.commit()
    except Exception as e:
        print "write to log, failed to update index count"
        db.rollback()


def TEST_get_docs_from_2_temp_with_OR(term1,term2):
    db = get_connection()
    cursor = db.cursor()
    query = ("""
              SELECT * FROM googlev2.term 
              where term=%s or term=%s
              """)
    data = (term1,term2)
    try:
        cursor.execute(query, data)
    except Exception as e:
        print 'fail to get docs from db - query OR operator'
    res = cursor.fetchall()


def get_docs_from_2_temp_with_OR(term1,term2):
    term1_result = get_docs_from_single_temp(term1)
    term2_result = get_docs_from_single_temp(term2)
    return term1_result+term2_result


def get_docs_from_2_temp_with_AND(term1, term2):
    total_reuslt = []
    term1_result = get_docs_from_single_temp(term1)
    term2_result = get_docs_from_single_temp(term2)
    for x in term1_result:
        for y in term2_result:
            if x[2] == y[2]:
                total_reuslt +=x;
    return total_reuslt


def get_docs_from_single_temp(term_word):
    db = get_connection()
    cursor = db.cursor()
    query = ("SELECT * FROM googlev2.term where term=%s")
    data = (term_word, )
    try:
        cursor.execute(query, data)
    except Exception as e:
        print 'fail to get docs from db - query OR operator'
    res = cursor.fetchall()
    return res;


def get_docs_from_single_term_Not(term_word):
    db = get_connection()
    cursor = db.cursor()
    query = ("SELECT * FROM googlev2.term where term!=%s")
    data = (term_word, )
    try:
        cursor.execute(query, data)
    except Exception as e:
        print 'fail to get docs from db - query OR operator'
    res = cursor.fetchall()
    return res;


def insert_doc_detail(docName, docID, brief):
    db = get_connection()
    cursor = db.cursor()
    query = ("insert into googlev2.docs VALUES (%s, %s, %s)")
    data = (docID, docName, brief)
    try:
        cursor.execute(query, data)
        db.commit()
    except Exception as e:
        print 'write to log, failed to get word'
        db.rollback()


def get_docs_details(doc_id):
    db = get_connection()
    cursor = db.cursor()
    query = ("SELECT * FROM googlev2.docs where doc_id=%s")
    data = (doc_id, )
    try:
        cursor.execute(query, data)
    except Exception as e:
        print 'fail to get docs from db - query OR operator'
    res = cursor.fetchall()
    return res[0];

def get_all_docs_details():
    db = get_connection()
    cursor = db.cursor()
    query = ("SELECT * FROM googlev2.docs")
    try:
        cursor.execute(query)
    except Exception as e:
        print 'fail to get docs from db - query OR operator'
    res = cursor.fetchall()
    return res;