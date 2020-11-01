import os
import sys
import analysis.actions as actions

action = sys.argv[1]
args = sys.argv[2:]

if action == 'analysis':
    response = actions.analysis.main(args)

if action == 'add_contact':
    response = actions.add_contact.main(args)

if action == 'edit_contact':
    response = actions.edit_contact.main(args)

if action == 'delete_contact':
    response = actions.delete_contact.main(args)

if action == 'test_db':
    response = actions.test_db.main()


print(response)
