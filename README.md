
# Desafio técnico Giro.Tech (backend)
## Ferramentas utilizadas
- Python
- Flask 
- SQLAlchemy (ORM)
- SQLite
- Pydantic (validação de dados)
- Pytest (testes)

## Instalação
**Clone o repositório:**
```bash
git clone https://github.com/ronaldMarquesbr/desafio-tecnico-backend-girotech.git

cd desafio-tecnico-backend-girotech
```

**Instalação das dependências**
```bash
pip install -r requirements.txt
```

## Rodando a aplicação
Para iniciar o servidor Flask, execute:
```bash
python run.py
```

A API estará disponível em http://127.0.0.1:3000.

## Endpoints

### Moedas
**Criação de moedas**
```
  POST /currencies
```

Corpo da requisição
```json
{
    "name": "<string>",
    "type": "<string>"
}
```

Respostas
| Código    |  Descrição                       |
| :-------- |:-------------------------------- |
| 200    | Moeda criada com sucesso |
| 400    | Dados enviados incorretamente|

O campos de *name* e *type* não podem ser repetidos, ou seja, não é permitido o salvamento de mais de uma moeda com mesmo *name* ou *type*.

**Obter moedas**
```
  GET /currencies
```

Exemplo de resposta 
```json
[
  {
    "id": 1,
    "name": "Dólar Americano",
    "type": "USD"
  },
  {
    "id": 2,
    "name": "Euro",
    "type": "EUR"
  }
]
```

### Taxas de câmbio
**Criação de taxa de câmbio**
```
  POST /exchange-rates
```

Corpo da requisição
```json
{
  "date": "2025-02-01",
  "daily_variation": 0.5,
  "daily_rate": 5.25,
  "currency_id": 1
}
```

Exemplo de resposta
```json
{
  "id": 1,
  "date": "2025-02-01",
  "daily_variation": 0.5,
  "daily_rate": 5.25,
  "currency_name": "Dólar Americano",
  "currency_type": "USD"
}
```

**Obter taxas de câmbio recentes**
```
  GET /exchange-rates/recent
```

Exemplo de resposta
```json
[
  {
    "id": 1,
    "date": "2025-02-01",
    "daily_variation": 0.5,
    "daily_rate": 5.25,
    "currency_name": "Dólar Americano",
    "currency_type": "USD"
  },
  {
    "id": 2,
    "date": "2025-02-02",
    "daily_variation": -0.3,
    "daily_rate": 5.22,
    "currency_name": "Euro",
    "currency_type": "EUR"
  }
]
```

**Atualização de taxa de câmbio**
```
  PATCH /exchange-rates/{id}
```

Corpo da requisição
```json
{
  "daily_variation": 0.8,
  "daily_rate": 5.30,
  "currency_id": 1
}
```

Exemplo de resposta
```json
{
  "id": 1,
  "date": "2025-02-01",
  "daily_variation": 0.8,
  "daily_rate": 5.30,
  "currency_name": "Euro",
  "currency_type": "EUR"
}
```

**Remover taxas de câmbio antigas**
```
  DELETE /exchange-rates/old
```

### Investidores
**Criação de investidor**
```
  POST /investors
```

Corpo da requisição
```json
{
  "name": "João Silva",
  "email": "joao@email.com"
}
```

Exemplo de resposta
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@email.com"
}
```

**Remover investidor**
```
  DELETE /investor/{id}
```

### Investimentos
**Criação de investimento**
```
  POST /investments
```

Corpo da requisição
```json
{
  "initial_amount": 10000,
  "months": 12,
  "interest_rate": 5.5,
  "final_amount": 10550,
  "currency_id": 1,
  "investor_id": 1
}
```

Exemplo de resposta
```json
{
  "id": 1,
  "initial_amount": 10000,
  "months": 12,
  "interest_rate": 5.5,
  "final_amount": 10550,
  "currency_id": 1,
  "investor_id": 1
}
```

## Testando a aplicação

Este projeto inclui testes automatizados para garantir o funcionamento correto das rotas e funcionalidades principais.



### Rodar os testes
Para executar todos os testes:
```bash
pytest
```
Para executar um teste específico:
```bash
pytest tests/test_minharota.py
```
Para visualizar os testes com mais detalhes:
```bash
pytest -s -v
```