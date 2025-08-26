import datetime
import os

import pandas as pd

from src import functions
from src.utils import constants, helpers, sql


def main(args):
    # start_time = time.time()

    # Get messages dataframe
    try:
        df = build_df(args)
    except Exception as e:
        return helpers.make_error_message(e)

    # If no messages are available after loading/filters, return a clear error
    try:
        if df is None or len(df) == 0:
            return helpers.make_error_message(
                "No messages found for the selected inputs (contact/group, CSV, and/or date range)."
            )
    except Exception:
        # If df doesn't behave like a DataFrame, fail safe
        return helpers.make_error_message(
            "No messages found for the selected inputs (contact/group, CSV, and/or date range)."
        )

    # Default to just getting total messages
    if args.function is None:
        args.function = "total"

    # Swap raw ints for string message types (vectorized)
    try:
        # Map known message types; default to empty string when unknown/missing
        df["message_type"] = df["message_type"].map(constants.MESSAGE_TYPES).fillna("")
    except KeyError:
        # CSV input might not have reaction type
        df["message_type"] = [""] * len(df)

    # Get members of chat
    try:
        chat_members = get_chat_members(df, args)
    except Exception as e:
        return helpers.make_error_message(e)

    # Process df based on function
    try:
        function = functions.get_function_class_by_name(args.function)
        result_dict, df = function.run(df, args, chat_members)
    except Exception as e:
        return helpers.make_error_message(e)

    # Return graph data if requested
    if args.graph:
        return {"graphData": result_dict}

    try:
        result_df = pd.DataFrame(data=result_dict)
        # result_df.sort_values(by=result_df.columns[1], inplace=True, ascending=False)
        # print(result_df.to_string(index=False))
    except Exception as e:
        return helpers.make_error_message(e)

    # Export to CSV
    if args.export:
        df.to_csv("message_data.csv", index=False)
        result_df.to_csv("member_data.csv", index=False)
        result_df.corr(method="pearson", numeric_only=True).round(4).to_csv(
            "correlation_matrix.csv", index=False
        )

    # print("--- %s seconds ---" % (time.time() - start_time))

    return {"htmlTable": result_df.to_html(index=False, escape=False)}


def build_df(args):
    if args.csv:
        df = build_df_from_csv(args)

    else:
        try:
            df = sql.get_df(args.name, args.group)
        except KeyError:
            if args.group:
                error_msg = f"Please add group chat {args.name} as a contact"
            else:
                error_msg = f"Please add {args.name} as a contact"
            raise Exception(error_msg)

        # Trim dataframe based on date constraints
        df = filter_by_date(df, args.from_date, args.to_date)

        # Set timezone and date format (vectorized)
        df["time"] = pd.to_datetime(df["time"] + constants.TIME_OFFSET, unit="ns")

        # Clean type column
        # Ensure mime type is string; default to text/plain
        if "type" in df.columns:
            df["type"] = df["type"].fillna("text/plain").astype("string")

    # Remove duplicate messages (happens with links sometimes)
    df = df.drop_duplicates(subset=["text", "sender", "time"])

    # Some messages show as null text even if they really do have text
    # See comment on helper function for more
    # Only decode attributed body where text is missing
    if "attributed_body" in df.columns:
        _mask = df["text"].isna()
        if _mask.any():
            df.loc[_mask, "text"] = df.loc[_mask, "attributed_body"].apply(
                helpers.decode_message_attributedbody
            )
    del df["attributed_body"]

    # Sort by date (sometimes the order gets messed up)
    # not sorting for now because
    # need to check that times are real and not just filled in as all right now (for csv)
    # df.sort_values(by="time", inplace=True)

    return df


def build_df_from_csv(args):
    if not os.path.isfile(args.csv_file_path):
        raise Exception(f"File not found at {args.csv_file_path}")

    # keep_default_na=False prevents empty string from being read as NaN
    df = pd.read_csv(args.csv_file_path, keep_default_na=False)

    # Make sure necessary columns are there
    for column in ["text", "sender"]:
        if column not in df.columns:
            raise Exception(f"Please make sure to include a {column} column in the csv")

    # Clean time column
    if "time" in df.columns:
        # Parse dates vectorized; fallback to now for invalids
        try:
            df["time"] = pd.to_datetime(df["time"], errors="coerce")
        except Exception:
            df["time"] = pd.NaT
        df["time"] = df["time"].fillna(pd.Timestamp.now())
    else:
        # default to using now for all dates
        df["time"] = pd.Timestamp.now()

    # Trim dataframe based on date constraints
    df = filter_by_date(
        df,
        args.from_date,
        args.to_date,
        use_seconds=False,
    )

    # Clean type column
    if "type" in df.columns:
        df["type"] = df["type"].fillna("text/plain").astype("string")
    else:
        df["type"] = "text/plain"

    return df


def get_chat_members(df, args):
    if args.csv:
        chat_members = list(set(df["sender"]))
    else:
        chat_ids = helpers.get_chat_ids()[args.name]
        chat_members = list(set(sql.get_chat_members(chat_ids)))
    for member in chat_members:
        if any(char.isdigit() for char in member):
            if args.group:
                error_msg = f"Please add contacts for every member of {args.name}"
            else:
                error_msg = f"Please add {member} as a contact"
            raise Exception(error_msg)

    return chat_members


def filter_by_date(df, from_date, to_date, use_seconds=True):
    offset = constants.TIME_OFFSET

    if use_seconds:
        # df['time'] is numeric nanoseconds; bounds are ns as well
        start = helpers.date_to_time(from_date, end_of_day=False) if from_date else None
        end = helpers.date_to_time(to_date, end_of_day=True) if to_date else None
        if start is not None:
            df = df[df["time"] >= (start - offset)]
        if end is not None:
            df = df[df["time"] <= (end - offset)]
    else:
        # df['time'] is datetime64
        start = helpers.parse_date(from_date) if from_date else None
        end = helpers.parse_date(to_date) if to_date else None
        if start is not None:
            df = df[df["time"] >= start]
        if end is not None:
            df = df[df["time"] <= end]

    return df
