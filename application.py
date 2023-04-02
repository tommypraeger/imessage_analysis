import json
import traceback
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import src

application = Flask(__name__)
api = Api(application)
CORS(application)


class Application(Resource):
    def get(self, action):
        return self.get_output(action)

    def post(self, action):
        parser = reqparse.RequestParser()
        parser.add_argument("args", type=dict, required=True)
        args_dict = parser.parse_args()["args"]

        args_list = []
        for key in args_dict:
            args_list.append(f"--{key}")
            val = args_dict[key]
            if val != "":
                args_list.append(val)

        return self.get_output(action, *args_list)

    def get_output(self, action, *args):
        try:
            args = self.convert_args_to_strs(args)
            output = src.main(action, args)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return self.error_msg(e, 500)

        try:
            output = json.loads(output)
        except json.decoder.JSONDecodeError:
            print(output)
            traceback.print_exc()
            return self.error_msg(output, 500)

        if "errorMessage" in output:
            print(output["errorMessage"])
            return output, 400

        return output, 200

    def convert_args_to_strs(self, args):
        return [str(arg) for arg in args]

    def error_msg(self, msg, code):
        return {"errorMessage": str(msg)}, code


api.add_resource(Application, "/api/v1/<string:action>")

if __name__ == "__main__":
    application.run(debug=True)
