from __future__ import print_function
from math import hypot, ceil
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from geopy.distance import geodesic


def create_data_model(locations):
    """Stores the data for the problem."""
    data = {}
    # Locations in block units
    data['locations'] = prepare_locations(locations)
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def prepare_locations(locations):
    data = []

    for item in locations:
        location = (float(item["lat"]), float(item['lon']))
        data.append(location)
    return data


def compute_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                distance_from = (from_node[0], from_node[1])
                distance_to = (to_node[0], to_node[1])
                distances[from_counter][to_counter] = ceil(geodesic(distance_from, distance_to).km)

    return distances


def get_tour_list(manager, routing, assignment):
    index = routing.Start(0)
    tour = []

    while not routing.IsEnd(index):
        tour.append(manager.IndexToNode(index))
        index = assignment.Value(routing.NextVar(index))

    tour.append(manager.IndexToNode(index))

    return tour


def build_tours(locations):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(locations)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['locations']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    distance_matrix = compute_distance_matrix(data['locations'])

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    return get_tour_list(manager, routing, assignment)
