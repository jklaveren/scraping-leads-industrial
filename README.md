# 🏭 Pipeline de Inteligência B2B: Extração e Automação Industrial

## 💎 Visão Geral do Projeto
Este repositório apresenta uma solução de ponta a ponta para a prospecção qualificada no setor industrial. O objetivo principal é transformar dados brutos e não estruturados da web em leads comerciais prontos para abordagem, eliminando o trabalho manual e aumentando a precisão dos dados de contato (CNPJ e E-mail).

---

## 🛠️ Desafios de Engenharia e Soluções Implementadas

### 1. Estratégia de Captura de Dados
Para evitar a complexidade e os bloqueios de extrações diretas em larga escala de motores de busca, optei por uma abordagem híbrida:
* **Ingestão de Dados:** Utilização de ferramentas de interface para coleta da massa bruta.
* **Processamento Python:** O núcleo da inteligência foi desenvolvido em Python para permitir total controle sobre a limpeza e o enriquecimento dos dados.

### 2. Mineração em Profundidade (Deep Scraping)
O maior desafio técnico foi a inconsistência estrutural dos sites industriais. Para resolver isso, o script `WebScraper.Py` foi desenhado com:
* **Crawling Heurístico:** O algoritmo identifica e navega em sublinks estratégicos (Contato, Institucional, Sobre) para localizar dados muitas vezes ocultos em rodapés.
* **Mecanismo de Fallback:** Implementação de rotina de busca automatizada em fontes secundárias para validar dados quando o site principal está inacessível.

### 3. Normalização e Higienização de Dados
* **Regex Pattern Matching:** Expressões regulares avançadas para extração de e-mails e formatação de CNPJs.
* **Tratamento de Strings:** Camada de limpeza que remove sufixos jurídicos (LTDA, S/A, ME), permitindo uma personalização de e-mail mais humana e assertiva.

### 4. Automação de Saída e Entregabilidade
Utilização do **Google Apps Script** (`scriptmail.js`) para o disparo final:
* **Reputação de IP:** Infraestrutura nativa do Google Workspace para garantir alta taxa de entregabilidade.
* **Controle de Fluxo:** Implementação de delays e logs em tempo real para monitorar a saúde da operação.

---

## 🏗️ Arquitetura Técnica
* **Core:** Python 3.x (Pandas, BeautifulSoup4, Requests)
* **Automação:** JavaScript (Google Apps Script)
* **Data Storage:** Excel / Google Sheets

## 📈 Resultados Alcançados
* **Eficiência:** Redução drástica no tempo de pesquisa manual.
* **Qualidade:** Filtro rigoroso para exportação de contatos verificados.
* **Escalabilidade:** Estrutura modular aplicável a diferentes nichos de mercado.
