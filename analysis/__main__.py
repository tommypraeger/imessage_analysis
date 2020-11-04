import os
import sys
import analysis.actions as actions
import analysis.utils.parse_args as parse_args

action = sys.argv[1]
args = sys.argv[2:]

if action == 'analysis':
    # Too many possible args to pass in individually
    args = parse_args.get_analysis_args(args)
    response = actions.analysis.main(args)

if action == 'add_contact':
    args = parse_args.get_add_contact_args(args)
    response = actions.add_contact.main(args.name, args.group, args.number)

if action == 'edit_contact':
    args = parse_args.get_edit_contact_args(args)
    response = actions.edit_contact.main(args.name, args.old_name, args.group, args.number)

if action == 'delete_contact':
    args = parse_args.get_delete_contact_args(args)
    response = actions.delete_contact.main(args.name, args.group)

if action == 'get_all_chat_names':
    response = actions.get_all_chat_names.main()

if action == 'get_all_phone_numbers':
    response = actions.get_all_phone_numbers.main()

if action == 'test_db':
    response = actions.test_db.main()


print(response)
