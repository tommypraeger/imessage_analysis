# iMessage Analysis

This README is a work in progress.

## Prerequisites
- Mac
- Python 3

## Installation
- `$ git clone https://github.com/tommypraeger/imessage_analysis.git`
- `$ cd imessage_analysis`
- `$ pip install -r requirements.txt`

## Setup

### Filling `user_data.py`
You need to replace the data in user_data.py with data for your computer. You need to fill in the 4 variables that exist in that file:
#### `USERNAME`

This is the name of the user on your computer. You can figure it out by running this from the command line:

`$ pwd | cut -d/ -f3`

This should print out the username (which is probably something similar to your actual name).

#### `CHAT_IDS`
#### `CONTACT_ID_TO_NAME`
#### `CONTACT_NAME_TO_ID`

- System Preferences > Security and Privacy > Privacy > Full Disk Access > give Terminal (or wherever you're running the script from) full disk access

## Usage
- `python3 imessage_analysis.py NAME flags`
- info for each flag

## Contributing
- tests
- more functions
- restructuring

## Acknowledgements
[This](https://stmorse.github.io/journal/iMessage.html) was very useful in learning how to do this and I used some code from it. I would recommend checking it out if you're interested in doing something similar.
