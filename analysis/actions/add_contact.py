import analysis.utils.helpers as helpers
import analysis.utils.parse_args as parse_args
import analysis.utils.sql as sql


def main(name, group, number, dry_run=False):
    user_data = helpers.load_user_data()

    if group:
        chat_ids = sql.get_chat_ids_from_chat_name(name)
        if len(chat_ids) == 0:
            return (f'Did not find {name}.\n'
                    'Make sure you type the chat name exactly right.')

        user_data['chat_ids'][name] = chat_ids
        user_data['contacts'][name] = 'group'
    else:
        if number is None:
            return 'Must provide a phone number when adding a non-group contact'
        
        phone_number = helpers.clean_phone_number(number)
    
        contact_ids = sql.get_contact_ids_from_phone_number(phone_number)
        if len(contact_ids) == 0:
            return (f'Did not find {number}.\n'
                    'Make sure you type in the phone number correctly.')
        
        chat_ids = sql.get_chat_ids_from_phone_number(phone_number)
        if len(chat_ids) == 0:
            return (f'Did not find {number}.\n'
                    'Make sure you type in the phone number correctly'
                    'and you have messages with this number.')
        
        user_data['contact_ids'][name] = contact_ids
        user_data['chat_ids'][name] = chat_ids
        user_data['contacts'][name] = number

    if not dry_run:
        helpers.save_user_data(user_data)

    return f'Contact for {name} added successfully'
