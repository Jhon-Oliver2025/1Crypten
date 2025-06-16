import React from 'react';
import './SignalCard.css';

const SignalCard = ({ signal }) => {
  const isCompra = signal.type.toUpperCase() === 'LONG';
  const typeText = isCompra ? 'COMPRA' : 'VENDA';
  
  // Calcula a variação percentual
  const variationPercent = ((signal.target_price - signal.entry_price) / signal.entry_price * 100).toFixed(1);
  
  // Formata a data e hora
  const datetime = new Date(signal.entry_time);
  const formattedDate = datetime.toLocaleDateString('pt-BR');
  const formattedTime = datetime.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

  return (
    <div className={`signal-card ${isCompra ? 'compra' : 'venda'}`}>
      <div className="card-header">
        <div className="symbol">{signal.symbol}</div>
        <div className={`type-label ${isCompra ? 'compra' : 'venda'}`}>
          {typeText}
        </div>
      </div>

      <div className="premium-tag">Sinais Premium</div>
      
      <div className="price-info">
        <div className="price-row">
          <span className="price-label">💰 Entrada:</span>
          <span className="price-value">${signal.entry_price}</span>
        </div>
        
        <div className="price-row">
          <span className="price-label">🎯 Alvo:</span>
          <span className="price-value">${signal.target_price}</span>
          <span className={`variation ${isCompra ? 'compra' : 'venda'}`}>
            ({variationPercent}%)
          </span>
        </div>
      </div>

      <div className="timestamp">
        <span className="clock-icon">🕒</span>
        {`${formattedDate} ${formattedTime}`}
      </div>
    </div>
  );
};

export default SignalCard;