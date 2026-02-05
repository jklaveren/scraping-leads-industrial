🏭 Pipeline de Inteligência B2B: Extração e Automação Industrial
💎 Visão Geral do Projeto
Este repositório apresenta uma solução de ponta a ponta para a prospecção qualificada no setor industrial. O objetivo principal foi transformar dados brutos e não estruturados da web em leads comerciais prontos para abordagem, eliminando o trabalho manual e aumentando a precisão dos dados de contato (CNPJ e E-mail).

🛠️ Desafios de Engenharia e Soluções Implementadas
1. Estratégia de Captura de Dados
Para evitar a complexidade e os bloqueios de extrações diretas em larga escala de motores de busca, optei por uma abordagem híbrida:

Ingestão de Dados: Utilização de ferramentas de interface para coleta da massa bruta.

Processamento Python: O núcleo da inteligência foi desenvolvido em Python para permitir total controle sobre a limpeza e o enriquecimento dos dados.

2. Mineração em Profundidade (Deep Scraping)
O maior desafio técnico foi a inconsistência estrutural dos sites industriais. Para resolver isso, o script WebScraper.py foi desenhado com:

Crawling Heurístico: O algoritmo não se limita à página inicial. Ele identifica e navega em sublinks estratégicos (Contato, Institucional, Sobre) para localizar dados muitas vezes ocultos em rodapés.

Mecanismo de Fallback: Implementei uma rotina de busca externa automatizada. Caso o site da empresa esteja inacessível ou incompleto, o sistema consulta fontes secundárias na web para validar o CNPJ e garantir a integridade da base.

3. Normalização e Higienização de Dados
Dados industriais frequentemente apresentam ruídos (notação científica em CNPJs, nomes de empresas com sufixos jurídicos excessivos).

Regex Pattern Matching: Utilização de expressões regulares avançadas para extrair e-mails válidos e formatar CNPJs no padrão brasileiro.

Tratamento de Strings: Desenvolvimento de uma camada de limpeza que remove termos como LTDA, S/A e ME, preparando o dado para uma personalização de e-mail mais assertiva e menos robótica.

4. Automação de Saída e Entregabilidade
A escolha pelo Google Apps Script (scriptmail.js) para o disparo final foi estratégica:

Reputação de IP: Utilizar a infraestrutura nativa do Google Workspace garante taxas de entregabilidade superiores a servidores SMTP convencionais.

Controle de Fluxo: Implementação de delays (Utilities.sleep) e logs de erro em tempo real para monitorar a saúde da operação de outbound.

🏗️ Arquitetura Técnica
Core: Python 3.x (Pandas, BeautifulSoup4, Requests).

Automação: JavaScript (Google Apps Script).

Banco de Dados: Estruturado em Excel/Google Sheets para fácil manipulação pelo time comercial.

📈 Resultados Alcançados
Redução de Tempo: Automação de um processo que levaria dias de pesquisa manual para poucos minutos de execução.

Qualidade do Dado: Filtro rigoroso de "Trigo vs Joio", exportando apenas contatos com e-mails verificados.

Escalabilidade: Estrutura modular que permite a aplicação do mesmo pipeline em diferentes setores econômicos.