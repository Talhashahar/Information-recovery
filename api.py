import json
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import Flask, request, jsonify, Response, render_template

import index_model
import parseTest

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def welcome():
    data1 = "Text"
    return render_template('/WebSerch.html', data=data1)





if __name__ == '__main__':
    app.run()