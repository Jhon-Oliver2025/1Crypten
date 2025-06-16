# System imports
import os
import sys
import time
import logging
import pandas as pd
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Core components
from core.database import Database
from core.technical_analysis import TechnicalAnalysis
from core.telegram_notifier import TelegramNotifier
from core.monitor import Monitor
from core.gerenciar_sinais import GerenciadorSinais

# API routes
from api.routes.auth import auth_bp
from api.routes.signals import signals_bp
from api.routes.settings import settings_bp
from api.routes.dashboard import dashboard_bp

# Configuração do Flask
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'sua-chave-secreta-aqui'
jwt = JWTManager(app)

# Registrando as rotas da API
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(signals_bp, url_prefix='/api/signals')
app.register_blueprint(settings_bp, url_prefix='/api/settings')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

class KryptonBot:
    def __init__(self):
        self.gerenciador = GerenciadorSinais()
        self.db = Database()
        self.analyzer = TechnicalAnalysis()
        
        # Configurações do Telegram
        from config import server
        telegram_token = server.config.get('TELEGRAM_TOKEN')
        telegram_chat_id = server.config.get('TELEGRAM_CHAT_ID')
        self.notifier = TelegramNotifier(telegram_token, telegram_chat_id)
        self.monitor = Monitor()
        
        # Configuração do logger
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def send_all_today_signals(self):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            signals_df = self.gerenciador.processar_sinais_abertos()
            today_signals = signals_df[signals_df['entry_time'].str.contains(today)]
            
            if today_signals.empty:
                self.logger.info("Nenhum sinal encontrado para hoje")
                return
                
            self.logger.info(f"Enviando {len(today_signals)} sinais para o Telegram")
            
            for _, signal in today_signals.iterrows():
                timeframe = signal.get('timeframe', '4h')
                quality_score = signal.get('quality_score', 90.0)
                    
                self.notifier.send_signal(
                    symbol=signal['symbol'],
                    signal_type=signal['type'],
                    price=float(signal['entry_price']),
                    timeframe=str(timeframe),
                    quality_score=quality_score
                )
                time.sleep(1)
                
            self.logger.info("✅ Todos os sinais foram enviados com sucesso")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar sinais: {e}")

    def test_telegram(self):
        """Testa a conexão com o Telegram"""
        try:
            result = self.notifier.test_connection()
            if result:
                self.logger.info("✅ Conexão com Telegram estabelecida com sucesso")
            else:
                self.logger.error("❌ Falha ao conectar com Telegram")
            return result
        except Exception as e:
            self.logger.error(f"❌ Erro ao testar Telegram: {e}")
            return False

    def cleanup(self):
        """Limpa recursos e encerra threads"""
        if self.monitor:
            self.monitor.stop()
            self.monitor.join(timeout=2)

    def initialize(self):
        """Inicializa todos os componentes do sistema"""
        try:
            if not self.gerenciador.verificar_integridade():
                self.logger.error("Falha na verificação de integridade")
                return False
                
            # Teste do Telegram durante a inicialização
            if not self.test_telegram():
                self.logger.warning("⚠️ Sistema iniciado, mas Telegram não está funcionando")
            
            self.gerenciador.limpar_sinais_antigos()
            self.gerenciador.migrar_sinais()
            
            # Send all today's signals
            self.send_all_today_signals()
            
            # Inicia monitoramento
            if hasattr(self.monitor, 'start'):
                self.monitor.start()
            
            # Registra handler de cleanup
            import atexit
            atexit.register(self.cleanup)
            
            self.logger.info("Sistema inicializado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao inicializar sistema: {e}")
            return False
            
    def check_system_status(self):
        """Verifica status de todos os componentes"""
        monitor_alive = hasattr(self.monitor, 'is_alive') and self.monitor.is_alive
        return {
            'sinais_file': os.path.exists('sinais_lista.csv'),
            'monitor': monitor_alive,
            'database': self.db.check_connection()
        }

# Instância global do bot
bot = KryptonBot()

if __name__ == '__main__':
    if bot.initialize():
        print("\n🚀 Iniciando servidor API...")
        print("\n📊 API disponível em: http://localhost:5000/api")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Falha ao inicializar o sistema")
        sys.exit(1)