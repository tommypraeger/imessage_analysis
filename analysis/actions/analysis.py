import datetime
import time

import pandas as pd

import analysis.functions as functions
import analysis.utils as utils


def main(args):
    # start_time = time.time()

    # Get messages dataframe
    try:
        df = utils.sql.get_df(args.name, args.group)
    except KeyError:
        if args.group:
            msg = f'Please group chat {args.name} as a contact'
            return utils.helpers.make_error_message(msg)
        else:
            msg = f'Please add {args.name} as a contact'
            return utils.helpers.make_error_message(msg)

    # Trim dataframe based on date constraints
    if args.from_date:
        df = df[df['time'] >= utils.helpers.date_to_time(args.from_date)]
    if args.to_date:
        df = df[df['time'] <= utils.helpers.date_to_time(args.to_date, end=True)]

    # Set timezone and date format
    df['time'] = [
        datetime.datetime.fromtimestamp((t + utils.constants.TIME_OFFSET) / 1e9)
        for t in df['time']
    ]

    # Clean type column
    df['type'] = [t if type(t) is str else 'text/plain' for t in df['type']]

    # Default to just getting total messages
    if args.function is None and not args.all_functions:
        args.function = 'total'

    # Always add reaction column
    df['is reaction?'] = df['text'].apply(utils.helpers.is_reaction)

    # Get members of chat
    chat_ids = utils.constants.CHAT_IDS[args.name]
    chat_members = list(set(utils.sql.get_chat_members(chat_ids)))
    for member in chat_members:
        if any(char.isdigit() for char in member):
            if args.group:
                msg = f'Please add contacts for every member of {args.name}'
                return utils.helpers.make_error_message(msg)
            else:
                msg = f'Please add {args.name} as a contact'
                return utils.helpers.make_error_message(msg)

    # Process df based on function
    result_dict = functions.process_df(df, args, chat_members)

    # Result dictionary without multiple columns means we are returning an graph
    if len(result_dict) < 2:
        return {
            'imagePath': 'graph.png'
        }

    result_df = pd.DataFrame(data=result_dict)
    result_df.sort_values(by=result_df.columns[1], inplace=True, ascending=False)
    # print(result_df.to_string(index=False))

    # Export to CSV
    if args.csv:
        df.to_csv('message_data.csv')
        result_df.to_csv('member_data.csv', index=False)
        result_df.corr(method='pearson').round(4).to_csv('correlation_matrix.csv')

    # print("--- %s seconds ---" % (time.time() - start_time))

    return {
        'htmlTable': result_df.to_html(index=False)
    }
