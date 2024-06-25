import json
import validators

from flask import Flask, request
from kgk_controller import search_posts, BASE_API_URL, BASE_WEB_URL

# create Flask instance
app_api = Flask(__name__)

# a simple description of the API
description_html = '''
                <!DOCTYPE html>
                <head>
                <title>API Landing</title>
                </head>
                <body>  
                    <h3>A simple API using Flask</h3>
                    <a href="http://localhost:5001/api?url=https://www.klassegegenklasse.org/">sample request</a>
                </body>
                '''


# return simple description
@app_api.route('/', methods=['GET'])
def description():
    return description_html


# requires user string argument: url
# returns error message if wrong arguments are passed.
@app_api.route('/api', methods=['GET'])
def get_content_from_url():
    required_params = ['url']
    # check for the required parameters
    if not all(k in request.args for k in required_params):
        error_message = {
            'Required paremeters': required_params,
            'Provided paremeters': [k for k in request.args],
        }
        return json.dumps({'status': 'error', 'message': error_message})

    # check validity of given url
    url = request.args.get('url')
    if not validators.url(url):
        error_message = f'Please submit a valid URL.'
        return json.dumps({'status': 'error', 'message': error_message})

    # remove trailing slash if necessary
    if url[-1] == '/':
        url = url[:-1]
    # isolate slug for content retrieval
    if BASE_WEB_URL in url:
        url = url.split(BASE_WEB_URL)[-1]
    content = search_posts(BASE_API_URL, url)

    # check that content was retrieved
    if content is None or len(content) < 1:
        error_message = 'Could not retrieve content for the provided URL.'
        return json.dumps({'status': 'error', 'message': error_message})

    return json.dumps({'status': 'success', 'summary': content})


if __name__ == '__main__':
    # for debugging locally
    app_api.run(debug=True, host='0.0.0.0', port=5001)

    # for production
    # app_api.run(host='0.0.0.0', port=5001)
