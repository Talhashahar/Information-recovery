import json
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import Flask, request, jsonify, Response, render_template
import os
import mammoth

import index_model
import parseTest
import db_model

app = Flask(__name__)
CORS(app)

words_retrived = []

@app.route('/', methods=['GET', 'POST'])
def welcome():
    index_model.find_new_files_and_move_temp_folder()
    index_model.index_files_from_temp_folder()
    return render_template('/WebSerch.html', display="none")


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.query_string
    query = query.replace("query=", "")
    query = query.replace("%28", "( ")
    query = query.replace("%29", " )")
    query = query.replace("%26", " & ")
    query = query.replace("%7C", " | ")
    query = query.replace("%21", " ! ")
    query = query.replace("+", " ")
    query = query.replace("  ", " ")
    parsequery = parseTest.order_query(query)
    retive_docs = parseTest.compile_expression(parsequery)
    retive_information = []
    for x in retive_docs:
        retive_information.append(db_model.get_docs_details(x[2]))
    print retive_docs
    for x in retive_docs:
        global words_retrived
        words_retrived.append(str(x[0]))
    print retive_information
    docs_after_remvoe_duplicate = list(set(retive_information))
    return render_template('/WebSerch.html', docs=docs_after_remvoe_duplicate, display="block")


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    ACT = db_model.get_all_Active_docs_details()
    InACT = db_model.get_all_InActive_docs_details()
    total = db_model.get_all_Active_docs_details() + db_model.get_all_InActive_docs_details()
    return render_template('/admin.html', Activedocs=ACT, InActivedocs=InACT, Alldocs=total)


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            filename = file.filename
            stored_files = "C:\\Users\\talha\\Desktop\\Information-recovery-master\\data\\Original\\{}".format(filename)
            file.save(stored_files)
            index_model.find_new_files_and_move_temp_folder()
            index_model.index_files_from_temp_folder()
        ACT = db_model.get_all_Active_docs_details()
        InACT = db_model.get_all_InActive_docs_details()
        total = db_model.get_all_Active_docs_details() + db_model.get_all_InActive_docs_details()
        return render_template('/admin.html', Activedocs=ACT, InActivedocs=InACT, Alldocs=total)


@app.route('/documents/<int:doc_id>')
def display_document(doc_id):
    file = open("C:\\Users\\talha\\Desktop\\Information-recovery-master\\data\\indexed\\doc_{}.txt".format(doc_id), "rb")
    text = file.read().lower()
    for line in text.split('\n'):
        for word in line.split(' '):
            if word in words_retrived:
                word_bold = (word, '<b>{}</b>'.format(word))[1]
                text = text.replace(word, word_bold)
                if word in words_retrived: words_retrived.remove(word)
    return render_template('doc_result.html', text=text)


@app.route('/changeStatus/<int:doc_id>')
def change_status_document(doc_id):
    doc_details = db_model.get_doc_status(doc_id)
    if doc_details[3] == 1:
        db_model.set_inactive_doc(doc_id)
    else:
        db_model.set_active_doc(doc_id)
    ACT = db_model.get_all_Active_docs_details()
    InACT = db_model.get_all_InActive_docs_details()
    total = db_model.get_all_Active_docs_details() + db_model.get_all_InActive_docs_details()
    return render_template('/admin.html', Activedocs=ACT, InActivedocs=InACT, Alldocs=total)


if __name__ == '__main__':
    app.run()