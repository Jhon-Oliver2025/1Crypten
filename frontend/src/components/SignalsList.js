import React, { useMemo } from 'react';
import SignalCard from './SignalCard';
import './SignalsList.css';

const SignalsList = ({ signals }) => {
  const sortedSignals = useMemo(() => {
    return [...signals].sort((a, b) => {
      // Convertendo string de data para timestamp
      const dateA = new Date(a.entry_time.replace(' ', 'T'));
      const dateB = new Date(b.entry_time.replace(' ', 'T'));
      return dateB - dateA;
    });
  }, [signals]);

  return (
    <div className="signals-container">
      <div className="signals-grid">
        {sortedSignals.map((signal) => (
          <SignalCard 
            key={`${signal.symbol}-${signal.entry_time}`} 
            signal={signal} 
          />
        ))}
      </div>
    </div>
  );
};

export default SignalsList;