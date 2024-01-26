import requests
from bs4 import BeautifulSoup
from scapy.all import sniff, IP
import jsbeautifier

def obter_codigo_fonte(url):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.text
    except requests.exceptions.RequestException as err:
        print(f"Erro na requisição HTTP: {err}")
        return None

def capturar_e_processar_pacotes(qtd_pacotes=10):
    def processar_pacote(pacote):
        if IP in pacote:
            print(f"IP Origem: {pacote[IP].src}, IP Destino: {pacote[IP].dst}")

    sniff(prn=processar_pacote, count=qtd_pacotes)

def descompilar_javascript(codigo_minificado):
    try:
        return jsbeautifier.beautify(codigo_minificado)
    except Exception as e:
        print(f"Erro na descompilação do JavaScript: {e}")
        return None

def reconhecimento_tecnologia(url):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()

        cabecalhos = resposta.headers
        print("Cabeçalhos HTTP:")
        for chave, valor in cabecalhos.items():
            print(f"{chave}: {valor}")

        soup = BeautifulSoup(resposta.text, 'html.parser')
        tecnologias = identificar_tecnologias(soup)

        print("\nTecnologias Identificadas:")
        if tecnologias:
            for tecnologia in tecnologias:
                print(tecnologia)
        else:
            print("Nenhuma tecnologia identificada.")

    except requests.exceptions.RequestException as err:
        print(f"Erro na requisição HTTP: {err}")

def identificar_tecnologias(soup):
    tecnologias = []

    # Exemplo: Identificando o uso do jQuery
    if soup.find("script", {"src": "https://code.jquery.com/jquery-3.6.0.min.js"}):
        tecnologias.append("jQuery")

    # Adicione mais verificações conforme necessário para outras tecnologias

    return tecnologias

# Exemplos de uso:

# Obtém e exibe o código fonte de uma URL
url_alvo = 'https://exemplo.com'
codigo_fonte = obter_codigo_fonte(url_alvo)
if codigo_fonte:
    print(codigo_fonte)

# Captura e processa pacotes da rede
capturar_e_processar_pacotes(qtd_pacotes=5)

# Descompila código JavaScript minificado
codigo_minificado = "function hello(){console.log('Hello, World!');}"
codigo_descompilado = descompilar_javascript(codigo_minificado)
if codigo_descompilado:
    print(codigo_descompilado)

# Reconhecimento de tecnologia em uma página web
reconhecimento_tecnologia(url_alvo)
