import analysis.utils.helpers as helpers
import analysis.utils.parse_args as parse_args


def main(args):
    args = parse_args.get_add_contact_args(args)

    user_data = helpers.load_user_data()

    if args.name not in user_data['contacts']:
        return f'No contact found for {args.name}'

    del user_data['contacts'][args.name]
    del user_data['chat_ids'][args.name]
    if not args.group:
        del user_data['contact_ids'][args.name]

    helpers.save_user_data(user_data)

    return f'Contact for {args.name} deleted successfully'
