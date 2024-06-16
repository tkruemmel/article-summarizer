import json
import validators

from flask import Flask, request
from kgk_controller import search_posts, BASE_URL

# create Flask instance
app = Flask(__name__)

# a simple description of the API written in html
description = '''
                <!DOCTYPE html>
                <head>
                <title>API Landing</title>
                </head>
                <body>  
                    <h3>A simple API using Flask</h3>
                    <a href="http://localhost:5001/api?url=https://www.klassegegenklasse.org/">sample request</a>
                </body>
                '''


@app.route('/', methods=['GET'])
def hello_world():
    return description


# requires user string argument: url
# returns error message if wrong arguments are passed.
@app.route('/api', methods=['GET'])
def square():
    required_params = ['url']
    if not all(k in request.args for k in required_params):
        error_message = {
            'Required paremeters': required_params,
            'Supplied paremeters': f'{[k for k in request.args]}',
        }
        return json.dumps({'status': 'error', 'message': error_message})

    url = request.args.get('url')
    if not validators.url(url):
        error_message = f'Please submit a valid URL: {url}.'
        return json.dumps({'status': 'error', 'message': error_message})

    if 'klassegegenklasse.org/' in url:
        url = url.split('klassegegenklasse.org/')[-1]
    content = search_posts(BASE_URL, url)
    return json.dumps({'status': 'success', 'summary': content})


if __name__ == '__main__':
    # for debugging locally
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5001)

    # for production
    # app.run(host='0.0.0.0', port=5001)
