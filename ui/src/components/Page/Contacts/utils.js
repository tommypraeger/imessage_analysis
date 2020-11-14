import { postFetch, verifySuccessOrAlert } from '../utils';
import { createFilterOptions } from '@material-ui/lab/Autocomplete';

const addContact = (name, number, setFetchesInProgress) => {
  postFetch('add_contact', {
    name,
    number
  }, setFetchesInProgress).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const addGroup = (name, setFetchesInProgress) => {
  postFetch('add_contact', {
    name,
    group: ''
  }, setFetchesInProgress).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const editContact = (name, oldName, number, setFetchesInProgress) => {
  postFetch('edit_contact', {
    name,
    number,
    'old-name': oldName
  }, setFetchesInProgress).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const editGroup = (name, oldName, setFetchesInProgress) => {
  postFetch('edit_contact', {
    name,
    group: '',
    'old-name': oldName
  }, setFetchesInProgress).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const deleteContact = (name, setFetchesInProgress) => {
  postFetch('delete_contact', {
    name
  }, setFetchesInProgress).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const deleteGroup = (name, setFetchesInProgress) => {
  postFetch('delete_contact', {
    name,
    group: ''
  }, setFetchesInProgress).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const phoneNumberFilterOptions = createFilterOptions({
  stringify: option => `${option.number}${option.formatted}`
});


export {
  addContact,
  addGroup,
  editContact,
  editGroup,
  deleteContact,
  deleteGroup,
  phoneNumberFilterOptions
};
