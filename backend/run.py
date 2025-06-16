from core.monitor import Monitor
from core.database import Database
from core.technical_analysis import TechnicalAnalysis
import threading

if __name__ == "__main__":
    # Inicializar componentes
    monitor = Monitor()
    
    # Inicia o monitoramento em background
    monitor_thread = threading.Thread(target=monitor.start, daemon=True)
    monitor_thread.start()
    
    print("\n=== KryptoN Trading Bot ===")
    print("Monitoramento iniciado...")
    
    try:
        while True:
            # Mantém o programa principal rodando
            threading.Event().wait()
    except KeyboardInterrupt:
        print("\n🛑 Encerrando o sistema...")
        monitor.stop()