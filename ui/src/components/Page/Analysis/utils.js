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

const buildArgs = (
  contactName,
  func,
  funcArgs,
  outputType,
  category,
  group,
  csv,
  startDate,
  endDate
) => {
  const args = {
    name: contactName,
    export: ''
  };

  args.function = func;

  Object.assign(args, funcArgs);

  args[outputType] = '';

  if (category) {
    args.category = category;
  }

  if (group) {
    args.group = '';
  } else if (csv) { // Don't set csv if a group chat is named 'messages.csv' lol
    args.csv = '';
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
  outputType,
  category,
  group,
  csv,
  startDate,
  endDate,
  setFetchesInProgress,
  setResponse
) => {
  setResponse({});
  const args = buildArgs(contactName, func, funcArgs, outputType, category, group, csv, startDate, endDate);
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

const addArg = (setFuncArgs, key, val) => {
  const newArg = {}
  newArg[key] = val;
  setFuncArgs(args => Object.assign(
    {},
    args,
    newArg
  ));
};

const removeArg = (setFuncArgs, key) => {
  setFuncArgs(args => {
    const newArgs = Object.assign({}, args);
    delete newArgs[key];
    return newArgs;
  });
};

const getCategories = (func, graphIndividual, setCategories, setCategory) => {
  const args = {
    function: func
  }
  if (graphIndividual) {
    args['graph-individual'] = ''
  }

  setCategories([]);
  postFetch('get_categories', args)
    .then(response => {
      const categories = JSON.parse(response);
      setCategories(categories);
      setCategory(categories[0]);
    })
    .catch(err => console.log(err));
}

export {
  runAnalysis,
  makeTableNice,
  addArg,
  removeArg,
  getCategories
};
