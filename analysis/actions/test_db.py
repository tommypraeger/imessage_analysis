from sqlite3 import OperationalError
import analysis.utils.sql as sql


def main():
    try:
        sql.test_db()
        return 0, "Database has sufficient permissions."
    except OperationalError:
        ret = "\n===================================\n\n"
        ret += "There was an error accessing the messages database.\n"

        ret += "\nIf you do not want to access the messages database, "
        ret += "you can pass --skip-mac-setup to the install.py script. "
        ret += "You would then only be able to use this program by providing a CSV of messages. "
        ret += "See the README for more details.\n"

        ret += "\nIf you are using a Mac and do want to access the messages database, do the following:\n"
        ret += "1. Open System Preferences\n"
        ret += "2. Go to Security and Privacy\n"
        ret += "3. Go to Privacy\n"
        ret += "4. Go to Full Disk Access\n"
        ret += str(
            "5. Give Terminal (or whatever application you're running this from) Full Disk Access, ",
        )
        ret += "and then run the install.py script again\n"
        ret += str(
            "\nMore info here: https://spin.atomicobject.com/2020/05/22/search-imessage-sql/\n",
        )
        ret += "\n===================================\n"
        return 1, ret
