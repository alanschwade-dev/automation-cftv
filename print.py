import requests
from requests.auth import HTTPDigestAuth
import os
from datetime import datetime
import schedule
import time

#Configuracoes
url = "http://10.1.1.6/cgi-bin/snapshot.cgi[?channel=1]"
url2 = "http://10.1.1.254/cgi-bin/snapshot.cgi?channel=1"
usuario = "xxx"
senha = "xxxx"
pasta_destino = os.path.join(os.path.expanduser("~"), "Documents", "Fotos Obras Coprel")
os.makedirs(pasta_destino, exist_ok=True)
pasta_destino2 = os.path.join(os.path.expanduser("~"), "Documents", "Fotos Obras Coprel", "Camera Secundaria")
os.makedirs(pasta_destino2, exist_ok=True)


def snapshot_camPrincipal():
    nome_arquivo = f"ObrasCam1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    caminho_completo = os.path.join(pasta_destino, nome_arquivo)
    
    try:
        resposta = requests.get(url, auth=HTTPDigestAuth(usuario, senha), timeout=5)
        resposta.raise_for_status()

        if "image" in resposta.headers.get("Content-Type", ""):
            with open(caminho_completo, "wb") as f:
                f.write(resposta.content)
            print(f"[{datetime.now()}] Snapshot salvo em: {caminho_completo}")
        else:
            print(f"[{datetime.now()}] ERRO: Resposta não é uma imagem.")

    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] ERRO: Não foi possível baixar a imagem: {e}")

def snapshot_camSecundaria():
    nome_arquivo = f"ObrasCam2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    caminho_completo = os.path.join(pasta_destino2, nome_arquivo)
    
    try:
        resposta = requests.get(url2, auth=HTTPDigestAuth(usuario, senha), timeout=5)
        resposta.raise_for_status()

        if "image" in resposta.headers.get("Content-Type", ""):
            with open(caminho_completo, "wb") as f:
                f.write(resposta.content)
            print(f"[{datetime.now()}] Snapshot secundario salvo em: {caminho_completo}")
        else:
            print(f"[{datetime.now()}] ERRO: Resposta não é na imagem 2.")

    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] ERRO: Não foi possível baixar a imagem 2: {e}")


#Horarios
schedule.every().day.at("08:00").do(snapshot_camPrincipal)
schedule.every().day.at("08:00").do(snapshot_camSecundaria)
schedule.every().day.at("12:00").do(snapshot_camPrincipal)
schedule.every().day.at("12:00").do(snapshot_camSecundaria)
schedule.every().day.at("16:00").do(snapshot_camPrincipal)
schedule.every().day.at("16:00").do(snapshot_camSecundaria)

#teste
#schedule.every().day.at("17:50").do(snapshot_camSecundaria)


print("Agendamento iniciado...")

#Loop para manter o script ativo
while True:
    schedule.run_pending()
    time.sleep(30)  # checa a cada 30 segundos
