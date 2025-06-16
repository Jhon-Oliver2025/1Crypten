import React from 'react';
import Header from './Header';
import SignalsList from './SignalsList';
import './SignalsWrapper.css';

const SignalsWrapper = ({ signals }) => {
  return (
    <div className="signals-wrapper">
      <div className="signals-content">
        <Header signals={signals} />
        <SignalsList signals={signals} />
      </div>
    </div>
  );
};

export default SignalsWrapper;