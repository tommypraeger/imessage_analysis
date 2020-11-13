import { postFetch, verifySuccessOrAlert } from '../utils';
import { createFilterOptions } from '@material-ui/lab/Autocomplete';

const addContact = (name, number) => {
  postFetch('add_contact', {
    name,
    number
  }).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const addGroup = (name) => {
  postFetch('add_contact', {
    name,
    group: ''
  }).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const editContact = (name, oldName, number) => {
  postFetch('edit_contact', {
    name,
    number,
    'old-name': oldName
  }).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const editGroup = (name, oldName) => {
  postFetch('edit_contact', {
    name,
    group: '',
    'old-name': oldName
  }).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const deleteContact = (name) => {
  postFetch('delete_contact', {
    name
  }).then(response => verifySuccessOrAlert(response))
    .catch(err => console.log(err));
};

const deleteGroup = (name) => {
  postFetch('delete_contact', {
    name,
    group: ''
  }).then(response => verifySuccessOrAlert(response))
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
