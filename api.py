from flask import Flask, request
from flask_restful import Api, Resource
from tour_build import build_tours

app = Flask(__name__)
api = Api(app)

class Tour(Resource):
    def post(self):
        data = request.get_json()
        locations = data["locations"]
        return build_tours(locations), 200

api.add_resource(Tour, "/tours/build")

if __name__ == "__main__":
    app.run()

