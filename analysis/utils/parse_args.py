import argparse
from analysis.utils.helpers import get_functions


def get_analysis_args(args):
    parser = argparse.ArgumentParser(description='run analysis on text messages')

    parser.add_argument('--name', type=str, help='name of person or group chat')
    parser.add_argument('--export', action='store_true', help='export data to csv')
    parser.add_argument('--from-date', type=str, help='date to start from. format mmddyy')
    parser.add_argument('--to-date', type=str, help='date to end at. format mmddyy')
    parser.add_argument('--group', action='store_true', help='desired chat is a group chat')
    parser.add_argument('--csv', action='store_true', help='messages are uploaded as a csv')
    parser.add_argument('--separate', action='store_true', help='separate phrase into words')
    parser.add_argument('--case-sensitive', action='store_true', help='make search case sensitive')
    parser.add_argument('--regex', action='store_true', help='use RegEx')
    parser.add_argument('--print-messages', action='store_true',
                        help='print found messages')  # not currently implemented
    parser.add_argument('--graph-individual', action='store_true',
                        help='graph lines for each person in group')
    parser.add_argument('--phrase', type=str, help='phrase to search for')
    parser.add_argument('--mime-type', type=str, help='MIME type of message to search for')
    parser.add_argument('--minutes-threshold', type=int,
                        help='Threshold in minutes from last messages for a message to be considered a conversation starter')

    function_group = parser.add_mutually_exclusive_group()
    function_group.add_argument('--function', type=str,
                                choices=get_functions(), help='name of function to call')
    function_group.add_argument('--all-functions', action='store_true', help='call all functions')

    graph_time_periods = parser.add_mutually_exclusive_group()
    graph_time_periods.add_argument('--day', action='store_true', help='graph data by day')
    graph_time_periods.add_argument('--week', action='store_true', help='graph data by week')
    graph_time_periods.add_argument('--month', action='store_true', help='graph data by month')
    graph_time_periods.add_argument('--year', action='store_true', help='graph data by year')

    return parser.parse_args(args)


def get_add_contact_args(args):
    parser = argparse.ArgumentParser(description='add contact')

    parser.add_argument('--name', type=str, help='name of person or group chat')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--number', type=str, help='phone number of person')
    group.add_argument('--group', action='store_true', help='desired contact is a group chat')

    return parser.parse_args(args)


def get_delete_contact_args(args):
    parser = argparse.ArgumentParser(description='add contact')

    parser.add_argument('--name', type=str, help='name of person or group chat')
    parser.add_argument('--group', action='store_true', help='desired contact is a group chat')

    return parser.parse_args(args)


def get_edit_contact_args(args):
    parser = argparse.ArgumentParser(description='add contact')

    parser.add_argument('--name', type=str, help='name of person or group chat')
    parser.add_argument('--old-name', type=str, help='previous name of person or group chat')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--number', type=str, help='phone number of person')
    group.add_argument('--group', action='store_true', help='desired contact is a group chat')

    return parser.parse_args(args)
