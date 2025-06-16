# System imports
import os
import sys
import threading
import time
import pytz
import pandas as pd
from datetime import datetime, timedelta
import cryptocompare
import traceback
from dash.exceptions import PreventUpdate
# --- Início da Edição ---
from dash.dependencies import Input, Output, State # Importar State
# --- Fim da Edição ---

from flask import Flask
from dash import Dash, html, dcc
# --- Início da Edição ---
# from dash.dependencies import Input, Output # Remover esta linha duplicada
# --- Fim da Edição ---

from config import server
from pages.login import create_login_layout, init_login_callbacks
from pages.dashboard import create_dashboard_layout, init_callbacks
from pages.landing_page import create_landing_layout
from core.monitor import Monitor
from core.database import Database
from core.technical_analysis import TechnicalAnalysis
# --- Início da Edição ---
from ui.components.signals_container import create_signals_container # Importar a função para recriar o container
# --- Fim da Edição ---
from flask_login import current_user
import threading
import signal
import sys
import os

# Inicializar componentes
db = Database()
analyzer = TechnicalAnalysis()
monitor = Monitor()

def signal_handler(sig, frame):
    print("\n🛑 Encerrando o sistema...")
    if monitor:
        monitor.stop()
        try:
            # Força encerramento após 3 segundos
            threading.Timer(3, lambda: os._exit(0)).start()
        except:
            os._exit(0)
    else:
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Configuração do Dash
app = Dash(
    __name__,
    server=True,
    url_base_pathname='/',
    suppress_callback_exceptions=True,
    external_stylesheets=[
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
    ],
    prevent_initial_callbacks=True
)

# Vincula o Dash ao servidor Flask
app.init_app(server)

# Adicionar debug para callbacks registrados
def print_registered_callbacks():
    print("\nCallbacks Registrados:")
    for output in app.callback_map:
        print(f"- {output}")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return create_landing_layout()
    elif pathname == '/login':
        return create_login_layout()
    elif pathname == '/dashboard':
        return create_dashboard_layout()
    return create_landing_layout()

# Inicializar callbacks
init_callbacks(app, db, analyzer)
init_login_callbacks(app)

# --- Início da Edição ---
# Callback para o botão Reiniciar Sinais
@app.callback(
    Output('signals-container-div', 'children'), # Alvo: o container de sinais
    Input('restart-signals-button', 'n_clicks'), # Gatilho: clique no botão
    State('url', 'pathname') # Estado: URL atual para garantir que estamos no dashboard
)
def restart_signals(n_clicks, current_pathname):
    if n_clicks is None or n_clicks == 0:
        # Previne a execução no carregamento inicial ou se não houver cliques
        raise PreventUpdate

    # Verifica se o usuário está na página do dashboard
    if current_pathname != '/dashboard':
        raise PreventUpdate

    print("\n🔄 Botão 'Reiniciar Sinais' clicado. Limpando e gerando novos sinais...")

    # 1. Limpar sinais existentes
    db.clear_signals()

    # 2. Rodar o scan de mercado para gerar novos sinais
    # Nota: O scan_market salva os sinais diretamente no CSV via TechnicalAnalysis -> GerenciadorSinais -> Database
    new_signals_list = analyzer.scan_market(verbose=True) # Executa o scan

    # 3. Ler os novos sinais do banco de dados (CSV)
    # A função create_signals_container espera um DataFrame ou lista de dicionários.
    # O scan_market retorna uma lista de dicionários, então podemos usar isso diretamente.
    # Se o scan_market retornar None ou uma lista vazia, passamos uma lista vazia.
    signals_data_for_display = new_signals_list if new_signals_list else []

    # 4. Recriar e retornar o conteúdo do container de sinais com os novos dados
    # Precisamos retornar APENAS os filhos do container, não o container inteiro,
    # pois o Output targets o 'children' do 'signals-container-div'.
    # A função create_signals_container retorna o html.Div com ID 'signals-container-div'.
    # Precisamos extrair os filhos desse Div.
    updated_container = create_signals_container(signals_data_for_display)

    # Retorna os filhos do Div principal retornado por create_signals_container
    return updated_container.children

# --- Fim da Edição ---


# Imprimir callbacks registrados
print_registered_callbacks()

if __name__ == '__main__':
    try:
        print("\n📡 Iniciando thread de monitoramento...")
        # Agora o monitor já está inicializado
        monitor_thread = threading.Thread(target=monitor.start, daemon=True)
        monitor_thread.start()
        
        print("\n🌐 Iniciando servidor web...")
        server.run(host='0.0.0.0', debug=True, port=8050, use_reloader=False)
        
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        if monitor:
            monitor.stop()
        sys.exit(1)