import analysis.actions.add_contact as add_contact
import analysis.actions.delete_contact as delete_contact
import analysis.utils.helpers as helpers


def main(name, old_name, group, number):
    delete_response = delete_contact.main(old_name, group, dry_run=True)
    if 'successMessage' not in delete_response:
        return delete_response

    add_response = add_contact.main(name, group, number, dry_run=True)
    if 'successMessage' not in add_response:
        return add_response

    delete_contact.main(old_name, group)
    add_contact.main(name, group, number)

    return helpers.make_success_message(f'Edited contact for {name} successfully')
