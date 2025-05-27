# FIAP Tech Challenge - Fase 3

Este projeto realiza a coleta, tratamento e previsão de dados da ANVISA sobre produtos manipulados, com exposição de modelos via API.

Existe a preocupação de que esse projeto fique em concordancia com;
- As Convenções próximas às do FastAPI, MLflow e projetos profissionais: 
- Principios de SOLID 
- Padrões de Projeto 
- Arquitetura limpa


## 🔧 Estrutura Geral

```
v2/
├── .venv/                             # Ambiente virtual gerenciado por Poetry
├── pyproject.toml                     # Configuração das dependências (Poetry)
├── poetry.lock                        # Lockfile (Poetry)
├── .python-version                    # Indica a versão Python usada pelo projeto (pyenv)
├── requirements.txt (opcional)        # Alternativa caso não use Poetry
├── README.md                          # README principal do projeto na raiz
├── docs/                              # Documentação complementar
│   └── *.md, *.pdf
├── artifacts/                         # Modelos treinados e outputs do MLflow
├── certs/                             # Certificados e arquivos de autenticação
├── notebooks/                         # Notebooks Jupyter para testes e exploração
├── src/                               # Código-fonte principal
│   ├── api/                           # Camada de aplicação (FastAPI)
│   │   ├── main.py
│   │   └── routes/
│   ├── ingestion/                     # Aquisição de dados (scraping/API externa)
│   ├── processing/                    # Pré-processamento de dados
│   ├── crud/                          # Operações com banco (CRUD)
│   ├── ml/                            # Código dos modelos de Machine Learning
│   ├── services/                      # Serviços de negócio (orquestram operações)
│   ├── schemas/                       # Validações e Schemas (Pydantic)
│   ├── models/                        # Modelos de domínio (SQLAlchemy)
│   ├── storage/                       # Conexão e persistência (Infraestrutura)
│   ├── dashboard/                     # Código/streamlit/gráficos
│   └── runner/                        # Executores automáticos
│       ├── run_carga_banco.py
│       └── run_modelo_lstm.py
└── tests/                             # Testes unitários e de integração
    ├── api/
    ├── ingestion/
    └── ml/

```

## 🚀 Como executar

### 1. Criar o banco e carregar os dados
```bash
python runner/run_carga_banco.py
```

### 2. Treinar o modelo LSTM
```bash
python runner/run_modelo_lstm.py
```

### 3. Iniciar a API
```bash
uvicorn api.main:app --reload
```

### 4. Acessar endpoints
- `http://localhost:8000/` → Mensagem inicial
- `http://localhost:8000/health/` → Status
- `http://localhost:8000/predict/` → POST com dados para previsão

## 📦 Exemplo de entrada para /predict
```json
[
  {"ANO_VENDA": 2022, "MES_VENDA": 10, "QTD_UNIDADE_FARMACOTECNICA": 1000.0},
  {"ANO_VENDA": 2022, "MES_VENDA": 11, "QTD_UNIDADE_FARMACOTECNICA": 1100.0},
  {"ANO_VENDA": 2022, "MES_VENDA": 12, "QTD_UNIDADE_FARMACOTECNICA": 1200.0},
  {"ANO_VENDA": 2023, "MES_VENDA": 1, "QTD_UNIDADE_FARMACOTECNICA": 1300.0}
]
```

## 📌 Dependências principais
- FastAPI
- SQLAlchemy
- TensorFlow
- Pandas / NumPy / Matplotlib
- Uvicorn (para execução local da API)

---

Desenvolvido por Antonio Juan ⚙️
