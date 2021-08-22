import datetime
import time

import pandas as pd

import analysis.functions as functions
import analysis.utils.constants as constants
import analysis.utils.helpers as helpers
import analysis.utils.sql as sql


def main(args):
    # start_time = time.time()

    # Get messages dataframe
    try:
        df = build_df(args)
    except Exception as e:
        return helpers.make_error_message(e)

    # Default to just getting total messages
    if args.function is None:
        args.function = 'total'

    # Always add reaction column
    df['is reaction?'] = df['text'].apply(helpers.is_reaction)

    # Get members of chat
    try:
        chat_members = get_chat_members(df, args)
    except Exception as e:
        return helpers.make_error_message(e)

    # Process df based on function
    try:
        result_dict = functions.process_df(df, args, chat_members)
    except Exception as e:
        return helpers.make_error_message(e)

    # Return graph data if requested
    if args.graph:
        return {
            'graphData': result_dict
        }

    try:
        result_df = pd.DataFrame(data=result_dict)
        result_df.sort_values(by=result_df.columns[1], inplace=True, ascending=False)
        # print(result_df.to_string(index=False))
    except Exception as e:
        return helpers.make_error_message(e)

    # Export to CSV
    if args.export:
        df.to_csv('message_data.csv', index=False)
        result_df.to_csv('member_data.csv', index=False)
        result_df.corr(method='pearson').round(4).to_csv('correlation_matrix.csv', index=False)

    # print("--- %s seconds ---" % (time.time() - start_time))

    return {
        'htmlTable': result_df.to_html(index=False)
    }


def build_df(args):
    if args.csv:
        df = build_df_from_csv(args)

    else:
        try:
            df = sql.get_df(args.name, args.group)
        except KeyError:
            if args.group:
                error_msg = f'Please add group chat {args.name} as a contact'
            else:
                error_msg = f'Please add {args.name} as a contact'
            raise Exception(error_msg)

        # Trim dataframe based on date constraints
        df = filter_by_date(df, args.from_date, args.to_date)

        # Set timezone and date format
        df['time'] = [
            datetime.datetime.fromtimestamp((t + constants.TIME_OFFSET) / 1e9)
            for t in df['time']
        ]

        # Clean type column
        df['type'] = [t if type(t) is str else 'text/plain' for t in df['type']]

    # Remove duplicate messages (happens with links sometimes)
    df = df.drop_duplicates(subset=['text', 'sender', 'time'])

    return df


def build_df_from_csv(args):
    # Message csv must be located in this file
    df = pd.read_csv('messages.csv')

    # Make sure necessary columns are there
    for column in ['text', 'sender']:
        if column not in df.columns:
            msg = f'Please make sure to include a {column} column in the csv'
            return helpers.make_error_message(msg)

    # Clean time column
    if 'time' in df.columns:
        if len(df.at[0, 'time']) >= 19:
            includes_time = True
        else:
            includes_time = False

        # Trim dataframe based on date constraints
        df = filter_by_date(df, args.from_date, args.to_date,
                            includes_time=includes_time, use_seconds=False)

        # Set timezone and date format
        if includes_time:
            df['time'] = [
                datetime.datetime(
                    int(t[constants.YEAR]),
                    int(t[constants.MONTH]),
                    int(t[constants.DAY]),
                    int(t[constants.HOURS]),
                    int(t[constants.MINUTES]),
                    int(t[constants.SECONDS]),
                )
                for t in df['time']
            ]
        else:
            df['time'] = [
                datetime.datetime(
                    int(t[constants.YEAR]),
                    int(t[constants.MONTH]),
                    int(t[constants.DAY])
                )
                for t in df['time']
            ]
    else:
        df['type'] = [datetime.datetime.now()] * len(df)

        # Clean type column
    if 'type' in df.columns:
        df['type'] = [t if type(t) is str else 'text/plain' for t in df['type']]
    else:
        df['type'] = ['text/plain'] * len(df)

    return df


def get_chat_members(df, args):
    if args.csv:
        chat_members = list(set(df['sender']))
    else:
        chat_ids = constants.CHAT_IDS[args.name]
        chat_members = list(set(sql.get_chat_members(chat_ids)))
    for member in chat_members:
        if any(char.isdigit() for char in member):
            if args.group:
                error_msg = f'Please add contacts for every member of {args.name}'
            else:
                error_msg = f'Please add {args.name} as a contact'
            raise Exception(error_msg)

    return chat_members


def filter_by_date(df, from_date, to_date, includes_time=False, use_seconds=True):
    offset = constants.TIME_OFFSET

    if from_date:
        if use_seconds:
            df = df[
                df['time'] >= helpers.date_to_time(from_date) - offset
            ]
        else:
            df = df[
                df.apply(lambda msg: helpers.date_to_time(msg.time, includes_time), axis=1)
                >=
                helpers.date_to_time(from_date)
            ]

    if to_date:
        if use_seconds:
            df = df[
                df['time'] <= helpers.date_to_time(to_date, end=True) - offset
            ]
        else:
            df = df[
                df.apply(lambda msg: helpers.date_to_time(msg.time, includes_time), axis=1)
                <=
                helpers.date_to_time(to_date, end=True)
            ]

    return df
