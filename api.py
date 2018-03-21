import json
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import Flask, request, jsonify, Response, render_template
import os

import index_model
import parseTest
import db_model

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def welcome():
    data1 = "Text"
    return render_template('/WebSerch.html', data=data1, display="none")
    pass


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
    print retive_information
    return render_template('/WebSerch.html', docs=retive_information, display="block")


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    all_docs = db_model.get_all_docs_details()
    pass
    return render_template('/admin.html', docs=all_docs)
    pass


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist("file")
        for file in files:
            filename = file.filename
            stored_files = "C:\Information_Retrive\data\Original\\{}.txt".format(filename)
            file.save(stored_files)
            index_model.find_new_files_and_move_temp_folder()
            index_model.index_files_from_temp_folder()
        return render_template('admin.html')




if __name__ == '__main__':
    app.run()