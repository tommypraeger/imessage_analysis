import Loader from 'react-loader-spinner';

const LoadingGif = () => (
  <div className='loading-gif'>
    <Loader
      type="Oval"
      color="#1982fc"
      height={200}
      width={200}
    />
  </div>
);

const Analysis = ({ response, fetchesInProgress }) => {
  if (fetchesInProgress > 0) {
    return <LoadingGif />;
  } else if (Object.keys(response).length === 0) {
    return <div />;
  } else {
    if ('htmlTable' in response) {
      return (
        <div
          className='analysis-table'
          dangerouslySetInnerHTML={{ __html: response.htmlTable }}
        />
      );
    } else if ('imagePath' in response) {
      return <img src={response.imagePath} alt='Analysis Table' />;
    }
  }
};

export default Analysis;
