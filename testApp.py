from flask import Flask, jsonify, request, render_template
import json
app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():

    # POST request
    if request.method == 'POST':
        print('Incoming..')

        # asjson = json.dumps(request.get_json())
        asjson = request.get_json()[1]

        print(type(asjson))  # parse as JSON
        print(asjson)
        return 'OK', 200

    # GET request
    else:
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers

@app.route('/test')
def test_page():
    # look inside `templates` and serve `index.html`
    return render_template('testIndex.html')