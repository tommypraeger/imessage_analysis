from src.utils import helpers, sql


def main(name, group, number, dry_run=False):
    user_data = helpers.load_user_data()

    if group:
        chat_ids = sql.get_chat_ids_from_chat_name(name)
        if len(chat_ids) == 0:
            msg = (
                f"Did not find {name}.\nMake sure you type the chat name exactly right."
            )
            return helpers.make_error_message(msg)

        user_data["chat_ids"][name] = chat_ids
        user_data["contacts"][name] = "group"

    else:
        if number is None:
            msg = "Must provide a phone number when adding a non-group contact"
            return helpers.make_error_message(msg)

        phone_number = helpers.clean_phone_number(number)

        contact_ids = sql.get_contact_ids_from_phone_number(phone_number)
        if len(contact_ids) == 0:
            msg = f"Did not find {number}.\nMake sure you type in the phone number correctly."
            return helpers.make_error_message(msg)

        chat_ids = sql.get_chat_ids_from_phone_number(phone_number)
        if len(chat_ids) == 0:
            msg = (
                f"Did not find {number}.\n"
                "Make sure you type in the phone number correctly"
                "and you have messages with this number."
            )
            return helpers.make_error_message(msg)

        user_data["contact_ids"][name] = contact_ids
        user_data["chat_ids"][name] = chat_ids
        user_data["contacts"][name] = number

    if not dry_run:
        helpers.save_user_data(user_data)

    return helpers.make_success_message(f"Contact for {name} added successfully")
