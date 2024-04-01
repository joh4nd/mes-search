import re
from flask import Flask, render_template, request, session
from flask_session import Session # https://pypi.org/project/Flask-Session/
from pipeline.es_client import Search

es = Search()

app = Flask(__name__)

# set cookie policy
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.get('/')
def index():
    return render_template('index.html')


@app.post('/')
def handle_search():
    query = request.form.get('query', '')
    return render_template(
        'index.html', query=query, results=[], from_=0, total=0)


@app.get('/document/<id>')
def get_document(id):
    return 'Document not found'
