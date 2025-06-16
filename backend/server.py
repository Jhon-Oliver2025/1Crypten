from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/sinais_lista.csv')
def get_signals_csv():
    return send_file('sinais_lista.csv', mimetype='text/csv')

if __name__ == '__main__':
    app.run(port=5000)