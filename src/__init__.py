import json
from sqlite3 import OperationalError
from src.actions.analysis import analysis, get_categories
from src.actions.contacts import (
    add_contact,
    edit_contact,
    delete_contact,
    get_all_chat_names,
    get_all_phone_numbers,
)
from src.actions.misc import get_user_data
from src.utils import parse_args, helpers


def main(action, args):
    try:
        if action == "analysis":
            # Too many possible args to pass in individually
            args = parse_args.get_analysis_args(args)
            response = analysis.main(args)

        if action == "add_contact":
            args = parse_args.get_add_contact_args(args)
            response = add_contact.main(args.name, args.group, args.number)

        if action == "edit_contact":
            args = parse_args.get_edit_contact_args(args)
            response = edit_contact.main(
                args.name, args.old_name, args.group, args.number
            )

        if action == "delete_contact":
            args = parse_args.get_delete_contact_args(args)
            response = delete_contact.main(args.name, args.group)

        if action == "get_all_chat_names":
            response = get_all_chat_names.main()

        if action == "get_all_phone_numbers":
            response = get_all_phone_numbers.main()

        if action == "get_user_data":
            response = get_user_data.main()

        if action == "get_categories":
            args = parse_args.get_get_categories_args(args)
            response = get_categories.main(args)

    except OperationalError:
        response = helpers.make_error_message(
            "Database permissions not set up correctly"
        )

    try:
        return json.dumps(response)
    except NameError:
        raise Exception(f'action "{action}" not found')
