const buildPostBody = (obj) => {
  return JSON.stringify({ 'args': obj });
};

const verifySuccessOrAlert = (response) => {
  if ('errorMessage' in response) {
    alert(response['errorMessage']);
  }
};

const getFetch = (action, setFetchesInProgress) => {
  setFetchesInProgress(fetches => fetches + 1);
  return fetch(`http://localhost:5000/api/v1/${action}`)
    .then(response => response.json());
};

const postFetch = (action, body, setFetchesInProgress) => {
  setFetchesInProgress(fetches => fetches + 1);
  return fetch(`http://localhost:5000/api/v1/${action}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: buildPostBody(body)
  }).then(response => response.json());
};

const formatNumber = (number) => {
  const matches = number.match(/^\+([\d-]{0,5})?(\d{3})(\d{3})(\d{4})$/);
  if (matches) {
    const intlCode = ''; // (matches[1] ? '+1 ' : ''); // not putting intl code for now
    return [intlCode, '(', matches[2], ') ', matches[3], '-', matches[4]].join('');
  }
  return number;
};

const formatNumbers = (numbers) => {
  return numbers.map(number => (
    {
      number: number,
      formatted: formatNumber(number)
    }
  ));
};

export {
  buildPostBody,
  verifySuccessOrAlert,
  getFetch,
  postFetch,
  formatNumber,
  formatNumbers
}