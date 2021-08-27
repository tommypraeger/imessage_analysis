import { Line } from 'react-chartjs-2';

const LineGraph = ({ data, category }) => {
  return (
    <Line
      data={data}
      options={{
        title: {
          display: true,
          text: category,
          fontSize: 24,
          fontStyle: 'normal'
        }
      }}
    />
  );
}

export default LineGraph;