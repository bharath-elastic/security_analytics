from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.json)
        return 'got request', 200
    else:
        return '<h1>webhook receiver</h1>'
