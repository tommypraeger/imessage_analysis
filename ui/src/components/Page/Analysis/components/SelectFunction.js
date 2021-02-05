const SelectFunction = ({ setFunc }) => (
  <select
    className='select'
    defaultValue='none'
    onChange={(event) => setFunc(event.target.value)}
  >
    <option value='none' disabled={true}>Select a function</option>

    <option value='total'>
      Total: How many messages each person sends
    </option>

    <option value='frequency'>
      Frequency: Graph of message frequency over time
    </option>

    <option value='reaction'>
      Reactions: How many messages are iMessage reactions
    </option>

    <option value='convo_starter'>
      Starters: How many times each person starts the conversation
    </option>

    <option value='phrase'>
      Word/Phrase: How many messages include a certain word/phrase
    </option>

    <option value='message_series'>
      Message Series: How many series of consecutive messages each person sends
    </option>

    <option value='word_count'>
      Word Count: The average word count in each message
    </option>

    <option value='word_length'>
      Word Length: The average length of each word sent
    </option>

    <option value='attachment'>
      Attachments: How many messages are attachments
    </option>

    <option value='link'>
      Links: How many messages are links
    </option>

    <option value='emoji'>
      Emoji: How many messages include emoji
    </option>

    <option value='game'>
      Games: How many messages are iMessage games
    </option>

    <option value='tweet'>
      Tweets: How many messages are tweets
    </option>

    <option value='all_caps'>
      All Caps: How many messages are in all caps
    </option>

    <option value='mime_type'>
      File Type: How many messages are of a specific file type
    </option>

    <option value='all_functions'>
      All: All functions (except a few that require more input)
    </option>

  </select>
);

export default SelectFunction;
