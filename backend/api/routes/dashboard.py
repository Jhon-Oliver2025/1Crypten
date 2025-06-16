from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from core.database import Database
from core.technical_analysis import TechnicalAnalysis
from core.gerenciar_sinais import GerenciadorSinais
import pandas as pd

dashboard_bp = Blueprint('dashboard', __name__)
db = Database()
gerenciador = GerenciadorSinais()

@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_dashboard_summary():
    try:
        signals_df = gerenciador.processar_sinais_abertos()
        
        if signals_df.empty:
            return jsonify({
                'total_signals': 0,
                'active_signals': 0,
                'status': 'no_signals'
            }), 200
            
        summary = {
            'total_signals': len(signals_df),
            'active_signals': len(signals_df[signals_df['status'] == 'active']),
            'long_positions': len(signals_df[signals_df['type'] == 'LONG']),
            'short_positions': len(signals_df[signals_df['type'] == 'SHORT']),
            'status': 'ok'
        }
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@dashboard_bp.route('/status', methods=['GET'])
@jwt_required()
def get_system_status():
    try:
        return jsonify({
            'database': db.check_connection(),
            'signals_file': gerenciador.verificar_integridade(),
            'analyzer': True
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500