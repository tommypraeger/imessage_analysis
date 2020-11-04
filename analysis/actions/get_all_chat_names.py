import json
import analysis.utils.sql as sql


def main():
    chat_names = sql.get_all_chat_names()
    return json.dumps(chat_names, ensure_ascii=False)
