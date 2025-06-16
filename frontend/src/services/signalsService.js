import axios from 'axios';

export const getSignals = async () => {
  try {
    const response = await axios.get('http://localhost:5001/sinais_lista.csv', {
      headers: {
        'Content-Type': 'text/csv'
      }
    });
    
    const lines = response.data.split('\n');
    const headers = lines[0].split(',');
    const signals = lines.slice(1)
      .filter(line => line.trim())
      .map(line => {
        const values = line.split(',');
        return {
          symbol: values[0],
          type: values[1],
          entry_price: parseFloat(values[2]),
          entry_time: values[3],
          target_price: parseFloat(values[4]),
          target_exit_time: values[5],
          status: values[6],
          quality_score: parseFloat(values[10]),
          signal_class: values[11],
          strategy_info: values[15]
        };
      })
      // Ordenando os sinais por data mais recente
      .sort((a, b) => {
        const dateA = new Date(a.entry_time.replace(/ /, 'T'));
        const dateB = new Date(b.entry_time.replace(/ /, 'T'));
        return dateB - dateA;
      });

    return signals;
  } catch (error) {
    console.error('Erro ao buscar sinais:', error);
    throw error;
  }
};