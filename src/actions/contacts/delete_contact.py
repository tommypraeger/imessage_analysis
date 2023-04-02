from src.utils import helpers


def main(name, group, dry_run=False):
    user_data = helpers.load_user_data()

    if name not in user_data["contacts"]:
        return helpers.make_error_message(f"No contact found for {name}")

    del user_data["contacts"][name]
    del user_data["chat_ids"][name]
    if not group:
        del user_data["contact_ids"][name]

    if not dry_run:
        helpers.save_user_data(user_data)

    return helpers.make_success_message(f"Contact for {name} deleted successfully")
