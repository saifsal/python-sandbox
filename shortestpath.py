import json

from collections import deque


def shortest_path(graph, start, target):
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current, path = queue.popleft()

        if current == target:
            return path

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None

def find_all_country_pairs(graph):
    countries = list(graph.keys())
    results = []

    for i, country_a in enumerate(countries):
        for country_b in countries[i + 1:]:
            path = shortest_path(graph, country_a, country_b)

            if path is None:
                continue

            intermediate = len(path) - 2

            results.append({
                "country_a": country_a,
                "country_b": country_b,
                "intermediate": intermediate,
                "path": path
            })

    results.sort(
        key=lambda result: result["intermediate"],
        reverse=True
    )

    return results

def make_graph_consistent(graph):
    for country, neighbors in list(graph.items()):
        for neighbor in neighbors:
            if neighbor not in graph:
                graph[neighbor] = []

    for country, neighbors in list(graph.items()):
        for neighbor in neighbors:
            if country not in graph[neighbor]:
                graph[neighbor].append(country)

    return graph

def validate_graph(graph):
    errors = []

    if not isinstance(graph, dict):
        errors.append("Graph must be a dictionary.")
        return errors

    countries = set(graph.keys())

    for country, neighbors in graph.items():

        if not isinstance(country, str):
            errors.append(
                f"Invalid country name: {country!r}"
            )

        if not isinstance(neighbors, list):
            errors.append(
                f"{country}: borders must be a list."
            )
            continue

        if len(neighbors) != len(set(neighbors)):
            errors.append(
                f"{country}: duplicate border."
            )

        for neighbor in neighbors:

            if neighbor not in countries:
                errors.append(
                    f"{country} -> {neighbor}: "
                    f"unknown country."
                )
                continue

            if country == neighbor:
                errors.append(
                    f"{country}: borders itself."
                )

            if country not in graph[neighbor]:
                errors.append(
                    f"{country} -> {neighbor}: "
                    f"missing reverse border."
                )

    return errors

with open("countries.json", "r") as countries:
    graph = json.load(countries)

    errors = validate_graph(graph)

    if errors:
        print("Graph contains errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Graph is consistent.")

    results = find_all_country_pairs(graph)

    winning_path = results[0]['path']
    print(*winning_path, sep=" -> ")

    for result in results[:100]:
        print(
            f"{result['intermediate']:2d} | "
            f"{result['country_a']} -> {result['country_b']}"
        )
