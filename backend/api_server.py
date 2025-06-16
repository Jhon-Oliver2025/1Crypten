from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/sinais_lista.csv')
def get_signals_csv():
    return send_file('sinais_lista.csv', mimetype='text/csv')

# Adicione esta importação no início do arquivo, se ainda não existir
import os

if __name__ == '__main__':
    print("\n=== KryptoN Trading Bot API ===")
    {{ edit_1 }}
    # Obtém a porta da variável de ambiente PORT, usando 5001 como fallback para desenvolvimento local
    port = int(os.environ.get('PORT', 5001))
    # Roda o aplicativo Flask no endereço 0.0.0.0 e na porta obtida
    app.run(host='0.0.0.0', port=port)