import json
from analysis.functions import function_to_class_map


def main(function, graph_individual):
    if graph_individual:
        return json.dumps(function_to_class_map[function].get_categories())
    return json.dumps(function_to_class_map[function].get_categories_allowing_graph_total())
