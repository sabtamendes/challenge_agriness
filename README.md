### Documentação de Instalação e Execução com Docker

- Conteinerização da aplicação
```bash
docker compose up -d --build
```

- Visualização dos logs

 - app:
```bash
docker ps -a

docker logs <id_container> --follow
```
 - celery:
```bash
docker ps -a

docker logs <id_container> --follow
```

- Executar os testes automatizados
```bash
docker exec -it app /bin/sh

pytest -v
```



### Documentação de Instalação e Execução

1. Configuração do Ambiente

1.1. Variáveis de Ambiente

***Instale as dependências***:

```bash
Copiar código

pip install -r requirements.txt
```

- Certifique-se de configurar as seguintes variáveis de ambiente:
```bash
Copiar código

export FLASK_APP=src.server
export FLASK_ENV=development
export DATABASE_URL=postgresql://postgres:password@localhost:5432/challenge_agriness_db
 ```
 
 1.2. Configuração do Flask

 - Para iniciar o servidor Flask:

```bash
Copiar código

flask run --host=127.0.0.1 --port=5000
ou
flask run
```

1.3. Configuração do Banco de Dados

- Para iniciar o banco de dados e aplicar as migrações:


***Inicialize o banco de dados***:
```bash
Copiar código

flask db init
```

***Crie uma nova migração***:
```bash
Copiar código

flask db migrate -m "Initial migration."
```

**Aplique as migrações***:

```bash

Copiar código

flask db upgrade
```
1.4 Gerenciamento de Migrações

 - Se precisar remover as migrações e reiniciar:
 - Remova a pasta de migrações existente:

```bash
Copiar código

rm -rf migrations
```


2. Configuração do Celery

2.1. Inicialização do RabbitMQ

***Inicie o servidor RabbitMQ***:

  
```bash
Copiar código

rabbitmq-server
```
2.2. Inicialização do Redis

***Inicie o servidor Redis***:

```bash
Copiar código

redis-server
```

2.3. Monitoramento de Tarefas

- Habilite o monitoramento de tarefas do Celery:
```bash
Copiar código

celery -A src.celery_app.celery worker --loglevel=info -E
```

2.4. Visualização de Mensagens na Fila

- Para visualizar mensagens na fila do Redis:

```bash
Copiar código

redis-cli LRANGE celery 0 -1
```

4. Execução de Testes

 ***Para executar os testes***:

```bash
Copiar código

pytest -v
```

5. Testes Manuais dos Endpoints
- Há um arquivo JSON na *raiz* do projeto
- Importar no Insomnia, Postman ou Thunderclient para o testes manuais

***TesteManualRotas.json***

- - GET rota que lista todos os lotes cadastrados, podendo filtrar pelo status created
```json
localhost:5000/batches/
```

- - POST rota que cadastra novos lotes
```json
localhost:5000/batches/

body = 
            {
                "batch_id": 1,
                "status": "created",
                "piglet_count": 25
            }
```

- - PATCH rota que atualiza principalmente a quantidade de leitões nascidos

```json
localhost:5000/batches/1

body = 
        {
            "piglet_count":1333
        }
```

- - DELETE  rota que deleta um lote existente
```json
localhost:5000/batches/1
```