from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from core.gerenciar_sinais import GerenciadorSinais

signals_bp = Blueprint('signals', __name__)
gerenciador = GerenciadorSinais()

@signals_bp.route('/list', methods=['GET'])
@jwt_required()
def get_signals():
    signals_df = gerenciador.processar_sinais_abertos()
    signals = signals_df.to_dict('records') if not signals_df.empty else []
    return jsonify(signals), 200

@signals_bp.route('/<symbol>', methods=['GET'])
@jwt_required()
def get_signal(symbol):
    signals_df = gerenciador.processar_sinais_abertos()
    signal = signals_df[signals_df['symbol'] == symbol].to_dict('records')
    if signal:
        return jsonify(signal[0]), 200
    return jsonify({"error": "Signal not found"}), 404