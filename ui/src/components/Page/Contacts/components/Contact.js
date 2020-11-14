import React, { useState } from 'react';
import EditContactModal from './EditContactModal';
import EditGroupChatModal from './EditGroupChatModal';
import { deleteContact, deleteGroup } from '../utils';
import { formatNumber } from '../../utils';

const Contact = ({ name, number, allPhoneNumbers, allChatNames }) => {
  const [editContactModalOpen, setEditContactModalOpen] = useState(false);
  const [editGroupChatModalOpen, setEditGroupChatModalOpen] = useState(false);

  return (
    <React.Fragment>
      <EditContactModal
        open={editContactModalOpen}
        setOpen={setEditContactModalOpen}
        name={name}
        number={number}
        allPhoneNumbers={allPhoneNumbers}
      />
      <EditGroupChatModal
        open={editGroupChatModalOpen}
        setOpen={setEditGroupChatModalOpen}
        name={name}
        allChatNames={allChatNames}
      />
      <li
        className='contact'
        onClick={() => {
          if (number) {
            setEditContactModalOpen(true);
          } else {
            setEditGroupChatModalOpen(true);
          }
        }}
      >
        <p className={number ? 'contact-name' : 'group-chat-name'}>
          {name}
        </p>
        {number ? <p className='contact-number'>{formatNumber(number)}</p> : ''}
        <p
          className='x-btn'
          onClick={(e) => {
            e.stopPropagation();
            if (number) {
              deleteContact(name);
            } else {
              deleteGroup(name);
            }
          }}
        >
          &#x2715;
        </p>
      </li>
    </React.Fragment>
  )
};

export default Contact;
