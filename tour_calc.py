from geopy.distance import geodesic
from math import ceil

def get_distances(tour_list):
    distances = []

    tour_list.pop() # Removendo destino final, ou seja, o ponto inicial

    for index, coordinate in enumerate(tour_list):
        if (index+1 < len(tour_list)):
            distance1 = coordinate
            distance2 = tour_list[int(index)+1]
            location1 = (distance1["lat"], distance1["lon"])
            location2 = (distance2["lat"], distance2["lon"])
            distances.append(geodesic(location1, location2).km)

    return {
        "total": ceil(sum(distances)),
        "items": distances
    }


def get_days_list(tour_list, distances, visiting_time):
    days = {"day1": [tour_list[0]]} # Inicializando o dia com o ponto de partida
    current_day = 1
    hours_in_day = 8
    time_buffer = 0

    for key, distance in enumerate(distances, 1):
        time = get_time(distance, 50, visiting_time)

        if (time_buffer + time < hours_in_day):
            time_buffer += time
            key_name = "day" + str(current_day)
            if (key_name in days and isinstance(days[key_name], list)):
                days[key_name].append(tour_list[int(key)])
            else:
                days[key_name] = []
                days[key_name].append(tour_list[int(key)])
        else:
            time_buffer = 0
            current_day += 1
            time_buffer += time
            key_name = "day" + str(current_day)

            if (key_name in days and isinstance(days[key_name], list)):
                days[key_name].append(tour_list[int(key)])
            else:
                days[key_name] = []

                if (int(current_day) > 1):
                    days[key_name].append(tour_list[0]) # Ponto de partida

                days[key_name].append(tour_list[int(key)])

    return days


def get_time(distance, speed = 50, visiting_time = 0):
    return (ceil(distance) / speed) + visiting_time
