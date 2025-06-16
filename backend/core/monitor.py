import threading
import time
import os
import traceback  # Add traceback import
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union
from binance.client import Client
from colorama import Fore, Style, init
from tabulate import tabulate
from tqdm import tqdm
from .database import Database
from .technical_analysis import TechnicalAnalysis
from .telegram_notifier import TelegramNotifier
from .gerenciar_sinais import GerenciadorSinais
from threading import Thread
import pandas as pd  # Adicione esta linha no topo do arquivo junto com os outros imports

# Initialize colorama
init()

class Monitor(Thread):
    VERSION = "7.6.0"
    
    def __init__(self):
        super().__init__()
        print("\n" + "="*70)
        print(f"🤖 Iniciando K-10 Bot v{self.VERSION}")
        print("="*70)
        
        from config import server
        
        self.db = Database()
        self.gerenciador = GerenciadorSinais()
        self.analyzer = TechnicalAnalysis()
        self.binance = Client()
        self.check_interval = 60
        self._monitor_running = True
        self._is_running = False
        self.daemon = True
        
        # Get Telegram credentials from config
        telegram_token = server.config.get('TELEGRAM_TOKEN')
        telegram_chat_id = server.config.get('TELEGRAM_CHAT_ID')
        
        self.notifier = TelegramNotifier(telegram_token, telegram_chat_id)
        if self.notifier.test_connection():
            print("✅ Telegram configurado com sucesso!")
        else:
            print("⚠️ Aviso: Telegram não configurado corretamente")
            # Remover a linha self.notifier = None  # Este é o problema principal
            
        self.stats = {
            'wins': 0,
            'losses': 0,
            'total_pairs': 0
        }
        print("✅ Sistema inicializado com sucesso!\n")

    def get_current_price(self, symbol: str) -> Optional[float]:
        """Obtém o preço atual de um par"""
        try:
            ticker = self.binance.futures_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            print(f"❌ Erro ao buscar preço de {symbol}: {e}")
            return None

    def calcular_variacao(self, entrada: float, atual: float, tipo: str) -> float:
        """Calcula a variação percentual do preço"""
        if tipo.upper() == 'LONG':
            return ((atual - entrada) / entrada) * 100
        return ((entrada - atual) / entrada) * 100

    def monitor_loop(self):
        """Loop principal de monitoramento"""
        try:
            sinais_abertos = self.gerenciador.processar_sinais_abertos()
            if not sinais_abertos.empty:
                print("\n[MONITOR] 📊 MONITORAMENTO DE SINAIS ATIVOS")
                print("="*50)
                table_data = []
                for _, sinal in sinais_abertos.iterrows():
                    try:
                        symbol = str(sinal['symbol'])
                        preco_atual = self.get_current_price(symbol)
                        if not preco_atual:
                            continue

                        entry_time = pd.to_datetime(sinal['entry_time'])
                        horas_ativas = (datetime.now() - entry_time).total_seconds() / 3600

                        variacao = self.calcular_variacao(
                            float(sinal['entry_price']),
                            preco_atual,
                            str(sinal['type'])
                        )

                        cor = Fore.GREEN if variacao > 0 else Fore.RED
                        table_data.append([
                            f"{Fore.CYAN}{symbol}{Style.RESET_ALL}",
                            f"{Fore.YELLOW}{sinal['type']}{Style.RESET_ALL}",
                            f"{cor}{variacao:+.2f}%{Style.RESET_ALL}",
                            f"{Fore.WHITE}{horas_ativas:.1f}h{Style.RESET_ALL}"
                        ])

                    except Exception as e:
                        print(f"❌ Erro ao processar sinal: {e}")
                        continue

                if table_data:
                    print(tabulate(
                        table_data,
                        headers=[
                            f'{Fore.CYAN}Par{Style.RESET_ALL}',
                            f'{Fore.YELLOW}Tipo{Style.RESET_ALL}',
                            f'{Fore.WHITE}Variação{Style.RESET_ALL}',
                            f'{Fore.WHITE}Tempo{Style.RESET_ALL}'
                        ],
                        tablefmt='grid'
                    ))
                print("="*50 + "\n")
            else:
                print("[INFO] Nenhum sinal ativo para monitorar")
            
            time.sleep(self.check_interval)
                
        except Exception as e:
            print(f"[ERROR] ❌ Erro no loop de monitoramento: {e}")
            print(f"[TRACE] {traceback.format_exc()}")
            time.sleep(30)

    def run(self):
        """Método principal da thread"""
        print("\n" + "="*70)
        print(f"🚀 INICIANDO MONITORAMENTO DE MERCADO - v{self.VERSION}")  # Adicionado versão
        print("="*70)
        self._is_running = True
        
        # --- Início da Edição ---
        # Variável para controlar se a limpeza diária já foi feita hoje
        self._last_cleanup_day = None
        # --- Fim da Edição ---

        while self._monitor_running:
            try:
                print("\n" + "="*70)
                now = datetime.now() # Obter a hora atual
                print(f"⏰ {now.strftime('%d/%m/%Y %H:%M:%S')}")
                print(f"[INFO] 🔄 Iniciando novo ciclo de verificação")  # Adicionado prefixo
                print("="*70)
                
                # --- Início da Edição ---
                # Verificar se é hora de fazer a limpeza diária (próximo da meia-noite)
                # Executa a limpeza entre 00:00 e 00:05
                if now.hour == 0 and now.minute < 5 and self._last_cleanup_day != now.date():
                    print("\n[CLEANUP] 🧹 Executando limpeza diária de sinais abertos do dia anterior...")
                    self.gerenciador.limpar_sinais_abertos_do_dia_anterior()
                    self._last_cleanup_day = now.date() # Marcar que a limpeza foi feita hoje
                    print("[CLEANUP] ✅ Limpeza diária concluída.")
                # --- Fim da Edição ---

                print("\n[SCAN] 📡 Escaneando mercado...")  # Adicionado prefixo
                novos_sinais = self.analyzer.scan_market(verbose=True)
                
                if novos_sinais:
                    print(f"\n[ALERT] ✨ {len(novos_sinais)} NOVOS SINAIS ENCONTRADOS!")  # Adicionado prefixo
                    print("-"*40)
                    for sinal in novos_sinais:
                        print(f"[SIGNAL] 📊 {sinal['symbol']} - {sinal['type']} @ {sinal['entry_price']}")  # Adicionado prefixo
                        if self.notifier:
                            # --- Início da Edição ---
                            # Passar o quality_score para o send_signal
                            self.notifier.send_signal(
                                sinal['symbol'],
                                sinal['type'],
                                float(sinal['entry_price']),
                                sinal.get('quality_score', 0), # Adicionado quality_score
                                sinal.get('entry_timeframe', '4h'), # Corrigido para entry_timeframe
                                sinal.get('target_price') # Adicionado target_price
                            )
                            # --- Fim da Edição ---
                    print("-"*40)
                else:
                    print("[INFO] Nenhum novo sinal encontrado")  # Nova mensagem
                
                self.monitor_loop()
                
                print("\n[WAIT] ⏳ AGUARDANDO PRÓXIMO CICLO")  # Adicionado prefixo
                print(f"[INFO] ⏰ Próxima verificação em {self.check_interval} segundos")  # Adicionado prefixo
                print("="*70)
                
                for i in range(self.check_interval, 0, -1):
                    if not self._monitor_running:
                        break
                    print(f"\r⌛ Aguardando: {i:3d}s", end="")
                    time.sleep(1)
                print("\r" + " "*50)
                
            except Exception as e:
                print(f"\n❌ ERRO NO CICLO: {e}")
                if not self._monitor_running:
                    break
                time.sleep(5)
        
        print("\n" + "="*70)
        print("✅ MONITORAMENTO ENCERRADO")
        print("="*70 + "\n")

    def stop(self):
        """Para o monitoramento"""
        print("🛑 Parando monitoramento...")
        self._monitor_running = False
        self._is_running = False
        if self.is_alive():
            self.join(timeout=2)  # Espera até 2 segundos pela thread terminar

def start_monitoring():
    """Função para iniciar o monitoramento em background"""
    try:
        monitor = Monitor()  # Removido os parâmetros
        monitor.start()  # Inicia a thread
        print("✅ Monitoramento iniciado com sucesso!")
        return monitor
    except Exception as e:
        print(f"❌ Erro ao iniciar monitoramento: {e}")
        return None

if __name__ == "__main__":
    monitor = Monitor()
    monitor.start()