# flask-app.py
from flask import Flask, request
import json

# create Flask instance
app = Flask(__name__)

# a simple description of the API written in html
description = """
                <!DOCTYPE html>
                <head>
                <title>API Landing</title>
                </head>
                <body>  
                    <h3>A simple API using Flask</h3>
                    <a href="http://localhost:5000/api?value=2">sample request</a>
                </body>
                """


@app.route('/', methods=['GET'])
def hello_world():
    return description


# requires user integer argument: value
# returns error message if wrong arguments are passed.
@app.route('/api', methods=['GET'])
def square():
    if not all(k in request.args for k in (["value"])):
        error_message = f"\
                            Required paremeters : 'value'<br>\
                            Supplied paremeters : {[k for k in request.args]}\
                            "
        return error_message
    else:
        # value = int(request.args['value'])
        value = request.args.get('value', type=int)
        return json.dumps({"Value Squared": value**2})


if __name__ == "__main__":
    # for debugging locally
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)

    # for production
    # app.run(host='0.0.0.0', port=5000)
