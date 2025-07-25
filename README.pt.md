# 💼 Scraper de vagas de emprego com filtros personalizados (Remote.com)

Um scraper de vagas de emprego, feito com **BeautifulSoup**, **Pandas** e **Dash**, que extrai dados do site [Remote.com](https://remote.com/jobs/all) baseado em filtros personalizados.

---

## Funcionalidades

- 📄 Extrai dados de Remote.com
- 🔍 Filtros de busca:
  - Tipo de contrato (Full-time, Part-time, Contract)
  - Local de trabalho (Remote, Hybrid, On-site)
  - Senioridade mínima
  - Moeda de pagamento e salario mínimo
  - Palavras-chaves
  - Frequência de viagem
- 💰 Calcula a renda média por hora
- 📥 Exporta em **EXCEL**

---

## Bibliotecas usadas

- [Python 3.10+](https://www.python.org/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Pandas](https://pandas.pydata.org/)
- [Dash](https://dash.plotly.com/)
- [Requests](https://docs.python-requests.org/)

---

## Prints

![Job Scraper Interface](./screenshots/interface.png)
![Scraped data](./screenshots/scraped.png)
![Excel result](./screenshots/workbook.png)