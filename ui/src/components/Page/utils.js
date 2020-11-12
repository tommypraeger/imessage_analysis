const buildPostBody = (obj) => {
  return JSON.stringify({ 'args': obj });
};

const verifySuccessOrAlert = (response) => {
  if ('errorMessage' in response) {
    alert(response['errorMessage']);
  }
};

const getFetch = (action) => {
  return fetch(`http://localhost:5000/api/v1/${action}`)
};

const postFetch = (action, body) => {
  return fetch(`http://localhost:5000/api/v1/${action}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: buildPostBody(body)
  })
};

export {
  buildPostBody,
  verifySuccessOrAlert,
  getFetch,
  postFetch
}