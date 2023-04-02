import json
from src.functions import get_function_class_by_name


def main(function_name, graph_individual):
    function = get_function_class_by_name(function_name)
    if graph_individual:
        categories = function.get_categories()
    else:
        categories = function.get_categories_allowing_graph_total()
    return json.dumps(categories)
