# TesteEnjoei

Teste de utilização da Fake Store API (link da documentação para essa API: https://fakestoreapi.com/docs)  para a empresa Enjoei

Realizado com a linguagem Python versão 3.9.19, com execução através do Jupyter Notebook.

O código tem como objetivo:
 - Realizar a conexão ao API da Fake Store, ler seus dados de usuários, carrinho de compras dos usuários e produtos;
 - Através dos processos de transformação e limpeza, adquirir os dados de ID do usuário, data de alteração mais recente do carrinho do usuário e definir qual a categoria de produtos que o usuário mais adiciona em seu carrinho.
 - Armazenar estes dados em um arquivo csv, nomeado de "Result.CSV"

O código retorna os seguintes campos:
 - userId: Id do usuário, adquirido da tabela de cadastros dos usuários. Formato Int.
 - category: Descrição da categoria do produto, adquirido da tabela de cadastros de produtos. Formato string.
 - date: Última data em que o userId realizou uma alteração de seu carrinho, adquirido da tabela de carrinhos dos usuários. Originalmente seu formato era em datetime, porém devido ao horário padronizado de 00:00:00 foi alterado para date.
 - quantity: Quantidade de produtos, da categoria mais comprada pelo cliente, que o cliente adicionou em seu carrinho na sua última atualização do carrinho.

As libs utilizadas para esse projeto foram:

 - requests, versão 2.31.0, com o propósito de realizar as requisições HTTP dos dados disponibilizados pela API.
 - pandas*, versão 2.2.1, sendo responsável pela transformação dos dados brutos no resultado desejado.

*Reconheço que em um ambiente de big data o pandas não é utilizado com frequência, por não ser bem otimizado para um grande volume de dados, porém pareceu ser a ferramenta perfeita para esse teste.

A maior parte das linhas foram comentadas para explicar o meu raciocínio, auxiliando na análise do código, visto que é um teste. Em um ambiente de produção não seria feito deste modo.
