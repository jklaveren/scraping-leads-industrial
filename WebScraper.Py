import pandas as pd
import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import urllib3

# Desabilita avisos de certificados SSL para sites industriais antigos
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuração de caminhos relativos ao local do script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_ENTRADA = os.path.join(BASE_DIR, "google.xlsx")
ARQUIVO_SAIDA = os.path.join(BASE_DIR, "carga_crm_limpa.xlsx")

def extrair_dados_contato(texto):
    """Localiza e-mails e CNPJs usando expressões regulares."""
    # Regex para E-mail (filtra arquivos de sistema/design)
    emails_raw = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', texto)
    blacklist = ['react', 'bootstrap', 'jquery', 'wix', 'png', 'jpg', 'svg', 'webp']
    emails = [e.lower() for e in emails_raw if not any(t in e.lower() for t in blacklist)]
    
    # Regex para CNPJ (Padrão brasileiro)
    cnpjs = re.findall(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto)
    
    return list(set(emails)), list(set(cnpjs))

def mineracao_profunda(url_base):
    """Navega na Home e páginas de contato para buscar dados ocultos."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    emails_finais, cnpjs_finais = set(), set()
    
    try:
        res = requests.get(url_base, timeout=12, headers=headers, verify=False)
        if res.status_code == 200:
            e, c = extrair_dados_contato(res.text)
            emails_finais.update(e)
            cnpjs_finais.update(c)
            
            # Busca links internos estratégicos
            soup = BeautifulSoup(res.text, 'html.parser')
            termos = ['contato', 'fale', 'sobre', 'quem', 'institucional', 'legal']
            
            for link in soup.find_all('a', href=True):
                if any(t in link.text.lower() or t in link['href'].lower() for t in termos):
                    url_int = urljoin(url_base, link['href'])
                    try:
                        res_int = requests.get(url_int, timeout=8, headers=headers, verify=False)
                        e, c = extrair_dados_contato(res_int.text)
                        emails_finais.update(e)
                        cnpjs_finais.update(c)
                        if emails_finais and cnpjs_finais: break
                    except: continue
                    
        return list(emails_finais), list(cnpjs_finais)
    except:
        return [], []

def busca_cnpj_externa(nome_empresa):
    """Fallback: Busca CNPJ via Google Search caso não esteja no site."""
    try:
        query = quote(f'CNPJ "{nome_empresa}"')
        url = f"https://www.google.com/search?q={query}"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        cnpjs = re.findall(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', res.text)
        return cnpjs[0] if cnpjs else ""
    except:
        return ""

def executar_pipeline():
    """Coordena o fluxo de extração, limpeza e enriquecimento."""
    if not os.path.exists(ARQUIVO_ENTRADA):
        print(f"Erro: Arquivo {ARQUIVO_ENTRADA} não encontrado.")
        return

    df = pd.read_excel(ARQUIVO_ENTRADA)
    # Normalização inicial de colunas vinda da extensão
    df = df.rename(columns={'qBF1Pd': 'Empresa', 'lcr4fd href': 'Website'}).copy()
    df = df.dropna(subset=['Empresa']).drop_duplicates(subset=['Empresa'])
    
    df['Email'], df['CNPJ'] = "", ""

    print(f"Iniciando Deep Scan em {len(df)} empresas...")

    for i, row in df.iterrows():
        empresa, url = row['Empresa'], row['Website']
        
        # Enriquecimento via Web Scraping
        if pd.notna(url) and 'google.com' not in str(url):
            url_alvo = url if str(url).startswith('http') else 'http://' + str(url)
            emails, cnpjs = mineracao_profunda(url_alvo)
            if emails: df.at[i, 'Email'] = ", ".join(emails[:2])
            if cnpjs: df.at[i, 'CNPJ'] = cnpjs[0]

        # Enriquecimento via Busca Externa (Fallback)
        if not df.at[i, 'CNPJ']:
            df.at[i, 'CNPJ'] = busca_cnpj_externa(empresa)

    # Limpeza final para o CRM
    df_crm = df[df['Email'] != ""].copy()
    df_crm['Empresa'] = df_crm['Empresa'].str.title().str.strip()
    
    df_crm[['Empresa', 'Email', 'CNPJ', 'Website']].to_excel(ARQUIVO_SAIDA, index=False)
    print(f"Sucesso! Arquivo gerado: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    executar_pipeline()