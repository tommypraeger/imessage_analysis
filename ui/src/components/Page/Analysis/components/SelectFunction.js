const SelectFunction = ({ setFunc }) => (
  <select
    className='select'
    defaultValue='none'
    onChange={(event) => setFunc(event.target.value)}
  >
    <option value='none' disabled={true}>Select a function</option>

    <option value='all_functions'>
      All functions
    </option>

    <option value='all_caps'>
      How many messages are in all caps
    </option>

    <option value='attachment'>
      How many messages are attachments
    </option>

    <option value='convo_start'>
      How many times each person starts are conversation
    </option>

    <option value='emoji'>
      How many messages include emojis
    </option>

    <option value='frequency'>
      Graph of message frequency over time
    </option>

    <option value='game'>
      How many messages are iMessage games
    </option>

    <option value='link'>
      How many messages are links
    </option>

    <option value='message_series'>
      How many series of consecutive messages each person sends
    </option>

    <option value='mime_type'>
      How many messages are of a specific file type
    </option>

    <option value='phrase'>
      How many messages include a certain word/phrase
    </option>

    <option value='reaction'>
      How many messages are iMessage reactions
    </option>

    <option value='total'>
      How many messages each person sends
    </option>

    <option value='tweet'>
      How many messages are tweets
    </option>

    <option value='word_count'>
      The average word count in each message
    </option>

    <option value='word_length'>
      The average length of each word sent
    </option>
  </select>
);

export default SelectFunction;
