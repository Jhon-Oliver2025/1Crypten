import React from 'react';
import './Header.css';

const Header = ({ signals }) => {
  const totalSignals = signals.length;
  const buySignals = signals.filter(signal => signal.type.toUpperCase() === 'LONG').length;
  const sellSignals = signals.filter(signal => signal.type.toUpperCase() === 'SHORT').length;

  return (
    <div className="header-container">
      <h1 className="header-title">Sinais Ativos</h1>
      <div className="header-stats">
        <div className="stat-item">
          <span className="stat-label">Total de Sinais:</span>
          <span className="stat-value">{totalSignals}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Compra:</span>
          <span className="stat-value buy">{buySignals}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Venda:</span>
          <span className="stat-value sell">{sellSignals}</span>
        </div>
      </div>
    </div>
  );
};

export default Header;