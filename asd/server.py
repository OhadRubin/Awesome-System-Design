from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with, reqparse, Resource
import asd_pb2
from flask_restful import reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int)
parser.add_argument('username')
parser.add_argument('birthday')
parser.add_argument('gender')


#each parser has fields it requires 
snapshot_fields = [
                    "pose",
                   "color_image",
                   "depth_image",
                   "feelings"
                  ]

class Config(Resource):
    def get(self):
        args = parser.parse_args()
        parser_names, available_parsers = self.collect_parsers()
        return {"data": args, "parsers": parser_names}

    def post(self):
        # print(len(request.data))
        packet = asd_pb2.Packet.FromString(request.data) 
        # TODO: publish to queue
        #print(packet.snapshot.pose)
        return {"form": "hi"}
    
    def collect_parsers(self):
        return snapshot_fields,{}


api.add_resource(Config, '/config')

if __name__ == '__main__':
    app.run(debug=True)