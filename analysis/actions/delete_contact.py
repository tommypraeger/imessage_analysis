import analysis.utils.helpers as helpers
import analysis.utils.parse_args as parse_args


def main(name, group, dry_run=False):
    user_data = helpers.load_user_data()

    if name not in user_data['contacts']:
        return f'No contact found for {name}'

    del user_data['contacts'][name]
    del user_data['chat_ids'][name]
    if not group:
        del user_data['contact_ids'][name]

    if not dry_run:
        helpers.save_user_data(user_data)

    return f'Contact for {name} deleted successfully'
