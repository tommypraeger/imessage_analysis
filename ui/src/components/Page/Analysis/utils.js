import { postFetch } from '../utils';

const buildArgs = (contactName, func, funcArgs, group) => {
  const args = {
    name: contactName,
  };

  if (func === 'all_functions') {
    args['all-functions'] = '';
  } else {
    args.function = func;
  }

  Object.assign(args, funcArgs);

  if (group) {
    args.group = '';
  }

  return args;
};

const runAnalysis = (
  contactName, func, funcArgs, group, setFetchesInProgress, setResponse
) => {
  setResponse({});
  const args = buildArgs(contactName, func, funcArgs, group);
  postFetch('analysis', args, setFetchesInProgress)
    .then(response => setResponse(response))
    .catch(err => console.log(err))
    .finally(() => setFetchesInProgress(fetches => fetches - 1));
};

export {
  runAnalysis
};
