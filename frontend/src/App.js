import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { getSignals } from './services/signalsService';
import MainLayout from './components/layout/MainLayout';
import Header from './components/Header';
import AppRoutes from './routes/AppRoutes';
import '@fortawesome/fontawesome-free/css/all.min.css';
import './App.css';

function App() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSignals = async () => {
      try {
        const data = await getSignals();
        setSignals(data);
      } catch (error) {
        console.error('Erro ao carregar sinais:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSignals();
    const interval = setInterval(fetchSignals, 60000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="loading">Carregando sinais...</div>;
  }

  return (
    <Router>
      <MainLayout>
        <div className="app">
          <AppRoutes signals={signals} />
        </div>
      </MainLayout>
    </Router>
  );
}

export default App;