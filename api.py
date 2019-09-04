from flask import Flask, request
from flask_restful import Api, Resource
from tour_build import build_tours
import tour_calc

app = Flask(__name__)
api = Api(app)

class Tour(Resource):
    def post(self):
        data = request.get_json()
        locations = data["locations"]

        if len(locations) == 0:
            return {
                "error": {
                    "message": "Empty locations list"
                },
                "success": False
            }, 412

        return self.get_ordered_tour(locations), 200


    def get_ordered_tour(self, locations):
        tour_list = []
        build_list = build_tours(locations)

        for location_index in build_list:
            tour_list.append(locations[location_index])

        distances = tour_calc.get_distances(tour_list)
        tour_list = tour_calc.get_days_list(tour_list, distances["items"])

        result = {
            "data" : {
                "tour": tour_list
            },
            "success": True
        }

        return result


api.add_resource(Tour, "/tours/build")

if __name__ == "__main__":
    app.run()

