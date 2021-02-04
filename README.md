# iMessage Analysis

## Prerequisites
- Mac (or you can use messages in a csv format, details below)
- Python 3.9 (Install from [here](https://www.python.org/downloads/))
- Node.js 14 (Install from [here](https://nodejs.org/en/))
- Permissions to access your messages database
  - To do this, open System Preferences > Security and Privacy > Privacy > Full Disk Access > and give Terminal (or a Terminal replacement, such as [iTerm2](https://iterm2.com/)) full disk access

## Installation and Setup
Open up Terminal (or wherever you gave permissions in the prerequisites), and then run the following:
- `cd Documents` or whichever your preferred directory for this stuff is
- `git clone https://github.com/tommypraeger/imessage_analysis.git`
- `cd imessage_analysis`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `python3 install.py`

If you are having an issue, make sure the prerequisites have been met.
To verify your installations of Python and Node.js, you can run:
- `python3 --version` and it should print something like `Python 3.9.1`
- `node -v` and it should print something like `v14.15.4`

If you did not give sufficient permissions on your messages database,
it should have printed the instructions again when you ran `python3 install.py`

## Usage
To start using, do:
- Run `./run.sh`
- Wait for the page to open in your browser

### Adding Contacts
Go to the Contacts page by clicking Contacts in the navigation bar at the top.

To add a group chat, click "+ Add Group Chat" and type in the name of your group chat, which should be able to be autofilled.
**Currently, I only support using group chats that are named. If you want to use a group chat that is unnamed, please give it a name.**
Make sure to add every member of the group chat as a contact before trying to run analysis on it.

To add one of your contacts, click "+ Add Contact" and type in the contact's name as you would like it to be displayed for name, and their phone number. Their number will only be listed if you have messages with them. You can type in the name either without any punctuation (i.e. like 1234567890) or in the format (xxx) xxx-xxxx.

### Running Analysis
Go to the Analysis page by clicking Analysis in the navigation bar at the top.

Choose which contact or group chat to run analysis, choose the function to run, set any other required arguments, and optionally set start and end dates. Then click Analyze.


### Using a CSV
**To use a CSV of messages, you can place a CSV file called `messages.csv` at the root of the `imessage_analysis` directory (i.e. the directory that the `run.sh` file is in.** When choosing who to run analysis for, choose `messages.csv`.

The CSV file must contain at least the following columns:
- A column titled `text`, which contains the text of the message
- A column titled `sender`, which contains the name of the person that sent the message

You may optionally also include a column titled `time`, which contains the time of the message. The time must be in the format `mm/dd/yyyy` or `mm/dd/yyyy HH:MM:SS`, where `mm` is the month as 2 digits, `dd` is the day as 2 digits, `yyyy` is the year as 4 digits, `HH` is the hour on a 24-hour clock as 2 digits, `MM` is the minutes as 2 digits, and `SS` is the seconds as 2 digits. Please be consistent with which date format you use.

Example dates for the two formats: `01/01/2020` and `01/01/2020 18:30:45`.

You may optionally also include a column titled `type`, which contains the mime type of the message. The mime types should be limited to the following list:
- image/png
- image/jpeg
- image/gif
- image/heic
- video/mp4
- video/quicktime
- text/plain
- text/markdown
- text/csv
- text/vcard
- audio/mpeg
- audio/amr
- audio/x-m4a
- text/x-python-script
- text/x-vlocation
- text/html
- text/css
- application/pdf
- application/json
- application/x-tex
- application/x-javascript
- application/x-iwork-keynote-sffkey
- application/vnd.openxmlformats-officedocument.wordprocessingml.document
- application/zip
- application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
- application/vnd.ms-excel
- application/epub+zip
- application/x-yaml
- application/vnd.openxmlformats-officedocument.presentationml.presentation
- message/rfc82
## Contributing
- Add unit tests to make sure this actually works.
- Add more functions. Be creative!

## Acknowledgements
[This](https://stmorse.github.io/journal/iMessage.html) was very useful in learning how to do this and I used some code from it. I would recommend checking it out if you're interested in doing something similar.
