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
    """query docs attributes based on index"""
    
    query = request.form.get('query', '')

    indexname = list(es.es.indices.get_alias(index="*").keys())[0]
    if indexname == "isis_docs":
        doctype = 'tweets'
    elif indexname == "documents":
        doctype = 'name'
    else:
        pass

    results = es.search(query={'match': {doctype: {'query': query}}})
    return render_template('index.html',
                           results = results['hits']['hits'],
                           query = query,
                           from_= 0,
                           total = results['hits']['total']['value'])


@app.get('/document/<id>')
def get_document(id):
    return 'Document not found'
