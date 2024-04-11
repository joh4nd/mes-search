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
    Query docs attributes based on index.

    For combined semantic/vector and full-text search

    Refs:
    - https://www.elastic.co/search-labs/tutorials/search-tutorial/semantic-search/semantic-search
    - https://www.elastic.co/search-labs/tutorials/search-tutorial/semantic-search/hybrid-search
    - https://www.elastic.co/search-labs/tutorials/search-tutorial/vector-search/hybrid-search
    """

    query = request.form.get('query', '')
    from_ = request.form.get('from_', type=int, default=0)

    indexname = list(es.es.indices.get_alias(index="*").keys())[0]
    if indexname == "isis_docs":
        doctype = 'tweets'
    elif indexname == "documents":
        doctype = 'name'
    else:
        pass

    # combined search
    search_query = {'sub_searches': [
                {'query': {'match': {doctype: {'query': query}}}}, # full-text
                {'query': {'text_expansion': {'elser_embedding': {
                                            'model_id': '.elser_model_2', # see es.deploy_elser()
                                            'model_text': query}}}} # vector
                                    ],
                'rank': {'rrf': {}}} # combine

    res = es.search(**search_query,
                    size=5, from_=from_)
    
    return render_template('index.html',
                           results = res['hits']['hits'],
                           query = query,
                           from_= from_,
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
