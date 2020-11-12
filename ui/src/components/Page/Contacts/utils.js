import { postFetch, verifySuccessOrAlert } from '../utils';

const addContact = (name, number) => {
  postFetch('add_contact', {
    name,
    number
  }).then(response => response.json())
    .then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err))
};

const addGroup = (name) => {
  postFetch('add_contact', {
    name,
    group: ''
  }).then(response => response.json())
    .then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err))
};

const editContact = (name, oldName, number) => {
  postFetch('delete_contact', {
    name,
    number,
    'old-name': oldName
  }).then(response => response.json())
    .then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err))
};

const editGroup = (name, oldName) => {
  postFetch('delete_contact', {
    name,
    group: '',
    'old-name': oldName
  }).then(response => response.json())
    .then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err))
};

const deleteContact = (name) => {
  postFetch('delete_contact', {
    name
  }).then(response => response.json())
    .then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err))
};

const deleteGroup = (name) => {
  postFetch('delete_contact', {
    name,
    group: ''
  }).then(response => response.json())
    .then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err))
};

export {
  addContact,
  addGroup,
  editContact,
  editGroup,
  deleteContact,
  deleteGroup
};
