import json

from validators import url as validate_url
from flask import Flask, request

from kgk_controller import find_specific_post
from summarizer import summarize


# create Flask instance
app_api = Flask(__name__)


# a simple description of the API
description_html = '''
    <!DOCTYPE html>
    <head>
        <title>Article Summarizer</title>
    </head>
    <body>  
        <h3>A simple API to generate summaries from klassegegenklasse articles.</h3>
        <a href="http://localhost:5000/api?url=https://www.klassegegenklasse.org/">sample request</a>
    </body>
    '''


# return simple description
@app_api.route('/', methods=['GET'])
def description():
    return description_html


# return generated summary for valid user input url
@app_api.route('/api', methods=['GET'])
def get_content_from_url():
    required_params = ['url']

    try:
        # check for the required parameters
        assert all(k in request.args for k in required_params), str(
            {
                'Required paremeters': required_params,
                'Provided paremeters': [k for k in request.args],
            }
        )
        url = request.args.get('url')
        # check validity of given url
        assert validate_url(url), 'Please submit a valid URL.'

        content = find_specific_post(url)
        assert (  # check that content was retrieved properly
            content is not None
        ), 'Could not retrieve content for the provided URL.'

        summary = summarize(
            content.get('content', {}).get('rendered'), promp_index=0
        )

        assert (  # check that summary was generated
            summary is not None
        ), "Could not generate summary from retrieved content."

    except AssertionError as err:
        return json.dumps({'status': 'error', 'message': str(err)})

    return json.dumps(
        {
            'status': 'success',
            'slug': content.get('slug', ''),
            'summary': summary,
        }
    )


if __name__ == '__main__':
    # for debugging locally
    app_api.run(debug=True, host='0.0.0.0', port=5000)

    # for production
    # app_api.run(host='0.0.0.0', port=5000)
