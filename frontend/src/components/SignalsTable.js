import React, { useState, useEffect } from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import { getSignals } from '../services/signalsService';

function SignalsTable() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSignals = async () => {
      try {
        const data = await getSignals();
        setSignals(data);
        setError(null);
      } catch (err) {
        setError('Erro ao carregar sinais');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchSignals();
    const interval = setInterval(fetchSignals, 5000); // Atualiza a cada 5 segundos

    return () => clearInterval(interval);
  }, []);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Par</TableCell>
            <TableCell>Tipo</TableCell>
            <TableCell>Preço Entrada</TableCell>
            <TableCell>Alvo</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Qualidade</TableCell>
            <TableCell>Classificação</TableCell>
            <TableCell>Estratégia</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {signals.map((signal) => (
            <TableRow key={signal.symbol}>
              <TableCell>{signal.symbol}</TableCell>
              <TableCell>
                <Chip
                  icon={signal.type === 'LONG' ? <TrendingUpIcon /> : <TrendingDownIcon />}
                  label={signal.type}
                  color={signal.type === 'LONG' ? 'success' : 'error'}
                  variant="outlined"
                />
              </TableCell>
              <TableCell>{signal.entry_price}</TableCell>
              <TableCell>{signal.target_price}</TableCell>
              <TableCell>
                <Chip label={signal.status} color="primary" />
              </TableCell>
              <TableCell>{signal.quality_score}</TableCell>
              <TableCell>{signal.signal_class}</TableCell>
              <TableCell>{signal.strategy_info}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default SignalsTable;