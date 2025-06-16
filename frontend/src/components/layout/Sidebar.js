import React from 'react';
import { Link /*, useNavigate*/ } from 'react-router-dom'; // Removido: 'useNavigate' importado mas não usado
import { useDispatch } from 'react-redux';
import { logout } from '../../store/slices/authSlice';
import logo from '../../assets/logo2.0.png';
import './Sidebar.css';

const Sidebar = ({ isOpen, onToggle }) => {
  const dispatch = useDispatch();
  // const navigate = useNavigate(); // Removido: 'navigate' declarado mas não usado

  const handleLogout = () => {
    dispatch(logout());
    localStorage.removeItem('token');
    window.location.href = '/';  // Alterado para garantir redirecionamento completo
  };

  return (
    <>
      <div className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="logo-container">
          <img src={logo} alt="KryptoN Trading Bot" className="logo" />
        </div>
        
        <nav className="nav-menu">
          <Link to="/signals" className="nav-item">  {/* Alterado de "/" para "/signals" */}
            <i className="fas fa-home"></i>
            <span>Sinais</span>
          </Link>
          <Link to="/dashboard" className="nav-item">
            <i className="fas fa-chart-line"></i>
            <span>Dashboard</span>
          </Link>
          <Link to="/settings" className="nav-item">
            <i className="fas fa-cog"></i>
            <span>Configurações</span>
          </Link>
          <Link to="/support" className="nav-item">
            <i className="fas fa-headset"></i>
            <span>Suporte</span>
          </Link>
          <Link to="/profile" className="nav-item">
            <i className="fas fa-user"></i>
            <span>Minha Conta</span>
          </Link>
          
          <button onClick={handleLogout} className="nav-item logout-button">
            <i className="fas fa-sign-out-alt"></i>
            <span>Sair</span>
          </button>
        </nav>
      </div>
      
      <button className="sidebar-toggle" onClick={onToggle}>
        <i className={`fas fa-${isOpen ? 'times' : 'bars'}`}></i>
      </button>
    </>
  );
};

export default Sidebar;