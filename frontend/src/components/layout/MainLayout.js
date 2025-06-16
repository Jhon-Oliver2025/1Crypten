import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import './MainLayout.css';

const MainLayout = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const location = useLocation();
  const token = localStorage.getItem('token');
  const isAuthRoute = location.pathname === '/' || location.pathname === '/login';

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="layout">
      {token && !isAuthRoute && <Sidebar isOpen={isSidebarOpen} onToggle={toggleSidebar} />}
      <main className={`main-content ${token && !isAuthRoute ? 'with-sidebar' : ''}`}>
        {children}
      </main>
    </div>
  );
};

export default MainLayout;