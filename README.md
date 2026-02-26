# BaseTeste — Ambiente de Desenvolvimento PostgreSQL

Ambiente Docker local com PostgreSQL que replica automaticamente a estrutura e dados do banco de produção para um banco de testes isolado.

---

## Estrutura do Projeto

```
BaseTeste/
├── .env                                    # Credenciais (não versionar)
├── .env.example                            # Template de credenciais
├── .gitignore
├── tabelas.conf                            # Tabelas a replicar e seus filtros
├── replica.py                              # Orquestrador principal (schema + dados)
├── base_testes_schema.py                   # Extrai e restaura o schema de produção
├── base_testes_replicar_dados_semcopy.py   # Replica dados via INSERT paralelo
├── base_testes_replicar_dados_comcopy.py   # Replica dados via COPY (em lote)
├── gerar_conf.py                           # Gera tabelas.conf ordenado por FK
├── out/                                    # Arquivos .sql gerados (não versionar)
└── postgresql/
    ├── Dockerfile                          # Imagem PostgreSQL 15 + Python + extensões
    ├── docker-compose.yml                  # Configuração do container
    └── init-scripts/
        └── 01_init.sql                     # Script de inicialização do banco
```

---

## Pré-requisitos

- Docker Engine + Docker Compose
- WSL 2 (Windows) ou Linux nativo
- Acesso à rede de produção

---

## Configuração Inicial

### 1. Credenciais

Crie o arquivo `.env` na raiz do projeto a partir do template:

```bash
cp .env.example .env
```

Edite o `.env` com as credenciais reais:

```env
# Produção (origem)
PROD_HOST=10.80.91.30
PROD_PORT=5432
PROD_DB=10.50.13.22_eleva
PROD_USER=seu_usuario
PROD_PASS=sua_senha

# Dev/Local (destino)
DEV_HOST=localhost
DEV_PORT=5432
DEV_DB=10.50.13.22_eleva_teste
DEV_USER=postgres
DEV_PASS=sua_senha_local
```

> ⚠️ **O arquivo `.env` nunca deve ser commitado no Git.**

---

### 2. Subir o Container

**Primeira vez ou após alterar o `Dockerfile`:**
```bash
cd postgresql
docker compose up -d --build
```

**Demais vezes:**
```bash
docker compose up -d
```

**Verificar se está saudável:**
```bash
docker compose ps
```

---

### 3. Gerar o `tabelas.conf` (opcional)

O `tabelas.conf` define quais tabelas serão replicadas e seus filtros. Para gerá-lo automaticamente a partir do banco de produção (ordenado por dependências de FK):

```bash
docker exec -it postgres_dev python3 /scripts/gerar_conf.py
```

Para visualizar sem gravar:
```bash
docker exec -it postgres_dev python3 /scripts/gerar_conf.py --dry-run
```

**Formato do arquivo gerado:**
```
# tabela | coluna_data | dias | limit
cbcliente |  |  | 100
cbbordero | data_dat | 365 | 500
cbfollowup | data_dat | 365 | 500
```

---

## Uso — Comandos Principais

### Setup Completo (Schema + Dados)

```bash
docker exec -it postgres_dev python3 /scripts/replica.py
```

### Apenas Schema (estrutura do banco)

```bash
docker exec -it postgres_dev python3 /scripts/replica.py --apenas-schema
```

### Apenas Dados

```bash
docker exec -it postgres_dev python3 /scripts/replica.py --apenas-dados
```

### Controlar Workers Paralelos

```bash
# Padrão: 5 workers paralelos
docker exec -it postgres_dev python3 /scripts/replica.py --apenas-dados --workers 3
```

### Dry-run (simula sem inserir)

```bash
docker exec -it postgres_dev python3 /scripts/replica.py --dry-run
```

---

## Scripts Individuais

### Schema

Extrai o schema de produção via `pg_dump`, sanitiza configurações incompatíveis e restaura no banco de testes:

```bash
docker exec -it postgres_dev python3 /scripts/base_testes_schema.py
```

### Replicação via INSERT (semcopy) — recomendado

Insere os dados registro a registro com `ON CONFLICT DO NOTHING`, processando até 5 tabelas em paralelo. Resolve dependências de FK automaticamente:

```bash
docker exec -it postgres_dev python3 /scripts/base_testes_replicar_dados_semcopy.py
docker exec -it postgres_dev python3 /scripts/base_testes_replicar_dados_semcopy.py --workers 3
docker exec -it postgres_dev python3 /scripts/base_testes_replicar_dados_semcopy.py --dry-run
```

### Replicação via COPY (comcopy) — mais rápido

Gera um arquivo `.sql` com blocos `COPY` e aplica em uma única transação. Mais rápido, porém substitui os dados existentes:

```bash
# Gera e aplica
docker exec -it postgres_dev python3 /scripts/base_testes_replicar_dados_comcopy.py

# Só gera o .sql sem aplicar
docker exec -it postgres_dev python3 /scripts/base_testes_replicar_dados_comcopy.py --apenas-gerar

# Aplica o último .sql gerado
docker exec -it postgres_dev python3 /scripts/base_testes_replicar_dados_comcopy.py --apenas-aplicar
```

Os arquivos `.sql` gerados ficam disponíveis na pasta `out/` do Windows.

---

## Gerenciamento do Container

### Reiniciar sem perder dados
```bash
docker compose down
docker compose up -d
```

### Apagar tudo e recriar do zero
```bash
cd postgresql
docker compose down -v
docker compose up -d --build
```

### Ver logs
```bash
docker logs postgres_dev
docker logs -f postgres_dev   # acompanhar em tempo real
```

### Acessar o banco via psql
```bash
docker exec -it postgres_dev psql -U postgres -d 10.50.13.22_eleva_teste
```

---

## Comparativo entre Métodos de Replicação

| | `semcopy` (INSERT) | `comcopy` (COPY) |
|---|---|---|
| **Velocidade** | Mais lento | Mais rápido |
| **Duplicatas** | Ignoradas (`ON CONFLICT`) | Substitui os dados |
| **Paralelismo** | Até 5 tabelas simultâneas | Sequencial |
| **Arquivo gerado** | Não | Sim (`.sql` em `out/`) |
| **Recomendado para** | Uso cotidiano | Carga inicial grande |

---

## Solução de Problemas

**Container não sobe após alterar o `Dockerfile`:**
```bash
docker compose down -v
docker compose up -d --build
```

**Erro de SSL ao instalar pacotes Python no build:**
Já tratado com `--trusted-host` no `Dockerfile`.

**Script não encontra o `.env`:**
Confirme que o arquivo `.env` existe na raiz do `BaseTeste/` e que o volume `../.env:/scripts/.env` está no `docker-compose.yml`.

**Tabela com erro de FK na replicação:**
Regenere o `tabelas.conf` com `gerar_conf.py` — ele ordena as tabelas respeitando as dependências de chave estrangeira.
