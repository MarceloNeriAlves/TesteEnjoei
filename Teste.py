#!/usr/bin/env python
# coding: utf-8

# link da documentação: https://fakestoreapi.com/docs
# 
# o resultado final deverá ser um arquivo em um dos seguintes formatos: Parquet, CSV, AVRO ou JSON. Este arquivo deve conter as seguintes informações:
# 
# - identificador de usuário
#  - data mais recente em que o usuário adicionou produtos ao carrinho
# - categoria em que o usuário tem mais produtos adicionados ao carrinho
# 
# considerações:
# 
# - você pode utilizar a linguagem de programação que quiser
# - a solução deve ser disponibilizada através de repositório público no GitHub.
# 
# critérios avaliados:
# 
# - lógica de programação
# - documentação
#  - qualidade do código 
# 
# a entrega do teste deverá ser realizada até 23/05/2024 (quinta feira) ao 12:00.

# In[16]:


import requests
import pandas as pd
from io import StringIO

#Lendo todos os dados necessários da API

url = 'https://fakestoreapi.com'
products = requests.get(f"{url}/products")
carts = requests.get(f"{url}/carts")
users = requests.get(f"{url}/users")
dfProduct = pd.read_json(StringIO(products.text))
dfCart = pd.read_json(StringIO(carts.text))
dfUser = pd.read_json(StringIO(users.text))


# In[17]:


#Realizando transformações necessárias na tabela de carrinhos dos usuários

dfCart= dfCart.explode('products') #Separando linhas de produtos agrupados
dfCart['products'] = dfCart['products'].astype('str') 
dfCart[['productId','quantity']] = dfCart['products'].str.split(',',expand=True) #Separando a coluna produtos para adquirir a coluna de id do produto e sua quantidade em carrinho
dfCart['productId'] = dfCart['productId'].str.extract('(\d+)') #Extraindo somente o número da chave.
dfCart['quantity'] = dfCart['quantity'].str.extract('(\d+)').astype(int) #Extraindo somente o número de quantidade e transformando-o em int
dfCart['date'] = dfCart['date'].dt.date #Transformando em formato date, já que o timestamp deste exemplo não apresentava dados úteis.


# In[18]:


#Realizando transformações necessárias na tabela produtos

dfProduct.rename(columns={'id':'productId'}, inplace= True) #Padronizando nome da coluna que utilizarei no join
dfProduct = dfProduct.filter(['productId', 'category']) #Filtrando apenas colunas que vou utilizar
dfProduct['productId'] = dfProduct['productId'].astype('str')


# In[19]:


#Apesar da tabela carrinho já conter id do usuário, acho mais prudente realizar o join considerando que normalmente algum dado do usuário seria interessante

dfEnd = dfUser.filter(['id'], axis=1)


# In[20]:


#Realizando as etapas de join e group by necessárias para chegar no resultado desejado

dfEnd.rename(columns={'id':'userId'}, inplace=True) #Padronizando id de usuário que usarei para o join
dfEnd = dfEnd.merge(dfCart, on='userId', how='left') #Left join para adquirir os dados dos carrinhos de todos os usuários com a possibilidade de adquirir dados de usuários caso necessário
dfEnd = dfEnd.filter(['userId', 'date', 'productId', 'quantity'], axis=1) #Filtrando apenas as colunas relevantes para a informação desejada
dfEnd = dfEnd.merge(dfProduct, on='productId', how='left') #Left join para adquirir a categoria de todos os produtos presentes no carrinho
dfEnd = dfEnd.drop(['productId'], axis=1) #Removendo o id do produto, que não tem relevância pós join para os dados desejados
idx = dfEnd.groupby(['userId'], sort=False)['date'].transform('max') == dfEnd.date #Retorna true para as linhas que contém a data máxima de um userid
dfEnd = dfEnd[idx] #filtra somente os indíces verdadeiros
dfEnd = dfEnd.groupby(['userId','category','date']).sum().reset_index() #Soma as quantidades de cada categoria
dfEnd = dfEnd.groupby(['userId']).max().reset_index() #Retorna somente a categoria com a maior quantidade e a sua quantidade
dfEnd['quantity'] = dfEnd['quantity'].astype(int) #Alterando a quantidade para int, já que não apresenta valores decimais


# In[21]:


dfEnd.to_csv('result.csv')

