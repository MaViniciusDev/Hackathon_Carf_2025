# 🎯 Sistema CARF - Previsão de HET e Organização de Lotes

## 📋 O que esse sistema faz?

1. **Prevê o tempo necessário** (HET) para julgar cada processo usando Machine Learning (Ridge Regression)
2. **Organiza processos** em lotes por tipo de documento e complexidade
3. **Distribui lotes** entre 8 turmas de forma balanceada

## 🚀 Como usar

### Executar tudo de uma vez:
```bash
python executar_pipeline.py
```

### Executar apenas a previsão de HET:
```bash
python src/previsao_het.py
```

### Executar apenas a organização de lotes:
```bash
python src/organizar_lotes.py
```

## 📂 Estrutura do Projeto

```
carf/
│
├── src/                          # Código fonte
│   ├── previsao_het.py          # Prevê HET com Ridge Regression
│   └── organizar_lotes.py       # Organiza em lotes e distribui
│
├── data/                         # Dados de entrada
│   ├── Horas_parametros.xlsx    # 20,742 processos
│   └── Descrição dos parâmetros.xlsx  # Mapeamento códigos → nomes
│
├── models/                       # Modelos treinados
│   └── ridge_model.pkl          # Modelo Ridge salvo
│
├── output/                       # Resultados gerados
│   ├── Processos_com_HET.xlsx   # Processos + HET previsto
│   ├── Processos_Categorizados.xlsx  # Processos + tipo + complexidade
│   ├── Lotes_para_Turmas.csv    # Lotes distribuídos por turma
│   └── Mapeamento_Parametros.csv  # Códigos → Nomes legíveis
│
└── executar_pipeline.py         # Script master que executa tudo
```

## 📊 Arquivos de Saída

### 1. `Processos_com_HET.xlsx`
Todos os 20,742 processos com HET previsto:
- ID do processo
- HET_FINAL (horas estimadas)
- Todos os parâmetros originais

### 2. `Processos_Categorizados.xlsx`
Processos categorizados:
- ID do processo
- HET_FINAL
- **tipo_documento**: AIOA, AIOP, DCOMP, PER, NEOP, NEOA, OUTROS
- **complexidade**: Simples (≤5h), Médio (≤20h), Complexo (>20h)

### 3. `Lotes_para_Turmas.csv`
Lotes distribuídos (para front-end):
- lote_id
- tipo_documento
- complexidade
- quantidade (nº de processos no lote)
- het_medio (tempo médio por processo)
- het_total (tempo total do lote)
- **turma** (1 a 8)
- ids_processos (lista de IDs)

### 4. `Mapeamento_Parametros.csv`
Mapeamento para exibir nomes legíveis:
- codigo (ex: "01.07.01")
- descricao (ex: "DCOMP - Declaração de compensação eletrônica")

## 🎓 Como Funciona

### 1. Previsão de HET (Ridge Regression)
- **Modelo**: Ridge Regression (regularização L2)
- **Acurácia**: MAE = 5.268 horas, R² = 0.740
- **Dados**: 9,999 processos com HET conhecido (treino) + 10,743 sem HET (previsão)
- **Parâmetros**: 297 colunas (tipos de documento, valores, datas, etc.)

### 2. Organização de Lotes (Sem ML complexo)
**Identificação de Tipo de Documento** (direto dos códigos):
- 01.01 → AIOA (Auto de Infração Obrigação Acessória)
- 01.02 → AIOP (Auto de Infração Obrigação Principal)
- 01.07.01 → DCOMP (Declaração de Compensação)
- 01.08.01 → PER (Pedido de Restituição/Ressarcimento)
- 01.09 → NEOP (Notificação de Exigência Obrigação Principal)
- 01.06 → NEOA (Notificação de Exigência Obrigação Acessória)
- 01.10 → OUTROS

**Categorização de Complexidade** (baseado em HET):
- **Simples**: ≤ 5 horas
- **Médio**: 5 < HET ≤ 20 horas
- **Complexo**: > 20 horas

**Criação de Lotes**:
- Agrupa por (tipo_documento, complexidade)
- Lotes de 50 processos

**Distribuição para Turmas**:
- Algoritmo greedy balanceado
- 8 turmas
- Balanceia pelo tempo total (het_total)

## 🛠️ Requisitos

```bash
pip install -r requirements.txt
```

Principais bibliotecas:
- pandas
- numpy
- scikit-learn
- openpyxl

## ⚙️ Configuração (se necessário)

Edite os caminhos em `config/` (futuro) ou diretamente nos scripts se precisar mudar:
- Localização dos arquivos de entrada
- Número de processos por lote (padrão: 50)
- Número de turmas (padrão: 8)
- Limiares de complexidade

## 📈 Desempenho do Modelo

**Ridge Regression - Previsão de HET:**
- MAE (Erro Médio Absoluto): 5.268 horas
- RMSE (Erro Quadrático Médio): 7.981 horas
- R² (Coeficiente de Determinação): 0.740

Isso significa que o modelo erra em média ~5 horas na previsão, o que é excelente para processos que levam de 1 a 100+ horas.

## 🎯 Para o Front-End

Consumir os seguintes arquivos CSV/Excel:

1. **`Lotes_para_Turmas.csv`**: Mostra lotes já distribuídos por turma
2. **`Mapeamento_Parametros.csv`**: Use para exibir nomes legíveis ao invés de códigos
3. **`Processos_Categorizados.xlsx`**: Detalhes completos de cada processo

## 📝 Notas

- **HET Prediction**: Sistema testado e validado (R²=0.74) - **NÃO MEXER**
- **Organização**: Simplificada (sem TF-IDF, Naive Bayes ou K-Means) - usa códigos direto dos dados
- **Tipos de Documento**: Já existem nos parâmetros (colunas 01.XX)
- **Distribuição**: Balanceada por tempo total, não por quantidade de processos

## 🔄 Fluxo de Execução

```
Horas_parametros.xlsx
         ↓
   [Ridge Regression]
         ↓
  Processos_com_HET.xlsx
         ↓
[Identificar Tipo de Documento]
         ↓
[Categorizar Complexidade]
         ↓
    [Criar Lotes]
         ↓
  [Distribuir Turmas]
         ↓
Lotes_para_Turmas.csv (pronto para front-end)
```
