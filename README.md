# iMessage Analysis

## Prerequisites
- Mac
  - If you are not using a Mac and/or don't want to access the messages database on your Mac, you can provide messages in a csv format.
- Python 3.13 (Install from [here](https://www.python.org/downloads/))
- Node.js 22 (Install from [here](https://nodejs.org/en/))
- If you want to access messages from your Mac, set up permissions to access your messages database:
  - Open System Preferences > Security and Privacy > Privacy > Full Disk Access > and give Terminal (or a Terminal replacement, such as [iTerm2](https://iterm2.com/)) full disk access

## Installation and Setup
Open up Terminal (or wherever you gave permissions in the prerequisites), and then run the following:
- `git clone https://github.com/tommypraeger/imessage_analysis.git`
- `cd imessage_analysis`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python3 install.py`
  - If you are not using a Mac and/or don't want to access the messages database on your Mac, pass the `--skip-mac-setup` flag. e.g. `python3 install.py --skip-mac-setup`

If you are having an issue, make sure the prerequisites have been met.
To verify your installations of Python and Node.js, you can run:
- `python3 --version` and it should print something like `Python 3.13.0`
- `node -v` and it should print something like `v22.12.0`

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

Choose which contact or group chat to run analysis, choose the function to run, set any other required arguments, and optionally set start and end dates. Then click Analyze. Depending on the function, a table or graph will be shown. If a table is shown, you can sort by any of the columns by clicking on the column header.


### Using a CSV
**To use a CSV of messages, you can place a CSV file at the root of the `imessage_analysis` directory (i.e. the directory that the `run.sh` file is in).** The directory limitation is for security reasons (when choosing a file from a browser, the browser does not have access to the absolute path).

The CSV file must contain at least the following columns:
- A column titled `text`, which contains the text of the message
- A column titled `sender`, which contains the name of the person that sent the message

You may optionally also include a column titled `time`, which contains the time of the message. The time must be in one of the following formats, where `mm` is the month as 2 digits, `dd` is the day as 2 digits, `yyyy` is the year as 4 digits, `HH` is the hour on a 24-hour clock as 2 digits, `MM` is the minutes as 2 digits, and `SS` is the seconds as 2 digits:
- `mm/dd/yyyy`
  - e.g `12/31/2020`
- `mm/dd/yyyy HH:MM:SS`
  - e.g. `12/31/2020 23:59:59`
- `yyyy/mm/dd`
  - e.g. `2020-12-31`
- `yyyy/mm/dd HH:MM:SS`
  - e.g. `2020-12-31 23:59:59`

If fractions of a second are included, they will be ignored.

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

### Running Tests
- Active the virtual environment: `source venv/bin/activate`
- Run pytest: `pytest`

## Notes

### Functions

#### Total
This is the total number of messages sent by each person. It also shows what percent of the total messages each person has sent.

#### Frequency
This is a graph of the number of messages over time. You can select between graphing by the number of messages per day, per week, per month, or per year. You may also select whether to graph each chat member individually, or just graph the total messages for each time period.

One future feature I may consider is allowing graphing of other functions besides just total messages. This could turn graphs into an alternative to tables rather a completely separate function.

#### Reactions Sent
This is the total number of iMessage reactions each person sends, along with how many of the total reactions they send. It also shows how many of each kind of reaction they send, along with what proportion each reaction is of the all of the reactions they send. The current iMessage reactions are:
- Like
- Love
- Dislike
- Laugh
- Emphasis
- Question
- Custom Emoji

#### Reactions Received
This is the total number of iMessage reactions each person receives, broken out by reaction type. It also shows what percentage of the total reactions each person receives.

#### Reaction Matrix
This shows how many reactions each person receives from every other person, broken down by reaction type. Rows are receivers and columns are reactors, so you can see who tends to react to whom.

#### Starters
This is how many times each person in a chat has "started the conversation". I define this as sending a new message that is not an iMessage reaction a certain amount of time after the last message has been sent. You can edit this amount of time (default 60 minutes). I also show what percentage of the conversations are started by each person.

#### Participation
How many conversations each person participates in, plus participation rate. You can set the conversation gap in minutes to control how conversations are grouped.

#### Solo Conversations
How often a member starts a conversation that no one else joins. Uses the same configurable conversation gap as Starters.

#### Participation Correlation
Pairwise correlation of conversation participation between members. Produces a table (not graphable) showing correlations for each pair of members; optionally exclude reactions from participation.

#### Word/Phrase
This is how many messages include a certain word or phrase that you enter. You have the option of making the search case-sensitive or case-insensitive i.e. whether I should ignore case. You also have the option to search separate words. For example, if you choose to search separate words, then "tom" will not match "tomorrow", but if you choose not to, it will. Punctuation is ignored in the message unless there is punctuation in the search term.You can also choose to provide a [RegEx](https://regexr.com/) input. If you choose to use RegEx, your choices about case-sensitivity and word separation are ignored.

Only the total number of messages that contain the search term is shown, not how many times the search term actually appears i.e a single message can only count once, no matter how many times it contains the search term.

A possible future feature is showing some of the matching messages to provide context.

#### Message Series
This is how many series of messages a person sends. A series of messages is defined as a string of messages all send my one person, where no message is sent longer than a certain amount of time of the last one (this is prevent the last message of a conversation and the first message of the next conversation from being counted in the same "messages series", if both messages were sent by the same person). This amount of time is configurable. I also show the average number of messages in each series.

#### Word Count
This is the average number of words in each message.

#### Word Length
This is the average length of each word sent.

#### CVA+ (Conversational Value Added)
A composite score blending volume and efficiency metrics (messages sent, conversations started/participated, reactions, word volume, and solo-conversation rate), with adjustable weights for volume vs. efficiency.

#### Attachments
This is how many messages are attachments. Attachments are defined as anything that isn't plain text.

#### Links
This is how many messages include links.

#### Emoji
This is how many messages include emoji.

#### Games
This is how many messages are iMessage games. I approximate whether a message is an iMessage game by checking if the file type is a JPEG image and the text of the message is iMessage game text. I also show how many times each person starts a game and what percentage of games they start.

#### Tweets
This is how many messages are shared tweets.

#### All Caps
This shows how many messages are completely capitalized. A message must contain letters (i.e. not just emoji or an attachment) to be considered to be all caps.

#### File Type
This shows how many messages are of a specific file type. The only file types that I made searchable are listed above in the Using a CSV section.

## Contributing
- Python formatting is done using [black](https://github.com/psf/black) using the default configuration. Run `black .` from the application directory to formatting before committing.
- Improve testing. Currently, there are just basic unit tests for the analysis functions to make sure they work.
- Add more functions. Be creative!

## Acknowledgements
[This](https://stmorse.github.io/journal/iMessage.html) was very useful in learning how to do this and I used some code from it. I would recommend checking it out if you're interested in doing something similar.
