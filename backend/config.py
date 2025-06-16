from flask import Flask
from flask_login import LoginManager

server = Flask(__name__)
server.config['SECRET_KEY'] = 'chave-secreta-krypton-2024'

# --- Início da Edição ---
# Adicionar chaves da API da Binance diretamente ao config do Flask
server.config['API_KEY'] = 'CBeEjFuDgfCCdAuyC9ITwP9cRd5mc4AIGaK8eWgDisEdzjdt32S2JflZwMLwIjFp'
server.config['API_SECRET'] = 'RS5p0K6l6802saRfE23erEZMtwoZu65GrAfBWP6r5BCAyrUasN4fQCGjS9UzB7Xk'
# --- Fim da Edição ---

# Telegram Configuration
server.config['TELEGRAM_TOKEN'] = "7690455274:AAHB64l8csWoE5UpV1Pnn9c8chJzd5sZTXQ"
server.config['TELEGRAM_CHAT_ID'] = "1249100206"

# Trading Configuration
server.config['TRADING'] = {
    'DEFAULT_TIMEFRAME': '4h',
    'MIN_VOLUME_USD': 500000,
    'MIN_SCORE': 7,
    'PREMIUM_SCORE': 8,

    'INDICATORS': {
        'RSI': {'window': 14, 'long_threshold': 30, 'short_threshold': 70},
        'EMA': {'fast': 9, 'slow': 21},
        'MACD': {'fast': 12, 'slow': 26, 'signal': 9},
        'BB': {'window': 20, 'std': 2},
        'SUPERTREND': {'period': 10, 'multiplier': 2.0}
    },

    'SCORE_WEIGHTS': {
        'trend_alignment': 2.0,
        'volume': 1.0,
        'momentum': 1.0,
        'pattern': 1.5,
        'correlation': 0.5
    }
}

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'  # type: ignore

@login_manager.user_loader
def load_user(user_id):
    class User:
        def __init__(self, username):
            self.id = username
            self.is_authenticated = True
            self.is_active = True
            self.is_anonymous = False

        def get_id(self):
            return str(self.id)

    if user_id == 'admin':
        return User(user_id)
    return None

# --- Início da Edição ---
# Remover a classe ServerConfig e sua instanciação
# class ServerConfig:
#     def __init__(self):
#         self.config = {
#             'API_KEY': 'CBeEjFuDgfCCdAuyC9ITwP9cRd5mc4AIGaK8eWgDisEdzjdt32S2JflZwMLwIjFp',
#             'API_SECRET': 'RS5p0K6l6802saRfE23erEZMtwoZu65GrAfBWP6r5BCAyrUasN4fQCGjS9UzB7Xk',
#             'TELEGRAM_TOKEN': 'YOUR_TELEGRAM_BOT_TOKEN',
#             'TELEGRAM_CHAT_ID': 'YOUR_TELEGRAM_CHAT_ID',
#         }

# server = ServerConfig() # Remover esta linha
# --- Fim da Edição ---