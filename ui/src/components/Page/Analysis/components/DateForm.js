import DatePicker from "react-datepicker";

const DateForm = ({ startDate, endDate, setStartDate, setEndDate }) => {
  return (
    <div className="input-div">
      <p>Limit dates to...</p>
      <div className="date-input">
        <p>Start:</p>
        <DatePicker
          dateFormat="MM/dd/yyyy"
          selected={startDate}
          onChange={(date) => setStartDate(date)}
          placeholderText="No start limit"
          isClearable={true}
        />
      </div>
      <div className="date-input">
        <p>End:</p>
        <DatePicker
          dateFormat="MM/dd/yyyy"
          selected={endDate}
          onChange={(date) => setEndDate(date)}
          placeholderText="No end limit"
          isClearable={true}
        />
      </div>
    </div>
  );
};

export default DateForm;
