import json
from src.functions import get_function_class_by_name


def main(args):
    function_name = args.function
    function = get_function_class_by_name(function_name)
    if not args.graph:
        categories = function.get_categories()
    elif args.graph_individual:
        categories = function.get_categories_allowing_graph()
    else:
        categories = function.get_categories_allowing_graph_total()
    return json.dumps(categories)
