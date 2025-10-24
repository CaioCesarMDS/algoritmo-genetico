from constants import USA13

# validate route, if route = 0 invalid
def validate_route(route):
    if route == 0 and route != 12:
        return 0
    
    expected_cities = list(range(1, 13))

    for city in expected_cities:
        if city not in route:
            return 0

    return route

def calculate_distance(route):
    if validate_route(route) == 0:
        return 0

    total_distance = 0
    previous_city = 0
    for city in route:
        total_distance += USA13[previous_city][city]
        previous_city = city
    total_distance += USA13[0][route[11]]
    return total_distance
        
# === Execução principal ===
if __name__ == "__main__":
    ex_route = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    ex_route2 = [1, 9, 3, 4, 5, 7, 6, 10, 11, 8, 2, 12]
    ex_invalid_route = [1, 9, 3, 4, 5, 26, 6, 10, 11, 8, 2, 13]
    ex_invalid_route2 = [1, 9, 3, 4, 5, 26]
    print(calculate_distance(ex_route))
    print(calculate_distance(ex_route2))
    print(calculate_distance(ex_invalid_route))    
    print(calculate_distance(ex_invalid_route2))    