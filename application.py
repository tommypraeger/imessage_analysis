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
            output = self.get_output(args)
        except subprocess.CalledProcessError as e:
            # Get exception from stack trace
            error = str(e.output).split('\\n')[-2][11:]
            print(error)
            return {
                'errorMessage': error['message']
            }, 400

        try:
            output = json.loads(output)
        except json.decoder.JSONDecodeError:
            print(output)
            return {
                'errorMessage': output
            }, 400

        if 'errorMessage' in output:
            print(output['errorMessage'])
            return output, 400

        return output, 200

    def post(self, action):
        parser = reqparse.RequestParser()
        parser.add_argument('args', type=dict, required=True)
        args_dict = parser.parse_args()['args']

        args_list = []
        for key in args_dict:
            args_list.append(f'--{key}')
            val = args_dict[key]
            if val != '':
                args_list.append(val)

        try:
            args = ['python3', '-m', 'analysis', action]
            args.extend(args_list)
            output = self.get_output(args)
        except subprocess.CalledProcessError as e:
            # Get exception from stack trace
            error = str(e.output).split('\\n')[-2][11:]
            print(error)
            return {
                'errorMessage': error
            }, 400

        try:
            output = json.loads(output)
        except json.decoder.JSONDecodeError:
            print(output)
            return {
                'errorMessage': output
            }, 400

        if 'errorMessage' in output:
            print(output['errorMessage'])
            return output, 400

        return output, 200

    def get_output(self, args):
        args = self.convert_args_to_strs(args)
        output = subprocess.run(args, stdout=subprocess.PIPE)
        return output.stdout.decode('utf-8')

    def convert_args_to_strs(self, args):
        return [str(arg) for arg in args]


api.add_resource(Application, '/api/v1/<string:action>')

if __name__ == '__main__':
    application.run(debug=True)
