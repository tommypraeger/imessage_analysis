import datetime
import time

import pandas as pd

import analysis.functions as functions
import analysis.utils as utils

# start_time = time.time()

# Get command line args
args = utils.parse_args.get_args()

# Get messages dataframe
df = utils.sql.get_df(args.name, args.group)

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

# Process df based on function
result_dict = functions.process_df(df, args)

result_df = pd.DataFrame(data=result_dict)
result_df.sort_values(by=result_df.columns[1], inplace=True, ascending=False)
print(result_df.to_string(index=False))

# Export to CSV
if args.csv:
    df.to_csv('message_data.csv')
    result_df.to_csv('member_data.csv', index=False)
    result_df.corr(method='pearson').round(4).to_csv('correlation_matrix.csv')

# print("--- %s seconds ---" % (time.time() - start_time))
