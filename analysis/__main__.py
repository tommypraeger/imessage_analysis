import os
import sys
import analysis.actions as actions

action = sys.argv[1]

if action == 'analysis':
    actions.analysis.main(sys.argv[2:])

