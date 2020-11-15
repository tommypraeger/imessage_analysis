import React, { useState } from 'react';
import AllCapsForm from './forms/AllCaps';
import AttachmentForm from './forms/Attachment';
import ConvoStarterForm from './forms/ConvoStarter';
import EmojiForm from './forms/Emoji';
import FrequencyForm from './forms/Frequency';
import GameForm from './forms/Game';
import LinkForm from './forms/Link';
import MessageSeriesForm from './forms/MessageSeries';
import MimeTypeForm from './forms/MimeType';
import PhraseForm from './forms/Phrase';
import ReactionForm from './forms/Reaction';
import TotalForm from './forms/Total';
import TweetForm from './forms/Tweet';
import WordCountForm from './forms/WordCount';
import WordLengthForm from './forms/WordLength';

const AnalysisPage = ({ contacts }) => {
  const [contactName, setContactName] = useState('');
  const [group, setGroup] = useState(false);

  const groupOptions = Object.keys(contacts).filter(name => contacts[name] === 'group')
    .map(name => (
      <option key={name} value={name}>
        {name}
      </option>
    ));
  const contactOptions = Object.keys(contacts).filter(name => contacts[name] !== 'group')
    .map(name => (
      <option key={name} value={name}>
        {name}
      </option>
    ));

  return (
    <div>
      <div className='select-contact'>
        <h2>Analysis for</h2>
        <select className='contact-select' defaultValue='none' onChange={(event) => {
          setContactName(event.target.value);
          if (contacts[event.target.value] === 'group') {
            setGroup(true);
          } else {
            setGroup(false);
          }
        }}>
          <option value='none' disabled={true}>Select a contact</option>
          <optgroup label='Group Chats'>
            {groupOptions}
          </optgroup>
          <optgroup label='Contacts'>
            {contactOptions}
          </optgroup>
        </select>
      </div>
    </div>
  );
};

export default AnalysisPage;
