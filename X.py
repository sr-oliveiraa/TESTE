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



from bs4 import BeautifulSoup
import requests

def analise_elementos_pagina(url):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        codigo_fonte = resposta.text

        # Parseia o conteúdo HTML
        soup = BeautifulSoup(codigo_fonte, 'html.parser')

        # Obtém elementos da página
        links = soup.find_all('a')
        imagens = soup.find_all('img')
        formularios = soup.find_all('form')
        scripts = soup.find_all('script')

        # Exibe informações sobre os elementos encontrados
        print(f"Links encontrados ({len(links)}):")
        for link in links:
            print(f"  - {link.get('href')}")

        print(f"\nImagens encontradas ({len(imagens)}):")
        for imagem in imagens:
            print(f"  - {imagem.get('src')}")

        print(f"\nFormulários encontrados ({len(formularios)}):")
        for formulario in formularios:
            print(f"  - {formulario}")

        print(f"\nScripts encontrados ({len(scripts)}):")
        for script in scripts:
            print(f"  - {script.get('src')}")

    except requests.exceptions.RequestException as err:
        print(f"Erro na requisição HTTP: {err}")

# Exemplo de uso:
url_alvo = 'https://exemplo.com'
analise_elementos_pagina(url_alvo)


from bs4 import BeautifulSoup
import requests

def reconhecimento_frameworks_front_end(url):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        codigo_fonte = resposta.text

        # Parseia o conteúdo HTML
        soup = BeautifulSoup(codigo_fonte, 'html.parser')

        # Encontra todos os scripts na página
        scripts = soup.find_all('script')

        frameworks_front_end = set()

        # Identifica frameworks front-end com base nos scripts
        for script in scripts:
            src = script.get('src')
            if src:
                # Exemplo: Verifica se o script faz referência a biblioteca jQuery
                if 'jquery' in src.lower():
                    frameworks_front_end.add('jQuery')

                # Adicione mais verificações conforme necessário para outros frameworks

        # Exibe frameworks front-end identificados
        if frameworks_front_end:
            print("Frameworks Front-End Identificados:")
            for framework in frameworks_front_end:
                print(f" - {framework}")
        else:
            print("Nenhum framework front-end identificado.")

    except requests.exceptions.RequestException as err:
        print(f"Erro na requisição HTTP: {err}")

# Exemplo de uso:
url_alvo = 'https://exemplo.com'
reconhecimento_frameworks_front_end(url_alvo)


import re
import requests

def detectar_vulnerabilidades_seguranca(url):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        codigo_fonte = resposta.text

        # Detecção de Injeção de SQL
        padrao_injecao_sql = re.compile(r'\b(union|select|insert|update|delete|alter|create)\b', re.IGNORECASE)
        resultados_injecao_sql = padrao_injecao_sql.findall(codigo_fonte)

        # Detecção de XSS (Cross-Site Scripting)
        padrao_xss = re.compile(r'<\s*script\s*>\s*.*<\s*/\s*script\s*>', re.IGNORECASE)
        resultados_xss = padrao_xss.findall(codigo_fonte)

        # Exibe resultados
        if resultados_injecao_sql:
            print("Possíveis Vulnerabilidades de Injeção de SQL Detectadas:")
            for resultado in resultados_injecao_sql:
                print(f" - '{resultado}'")

        if resultados_xss:
            print("Possíveis Vulnerabilidades de XSS (Cross-Site Scripting) Detectadas:")
            for resultado in resultados_xss:
                print(f" - '{resultado}'")

        if not resultados_injecao_sql and not resultados_xss:
            print("Nenhuma vulnerabilidade de segurança detectada.")

    except requests.exceptions.RequestException as err:
        print(f"Erro na requisição HTTP: {err}")

# Exemplo de uso:
url_alvo = 'https://exemplo.com'
detectar_vulnerabilidades_seguranca(url_alvo)


from scapy.all import sniff, IP

def monitorar_trafego_rede(tempo_monitoramento=10):
    pacotes_capturados = []

    # Função chamada para cada pacote capturado
    def processar_pacote(pacote):
        # Exibe informações básicas sobre o pacote IP
        if IP in pacote:
            pacote_info = {
                'Origem': pacote[IP].src,
                'Destino': pacote[IP].dst,
                'Protocolo': pacote[IP].proto
            }
            pacotes_capturados.append(pacote_info)

    # Captura pacotes durante o tempo especificado
    sniff(prn=processar_pacote, timeout=tempo_monitoramento)

    # Exibe informações sobre os pacotes capturados
    print(f"{'='*20} Pacotes Capturados {'='*20}")
    for idx, pacote_info in enumerate(pacotes_capturados, 1):
        print(f"Pacote {idx}: {pacote_info}")

# Exemplo de uso:
tempo_monitoramento = 10  # Tempo em segundos
monitorar_trafego_rede(tempo_monitoramento)


import csv
import json

def exportar_resultados(resultados, formato='csv'):
    """
    Exporta os resultados para o formato especificado.

    Parâmetros:
    - resultados: Lista de resultados a serem exportados.
    - formato: Formato de exportação desejado ('csv', 'json' ou 'html').
    """

    if formato not in ['csv', 'json', 'html']:
        print(f"Formato '{formato}' não suportado para exportação.")
        return

    nome_arquivo = f'resultados_exportados.{formato}'

    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_saida:
            if formato == 'csv':
                campo_nomes = resultados[0].keys() if resultados else []
                escritor_csv = csv.DictWriter(arquivo_saida, fieldnames=campo_nomes)
                escritor_csv.writeheader()
                escritor_csv.writerows(resultados)

            elif formato == 'json':
                json.dump(resultados, arquivo_saida, indent=2, ensure_ascii=False)

            elif formato == 'html':
                # Formato HTML personalizado - adaptar conforme necessário
                arquivo_saida.write('<html><body>\n')
                arquivo_saida.write('<h2>Resultados Exportados</h2>\n')
                for resultado in resultados:
                    arquivo_saida.write(f'<p>{resultado}</p>\n')
                arquivo_saida.write('</body></html>')

            print(f"Resultados exportados para {nome_arquivo} no formato {formato}.")

    except Exception as e:
        print(f"Erro durante a exportação: {e}")

# Exemplo de uso:
resultados_exemplo = [{'Origem': '192.168.0.1', 'Destino': '8.8.8.8', 'Protocolo': 6},
                      {'Origem': '10.0.0.1', 'Destino': '8.8.4.4', 'Protocolo': 17}]

exportar_resultados(resultados_exemplo, formato='csv')
exportar_resultados(resultados_exemplo, formato='json')
exportar_resultados(resultados_exemplo, formato='html')

