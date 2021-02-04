import analysis.utils.sql as sql


def main():
    try:
        sql.test_db()
        return 'Database has sufficient permissions.'
    except Exception as e:
        ret = ''
        ret = add_string_on_new_line(ret, str(e))
        ret = add_string_on_new_line(ret, 'There is an error with accessing the database.')
        ret = add_string_on_new_line(ret, 'Do the following:')
        ret = add_string_on_new_line(ret, 'Open System Preferences')
        ret = add_string_on_new_line(ret, 'Go to Security and Privacy')
        ret = add_string_on_new_line(ret, 'Go to Privacy')
        ret = add_string_on_new_line(ret, 'Go to Full Disk Access')
        ret = add_string_on_new_line(
            ret, 'Give Terminal (or whatever application you\'re running this from) Full Disk Access')
        ret = add_string_on_new_line(
            ret, 'More info here: https://spin.atomicobject.com/2020/05/22/search-imessage-sql/')
        return ret


def add_string_on_new_line(str1, str2):
    return str1 + '\n' + str2
