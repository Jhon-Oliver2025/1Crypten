import React from 'react';
import SignalsWrapper from './SignalsWrapper';
import './SignalsContainer.css';

const SignalsContainer = ({ signals }) => {
  return (
    <div className="signals-container">
      <SignalsWrapper signals={signals} />
    </div>
  );
};

export default SignalsContainer;