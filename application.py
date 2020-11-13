# Flask web server
import json
import subprocess
from flask import Flask, request
from flask_restful import (
    Resource,
    Api,
    reqparse
)
from flask_cors import CORS

application = Flask(__name__)
api = Api(application)
CORS(application)


class Application(Resource):
    def get(self, action):
        try:
            args = ['python3', '-m', 'analysis', action]
            output = subprocess.check_output(args)
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            # Get exception from stack trace
            error = str(e.output).split('\\n')[-2][11:]
            print(error)
            return {
                'errorMessage': error['message']
            }

        output = json.loads(output)

        if 'errorMessage' in output:
            return output, 400

        return output, 200

    def post(self, action):
        parser = reqparse.RequestParser()
        parser.add_argument('args', type=dict, required=True)
        args_dict = parser.parse_args()['args']

        print(args_dict)

        args_list = []
        for key in args_dict:
            args_list.append(f'--{key}')
            val = args_dict[key]
            if val != '':
                args_list.append(val)

        try:
            args = ['python3', '-m', 'analysis', action]
            args.extend(args_list)
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            # Get exception from stack trace
            error = str(e.output).split('\\n')[-2][11:]
            print(error)
            return {
                'errorMessage': error
            }

        print(output)
        output = json.loads(output)

        if 'errorMessage' in output:
            return output, 400

        return output, 200


api.add_resource(Application, '/api/v1/<string:action>')

if __name__ == '__main__':
    application.run(debug=True)
