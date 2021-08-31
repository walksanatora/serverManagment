import flask
from flask import request, url_for
app = flask.Flask(__name__)

import docker
dock = docker.from_env()

@app.route('/up/<path:file>')
def upload(file):  
    return 

@app.route('/down/<path:file>')
def download(file):
    pass

if __name__ == '__main__':
    app.run(port=8182,host='0.0.0.0')