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
    """
    Query msgs in index.
    
    Enable full-text and vector search.

    Refs:
    - https://www.elastic.co/search-labs/tutorials/search-tutorial/vector-search/nearest-neighbor-search
    """

    query = request.form.get('query', '')
    from_ = request.form.get('from_', type=int, default=0)
    search_type = request.form.get('searchType', '')

    # use index_name to set search key
    index_name = list(es.es.indices.get_alias(index="*").keys())[0]
    if index_name == "isis_docs":
            doctype = 'tweets'
    elif index_name == "documents":
            doctype = 'name'
    else:
        pass

    if search_type == 'full_text':
        query_dll={'match': {doctype: {'query': query}}}
        res = es.search(query=query_dll, size=5, from_=from_)

    elif search_type == 'vector':
        res = es.search(knn={'field': 'embedding',
                            'query_vector': es.get_embedding(query),
                            'num_candidates': 50,
                            'k': 10},
                        size=5,
                        from_=from_)
    
    return render_template('index.html',
                           results = res['hits']['hits'],
                           query = query,
                           from_= from_,
                           total = res['hits']['total']['value'],
                           search_type=search_type)


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
