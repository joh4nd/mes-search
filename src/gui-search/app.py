import re
from flask import Flask, render_template, request, session
from flask_session import Session # https://pypi.org/project/Flask-Session/
from pipeline.es_client import Search
import re

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

    res = es.search(query={'match': {doctype: {'query': query}}})
    return render_template('index.html',
                           results = res['hits']['hits'],
                           query = query,
                           from_= 0,
                           total = res['hits']['total']['value'])


@app.get('/message/<id>')
def get_message(id):
    """Retrieves the messages"""

    res = es.retrieve_message(id)["_source"]
    

    #TODO make msg class to do this better...
    username = res['username']
    # msg = res['tweets'].split('\n')
    URLs = extract_urls(res['tweets'])
    if URLs:
        msg = remove_urls(res['tweets'], URLs)
    else:
        msg = res['tweets']

    return render_template('message.html', username=username, msg=msg, URLs=URLs)


def extract_urls(msg):
    """extract URLs from messages."""

    url_pattern = r'https?://\S+'
    
    urls = re.findall(url_pattern, msg)

    return urls

def remove_urls(msg, urls):
    """remove URLs from msgbodies"""

    msg_worker = msg

    for url in urls:
        msg_clean = re.sub(re.escape(url), '', msg_worker)
        msg_worker = msg_clean

    return msg_clean
