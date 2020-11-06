# Flask web server
import json
import subprocess
from flask import Flask, request
from flask_restful import (
    Resource,
    Api,
    reqparse
)

application = Flask(__name__)
api = Api(application)


class Application(Resource):
    def get(self, action):
        args = ['python3', '-m', 'analysis', action]
        output = json.loads(subprocess.check_output(args))

        if 'errorMessage' in output:
            return output, 400

        return output, 200

    def post(self, action):
        parser = reqparse.RequestParser()
        parser.add_argument('args', type=dict, required=True)
        args_dict = parser.parse_args()['args']

        args_list = []
        for key in args_dict:
            args_list.append(f'--{key}')
            args_list.append(args_dict[key])

        args = ['python3', '-m', 'analysis', action]
        args.extend(args_list)
        output = json.loads(subprocess.check_output(args))

        if 'errorMessage' in output:
            return output, 400

        return output, 200


api.add_resource(Application, '/api/v1/<string:action>')

if __name__ == '__main__':
    application.run(debug=True)