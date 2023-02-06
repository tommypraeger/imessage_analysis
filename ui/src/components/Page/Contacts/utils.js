import { postFetch, verifySuccessOrAlert } from "../utils";
import { createFilterOptions } from "@mui/material/Autocomplete";

const addContact = (name, number, setFetchesInProgress, setUpdateContacts) => {
  postFetch(
    "add_contact",
    {
      name,
      number,
    },
    setFetchesInProgress
  )
    .then((response) => verifySuccessOrAlert(response))
    .catch((err) => console.log(err))
    .then(() => setUpdateContacts((x) => x + 1))
    .finally(() => setFetchesInProgress((fetches) => fetches - 1));
};

const addGroup = (name, setFetchesInProgress, setUpdateContacts) => {
  postFetch(
    "add_contact",
    {
      name,
      group: "",
    },
    setFetchesInProgress
  )
    .then((response) => verifySuccessOrAlert(response))
    .catch((err) => console.log(err))
    .then(() => setUpdateContacts((x) => x + 1))
    .finally(() => setFetchesInProgress((fetches) => fetches - 1));
};

const editContact = (name, oldName, number, setFetchesInProgress, setUpdateContacts) => {
  postFetch(
    "edit_contact",
    {
      name,
      number,
      "old-name": oldName,
    },
    setFetchesInProgress
  )
    .then((response) => verifySuccessOrAlert(response))
    .catch((err) => console.log(err))
    .then(() => setUpdateContacts((x) => x + 1))
    .finally(() => setFetchesInProgress((fetches) => fetches - 1));
};

const editGroup = (name, oldName, setFetchesInProgress, setUpdateContacts) => {
  postFetch(
    "edit_contact",
    {
      name,
      group: "",
      "old-name": oldName,
    },
    setFetchesInProgress
  )
    .then((response) => verifySuccessOrAlert(response))
    .catch((err) => console.log(err))
    .then(() => setUpdateContacts((x) => x + 1))
    .finally(() => setFetchesInProgress((fetches) => fetches - 1));
};

const deleteContact = (name, setFetchesInProgress, setUpdateContacts) => {
  postFetch(
    "delete_contact",
    {
      name,
    },
    setFetchesInProgress
  )
    .then((response) => verifySuccessOrAlert(response))
    .catch((err) => console.log(err))
    .then(() => setUpdateContacts((x) => x + 1))
    .finally(() => setFetchesInProgress((fetches) => fetches - 1));
};

const deleteGroup = (name, setFetchesInProgress, setUpdateContacts) => {
  postFetch(
    "delete_contact",
    {
      name,
      group: "",
    },
    setFetchesInProgress
  )
    .then((response) => verifySuccessOrAlert(response))
    .catch((err) => console.log(err))
    .then(() => setUpdateContacts((x) => x + 1))
    .finally(() => setFetchesInProgress((fetches) => fetches - 1));
};

const phoneNumberFilterOptions = createFilterOptions({
  stringify: (option) => `${option.number}${option.formatted}`,
});

export {
  addContact,
  addGroup,
  editContact,
  editGroup,
  deleteContact,
  deleteGroup,
  phoneNumberFilterOptions,
};
