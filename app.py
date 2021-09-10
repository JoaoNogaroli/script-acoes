import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
res = requests.get('https://br.advfn.com/indice/ibovespa')
soup = BeautifulSoup(res.text, 'html.parser')
div= soup.find('div', class_ = 'stock-list block')
tab = div.find('table', class_ = 'table_element_class')
#print(tab)
thead = tab.find('thead').find_all('th')
nome_coluna = []
for t in thead:
    nome_coluna.append(t.text)

td = tab.find_all('tr')

tabela_com_val = td.pop(0)
itens = []
for k in td:
    itens.append(k.text)
nomes_ativos = []
for k in td:
    nomes_ativos.append(k.find('a').text)
valores = []
for k in td:
    valores.append((k.find('td', class_ = 'PriceTextDown Numeric Column3'))or(k.find('td', class_ = 'PriceTextUp Numeric Column3'))or(k.find('td', class_ = 'PriceTextUnchanged Numeric Column3')))
valores_finais = []
for val in valores:
    valores_finais.append(val.text)
siglas = []
for s in td:
    siglas_a_filtrar = (s.find('td', class_ = 'String Column2'))
    siglas.append(siglas_a_filtrar.text)
total = []
total.append(nomes_ativos)
total.append(siglas)
total.append(valores_finais)
#print(len(total))
df = DataFrame(total).transpose()
df.columns = ['Ativo','Sigla','Valor Atual']
print(df)
df.to_excel("bolsa.xlsx")
