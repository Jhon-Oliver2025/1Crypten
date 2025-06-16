from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/sinais_lista.csv')
def get_signals_csv():
    return send_file('sinais_lista.csv', mimetype='text/csv')

if __name__ == '__main__':
    print("\n=== KryptoN Trading Bot API ===")
    print("Servidor API iniciado na porta 5001")
    print("Endpoint: http://localhost:5001/sinais_lista.csv")
    app.run(port=5001)