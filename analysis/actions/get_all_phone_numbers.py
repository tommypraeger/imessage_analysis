import json
import analysis.utils.sql as sql


def main():
    phone_numbers = sql.get_all_phone_numbers()
    return json.dumps(phone_numbers)
