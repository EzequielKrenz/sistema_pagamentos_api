import time

from app.database import SessionLocal, criar_tabelas
from app.services.notification_service import processar_eventos_pendentes

INTERVALO_SEGUNDOS = 5


def executar_worker():
    criar_tabelas()
    print("Worker de notificações iniciado. Pressione CTRL+C para parar.")
    while True:
        db = SessionLocal()
        try:
            quantidade = processar_eventos_pendentes(db)
            if quantidade:
                print(f"Eventos de preço processados: {quantidade}")
        finally:
            db.close()
        time.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    executar_worker()
