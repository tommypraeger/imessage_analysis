import { Line } from 'react-chartjs-2';
const LineGraph = ({ data }) => {
  return (
    <Line
      data={data}
      options={{
        title: {
          display: true,
          text: 'Messages Sent Over Time',
          fontSize: 24,
          fontStyle: 'normal'
        }
      }}
    />
  );
}

export default LineGraph;