from flask import Flask, request, jsonify

from .functions import ALL as functions_all
from .backends import ALL as backends_all
from .common import ActionRequest

app = Flask(__name__)
def register_api(app, action):
    endpoint = action.endpoint
    function = action.function

    def flask_function():
        queries = request.args.to_dict()
        payload = request.data.decode('utf-8')
        action_request = ActionRequest(queries=queries, payload=payload)
        action_response = function(action_request)
        return jsonify(action_response.data), action_response.http_code, action_response.headers or {}

    flask_function.__name__ = action.function.__name__
    flask_function.__doc__ = action.function.__doc__
    app.add_url_rule(endpoint, endpoint, flask_function, methods=[action.method.name])

all_apis = functions_all + backends_all

for api in all_apis:
    for action in api:
        register_api(app, action)

if __name__ == '__main__':
    app.run(debug=True)