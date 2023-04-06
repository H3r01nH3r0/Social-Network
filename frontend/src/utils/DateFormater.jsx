import React from 'react';

const DateTimeFormat = ({ datetimeString }) => {
    const date = new Date(datetimeString);

    const year = date.getFullYear();
    const month = date.toLocaleString('en-US', { month: 'long' }).toLowerCase().slice(0, 3);
    const day = String(date.getDate()).padStart(2, '0');

    const formattedDateTimeString = `${day} ${month} ${year}`;

    return (
        <span>{formattedDateTimeString}</span>
    );
};

export default DateTimeFormat;