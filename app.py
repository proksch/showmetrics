from flask import Flask, request, Response
from random import random
app = Flask(__name__)

countIdx = 0
countSub = 0


@app.route('/', methods=['GET'])
def index():
    global countIdx
    countIdx += 1
    return "<html><body><h1>Index</h1><p>You are visitor {}!</p><a href=\"./sub\">Goto Sub</a></body></html>".format(countIdx)

@app.route('/sub', methods=['GET'])
def sub():
    global countSub
    countSub += 1
    return "<html><body><h1>Sub</h1><p>This is not the main page anymore. Welcome sub-visitor {}!</p><a href=\"./\">Back to Index</a></body></html>".format(countSub)

@app.route('/metrics', methods=['GET'])
def metrics():
    global countIdx, countSub

    m = "# HELP my_random This is just a random 'gauge' for illustration.\n"
    m+= "# TYPE my_random gauge\n"
    m+= "my_random " + str(random()) + "\n\n"

    m+= "# HELP num_requests The number of requests that have been served, by page.\n"
    m+= "# TYPE num_requests counter\n"
    m+= "num_requests{{page=\"index\"}} {}\n".format(countIdx)
    m+= "num_requests{{page=\"sub\"}} {}\n".format(countSub)

    return Response(m, mimetype="text/plain")

app.run(host="0.0.0.0", port=8080, debug=True)