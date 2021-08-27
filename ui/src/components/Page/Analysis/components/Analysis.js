import { useEffect } from 'react';
import Loader from 'react-loader-spinner';
import { makeTableNice } from '../utils';
import LineGraph from './LineGraph';

const LoadingGif = () => (
  <div className='loading-gif'>
    <Loader
      type='Oval'
      color='#1982fc'
      height={200}
      width={200}
    />
  </div>
);

const Analysis = ({ response, category, fetchesInProgress, fetchSeconds }) => {
  useEffect(() => {
    makeTableNice();
  });

  if (fetchesInProgress > 0) {
    return (
      <div>
        <LoadingGif />
        {fetchSeconds < 3 ? '' : (
          <p className='center-content'>
            Request has been loading for {fetchSeconds} seconds
          </p>
        )}
      </div>
    );
  } else if (Object.keys(response).length === 0) {
    return <div />;
  } else {
    if ('htmlTable' in response) {
      return (
        <div
          id='analysis-table'
          dangerouslySetInnerHTML={{ __html: response.htmlTable }}
        />
      );
    } else if ('graphData' in response) {
      return (
        <div className='center-content'>
          <LineGraph data={response.graphData} category={category} />
        </div>
      );
    } else if ('errorMessage' in response) {
      return <p className='center-content'>{response.errorMessage}</p>;
    } else {
      return <div />;
    }
  }
};

export default Analysis;
