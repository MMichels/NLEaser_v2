# NLEaser API

Aplicação web para analise de texto utilizando tecnicas de NLP, com foco em resultado e praticidade.

## Instalação

1 - Instale o Python versão 3.6 ou mais recente \
2 - Instale o [MongoDB](https://www.mongodb.com/try/download/community) versão 4.4.X \
3 - Instale o [RabbitMQ](https://www.rabbitmq.com/download.html) versão 3.8.x \
4 - Clone o repositório para um diretorio local \
5 - Instale as dependencias com 'pip install -r requirements.txt' \
6 - Verifique as configurações no arquivo setup.py \
7 - Configure o acesso ao RabbitMQ no arquivo nleaser/models/config/__init__.py \ 
  7.1 - Na função 'config_rabbit_access' altere o atributo "value" dos objetos user e pwd \
  7.2 - Execute o arquivo com o comando: 'python nleaser/models/config/__init__.py' \
8 - Execute a aplicação com o comando: 'python main.py'

### Desenvolvedores

Lucas Domiciano Barbosa - lucas2809@live.com \
Mateus Michels de Oliveira - michels09@hotmail.com
