import pandas as pd
from typing import Dict, Any, Optional, List
import os
from datetime import datetime
import traceback  # Adicionar esta linha no início do arquivo

class Database:
    def __init__(self):
        self.signals_file = 'sinais_lista.csv'
        self.config_file = 'config.csv'
        self.signal_columns = [
            'symbol', 'type', 'entry_price', 'entry_time',
            'target_price', 'target_exit_time', 'status', 'exit_price',
            'variation', 'result', 'quality_score', 'signal_class',
            'trend_score', 'alignment_score', 'market_score',
            'strategy_info', 'trend_timeframe', 'entry_timeframe'
        ]
        self._initialize_files()

    def _initialize_files(self) -> None:
        if not os.path.exists(self.signals_file):
            # Corrigido: usando pd.DataFrame com dict vazio
            df = pd.DataFrame({col: [] for col in self.signal_columns})
            df.to_csv(self.signals_file, index=False)
        
        if not os.path.exists(self.config_file):
            # Corrigido: usando pd.DataFrame com dict vazio
            df = pd.DataFrame({'key': [], 'value': []})
            df.to_csv(self.config_file, index=False)

    def check_connection(self) -> bool:
        try:
            df = pd.read_csv(self.signals_file)
            df.to_csv(self.signals_file, index=False)
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    def get_config(self, key: str) -> Optional[str]:
        try:
            df = pd.read_csv(self.config_file)
            value = df.loc[df['key'] == key, 'value'].iloc[0]
            return str(value)
        except Exception:
            return None

    def get_all_config(self):
        """Retorna todas as configurações"""
        try:
            df = pd.read_csv(self.config_file)
            return df.to_dict('records')
        except Exception:
            return {}

    def update_config(self, config_data):
        """Atualiza as configurações"""
        try:
            df = pd.DataFrame([config_data])
            df.to_csv(self.config_file, index=False)
            return True
        except Exception:
            return False

    def get_signal_by_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        try:
            df = pd.read_csv(self.signals_file)
            signal = df.loc[df['symbol'] == symbol].iloc[0]
            return signal.to_dict()
        except Exception:
            return None

    def _get_signal_class(self, quality_score: float) -> str:
        """Retorna a classificação do sinal baseado no quality_score"""
        if quality_score >= 90:
            return "⭐⭐⭐⭐⭐ (Muito Bom)"
        elif quality_score >= 80:
            return "⭐⭐⭐⭐ (Bom)"
        elif quality_score >= 70:
            return "⭐⭐⭐ (Regular)"
        elif quality_score >= 60:
            return "⭐⭐ (Básico)"
        return "❌ Score Insuficiente"

    def add_signal(self, signal: Dict[str, Any]) -> bool:
        try:
            print(f"Debug - Recebendo sinal: {signal}")
            
            # Converter o tipo do sinal para maiúsculo
            if 'type' in signal:
                if signal['type'].lower() == 'compra':
                    signal['type'] = 'LONG'
                elif signal['type'].lower() == 'venda':
                    signal['type'] = 'SHORT'
            
            # Garantir que o quality_score seja numérico
            if 'quality_score' in signal:
                try:
                    quality_score = float(signal['quality_score'])
                    signal['quality_score'] = quality_score
                    signal['signal_class'] = self._get_signal_class(quality_score)
                except (ValueError, TypeError):
                    print(f"❌ Erro ao converter quality_score: {signal['quality_score']}")
                    signal['quality_score'] = 0
                    signal['signal_class'] = "❌ Score Inválido"
            
            # Garantir que todas as colunas existam
            for col in self.signal_columns:
                if col not in signal:
                    signal[col] = ''
            
            # Remover colunas extras que não estão em signal_columns
            signal = {k: v for k, v in signal.items() if k in self.signal_columns}
            
            df = pd.read_csv(self.signals_file)
            
            # Verificar se o sinal já existe
            if not df.empty:
                existing_signal = df[
                    (df['symbol'] == signal['symbol']) & 
                    (df['status'] == 'OPEN')
                ]
                if not existing_signal.empty:
                    print(f"⚠️ Sinal já existe para {signal['symbol']}")
                    return False
            
            # Adicionar novo sinal
            new_df = pd.concat([df, pd.DataFrame([signal])], ignore_index=True)
            new_df.to_csv(self.signals_file, index=False)
            print(f"✅ Sinal salvo com sucesso para {signal['symbol']}")
            return True
            
        except Exception as e:
            print(f"❌ Erro detalhado ao adicionar sinal: {str(e)}")
            traceback.print_exc()
            return False

    def set_config(self, key: str, value: str) -> bool:
        """
        Salva uma configuração no arquivo CSV
        :param key: Chave da configuração
        :param value: Valor da configuração
        :return: True se salvou com sucesso, False caso contrário
        """
        try:
            # Lê o arquivo de configuração existente
            if os.path.exists(self.config_file):
                df = pd.read_csv(self.config_file)
            else:
                df = pd.DataFrame({'key': [], 'value': []})
            
            # Atualiza ou adiciona a configuração
            if key in df['key'].values:
                df.loc[df['key'] == key, 'value'] = value
            else:
                new_row = pd.DataFrame({'key': [key], 'value': [value]})
                df = pd.concat([df, new_row], ignore_index=True)
            
            # Salva as alterações
            df.to_csv(self.config_file, index=False)
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar configuração: {e}")
            return False

    def get_signals_by_date(self, date_str: Optional[str] = None) -> pd.DataFrame:
        """Get all signals from a specific date starting at 00:00"""
        try:
            df = pd.read_csv(self.signals_file)
            
            # Se não houver data fornecida, usa hoje
            if date_str is None:
                date_str = datetime.now().strftime('%Y-%m-%d')
            
            # Converte entry_time para datetime
            df['entry_time'] = pd.to_datetime(df['entry_time'])
            
            # Filtra sinais da data especificada
            date_start = pd.to_datetime(f"{date_str} 00:00:00")
            date_end = pd.to_datetime(f"{date_str} 23:59:59")
            
            # Garante que o retorno seja sempre um DataFrame
            filtered_df = pd.DataFrame(df[
                (df['entry_time'] >= date_start) & 
                (df['entry_time'] <= date_end)
            ].copy())
            
            return filtered_df
            
        except Exception as e:
            print(f"❌ Erro ao buscar sinais por data: {e}")
            return pd.DataFrame()

    def get_signals(self) -> pd.DataFrame:
        """Lê todos os sinais mantendo a formatação HTML"""
        try:
            df = pd.read_csv(self.signals_file)
            # Garante que signal_class seja lido como string
            if 'signal_class' in df.columns:
                df['signal_class'] = df['signal_class'].astype(str)
            return df
        except Exception as e:
            print(f"Error reading signals: {e}")
            return pd.DataFrame()