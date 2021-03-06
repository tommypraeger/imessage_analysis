import $ from 'jquery';
import 'datatables.net';
import 'datatables.net-dt/css/jquery.dataTables.css';
import { postFetch } from '../utils';

const formatDate = (date) => {
  let strDate = date.toLocaleString().split(',')[0];
  if (strDate.split('/')[0].length < 2) {
    strDate = `0${strDate}`;
  }
  if (strDate.split('/')[1].length < 2) {
    strDate = `${strDate.slice(0, 3)}0${strDate.slice(3)}`;
  }
  return strDate;
};

const buildArgs = (contactName, func, funcArgs, group, startDate, endDate) => {
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

  if (startDate) {
    args['from-date'] = formatDate(startDate);
  }

  if (endDate) {
    args['to-date'] = formatDate(endDate);
  }

  return args;
};

const runAnalysis = (
  contactName,
  func,
  funcArgs,
  group,
  startDate,
  endDate,
  setFetchesInProgress,
  setResponse
) => {
  setResponse({});
  const args = buildArgs(contactName, func, funcArgs, group, startDate, endDate);
  postFetch('analysis', args, setFetchesInProgress)
    .then(response => setResponse(response))
    .catch(err => console.log(err))
    .finally(() => setFetchesInProgress(fetches => fetches - 1));
};

const makeTableNice = () => {
  const table = $('#analysis-table').children('table');
  if (table.length > 0) {
    table.DataTable({
      paging: false,
      searching: false
    });
  }
};

export {
  runAnalysis,
  makeTableNice
};
