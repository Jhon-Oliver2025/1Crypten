import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import SignalsContainer from '../components/SignalsContainer';
import LPage from '../screens/LPage';
import Login from '../screens/LoginScreen';
import MaintenancePage from '../components/MaintenancePage';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/login" />;
  }
  return children;
};

const AppRoutes = ({ signals }) => {
  const token = localStorage.getItem('token');

  return (
    <React.Suspense fallback={<div>Carregando...</div>}>
      <Routes>
        <Route path="/" element={token ? <Navigate to="/signals" /> : <LPage />} />
        <Route path="/login" element={token ? <Navigate to="/signals" /> : <Login />} />
        <Route 
          path="/signals" 
          element={
            <ProtectedRoute>
              <SignalsContainer signals={signals} />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <MaintenancePage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/settings" 
          element={
            <ProtectedRoute signals={signals}>
              <MaintenancePage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/support" 
          element={
            <ProtectedRoute signals={signals}>
              <MaintenancePage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/profile" 
          element={
            <ProtectedRoute signals={signals}>
              <MaintenancePage />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </React.Suspense>
  );
};

export default AppRoutes;