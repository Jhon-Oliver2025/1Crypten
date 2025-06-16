import React from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo2.0.png';
import './LPage.css';

const LPage = () => {
  const navigate = useNavigate();

  return (
    <div className="lpage-container">
      <div className="overlay">
        <div className="content">
          <img src={logo} alt="KryptoN Logo" className="logo" />
          <button 
            className="enter-button"
            onClick={() => navigate('/login')}
          >
            Entrar
          </button>
        </div>
      </div>
    </div>
  );
};

export default LPage;