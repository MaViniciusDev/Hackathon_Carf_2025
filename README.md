# Sistema CARF - Previsão de HET, Organização e Monitoramento de Performance

## Descrição

Sistema integrado para otimização de processos do CARF (Conselho Administrativo de Recursos Fiscais) que utiliza Machine Learning para previsão de tempo de julgamento, organização automatizada de lotes e monitoramento de performance analítica.

## Funcionalidades Principais

1. **Previsão de HET (Horas Estimadas de Trabalho)**: Modelo de Machine Learning (Ridge Regression) para estimativa de tempo necessário para análise e julgamento de processos
2. **Organização Automatizada**: Categorização e distribuição inteligente de processos em lotes balanceados entre turmas
3. **Análise de Desempenho**: Sistema profissional de acompanhamento e análise de eficiência de analistas e turmas após conclusão de processos

## Utilização

### Execução Completa do Pipeline

```bash
python executar_pipeline.py
```

### Execução Modular

**Previsão de HET:**
```bash
python src/previsao_het.py
```

**Organização de Lotes:**
```bash
python src/organizar_lotes.py
```

**Análise de Desempenho:**
```bash
python src/analise_desempenho.py
```
*Requer dados de monitoramento (processos concluídos)*

### API de Monitoramento

```python
from src.api_monitoramento import APIMonitoramento

api = APIMonitoramento()

# Registrar início de análise
api.iniciar_analise(
    processo_id='PROC_001',
    analista_id='ANALISTA_007',
    turma=3,
    het_previsto=12.5
)

# Registrar conclusão
api.concluir_analise('PROC_001')
```

## Estrutura do Projeto

```
carf/
│
├── src/                          # Código fonte
│   ├── previsao_het.py          # Modelo preditivo (Ridge Regression)
│   ├── organizar_lotes.py       # Organização e distribuição de lotes
│   ├── analise_desempenho.py    # Sistema de análise de desempenho
│   └── api_monitoramento.py     # API para registro de eventos
│
├── data/                         # Dados de entrada
│   ├── Horas_parametros.xlsx    # Dataset principal (20,742 processos)
│   └── Descrição dos parâmetros.xlsx  # Dicionário de parâmetros
│
├── models/                       # Modelos treinados
│   └── ridge_model.pkl          # Modelo Ridge Regression serializado
│
├── output/                       # Resultados e relatórios
│   ├── Processos_com_HET.xlsx   # Processos com HET previsto
│   ├── Processos_Categorizados.xlsx  # Processos categorizados
│   ├── Lotes_para_Turmas.csv    # Distribuição de lotes
│   ├── Mapeamento_Parametros.csv  # Mapeamento de códigos
│   ├── Monitoramento_Processos.xlsx  # Registro de análises
│   ├── Ranking_Analistas.xlsx   # Performance individual
│   ├── Ranking_Turmas.xlsx      # Performance por turma
│   └── dashboard_*.json         # Dashboards em formato JSON
│
├── docs/                         # Documentação técnica
│   ├── README_SIMPLIFICADO.md   # Guia de referência rápida
│   ├── SISTEMA_MONITORAMENTO.md # Documentação do sistema de monitoramento
│   └── requirements.txt         # Dependências Python
│
└── executar_pipeline.py         # Script de execução completa
```

## Arquivos de Saída

### Módulo de Previsão

**Processos_com_HET.xlsx**
- Base completa com 20,742 processos
- HET_FINAL: horas estimadas de trabalho previstas
- Todos os parâmetros de entrada preservados

### Módulo de Organização

**Processos_Categorizados.xlsx**
- Processos classificados por tipo de documento (AIOA, AIOP, DCOMP, PER, NEOP, NEOA, OUTROS)
- Categorização de complexidade: Simples (≤5h), Médio (≤20h), Complexo (>20h)
- Dados completos para análise e distribuição

**Lotes_para_Turmas.csv**
- Lotes organizados e distribuídos entre 8 turmas
- Informações: lote_id, tipo_documento, complexidade, quantidade, HET médio/total
- Turma atribuída (1-8)
- IDs dos processos componentes

**Mapeamento_Parametros.csv**
- Dicionário de códigos de parâmetros
- Formato: código → descrição legível

### Módulo de Monitoramento

**Monitoramento_Processos.xlsx**
- Registro histórico completo de análises
- Timestamps de início e conclusão
- Comparação HET previsto vs tempo real
- Cálculo de eficiência

**Ranking_Analistas.xlsx**
- Performance individual quantificada
- Classificação S/A/B/C/D por eficiência
- Análise de especialização por tipo de processo
- Pontuação e posicionamento

**Ranking_Turmas.xlsx**
- Performance agregada por turma
- Métricas consolidadas
- Análise de especialização coletiva
- Comparativo inter-turmas

**dashboard_[tipo]_[id].json**
- Painéis individuais e gerenciais em formato JSON
- Preparados para integração com interfaces web
- Estrutura padronizada para consumo via API
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
**Categorização de Complexidade** (baseado em HET):
- Simples: ≤ 5 horas
- Médio: 5 < HET ≤ 20 horas
- Complexo: > 20 horas

**Formação de Lotes**:
- Agrupamento por (tipo_documento, complexidade)
- Tamanho padrão: 50 processos por lote

**Distribuição entre Turmas**:
- Algoritmo de balanceamento greedy
- 8 turmas operacionais
- Critério: equalização de carga por tempo total (HET agregado)

### 3. Sistema de Análise de Desempenho

**Processamento Após Entrega**:
- Análise executada apenas após conclusão de processos reais
- Baseado em dados de monitoramento (não simulação)
- Comparação tempo real vs HET previsto
- Cálculo de eficiência: Eficiência = Tempo Real / HET Previsto

**Sistema de Classificação (S/A/B/C/D)**:

| Classificação | Eficiência | Interpretação |
|---------------|------------|---------------|
| S | < 0.70 | Excelente - 30%+ mais rápido que previsto |
| A | 0.70-0.85 | Ótimo - 15-30% mais rápido |
| B | 0.85-1.00 | Bom - Dentro do prazo previsto |
| C | 1.00-1.20 | Regular - Até 20% acima do previsto |
| D | > 1.20 | Requer atenção - Significativamente acima |

**Análise de Especialização**:
- Identificação de competências por tipo de processo (AIOP, DCOMP, PER, NEOP, NEOA, etc.)
- Classificação granular S/A/B/C/D para cada categoria
- Suporte à alocação estratégica baseada em demonstração de competência

**Métricas e Rankings**:
- Ranking individual quantitativo de analistas
- Ranking agregado de turmas
- Análise de distribuição de especialização
- Métricas de volume e eficiência temporal

**Para documentação completa**: Consultar [docs/SISTEMA_MONITORAMENTO.md](docs/SISTEMA_MONITORAMENTO.md)

## Requisitos do Sistema

```bash
pip install -r docs/requirements.txt
```

**Dependências principais:**
- pandas - Manipulação de dados
- numpy - Operações numéricas
- scikit-learn - Machine Learning
- openpyxl - Leitura/escrita de arquivos Excel

## Performance do Modelo Preditivo

**Ridge Regression - Previsão de HET**

Métricas de avaliação:
- MAE (Mean Absolute Error): 5.268 horas
- RMSE (Root Mean Squared Error): 7.981 horas
- R² (Coefficient of Determination): 0.740

**Interpretação:** O modelo demonstra capacidade preditiva de 74%, com erro médio de aproximadamente 5 horas na estimativa de tempo de julgamento. Considerando a amplitude de duração dos processos (1-100+ horas), o desempenho é considerado satisfatório para aplicação operacional.

## Para o Front-End

**Arquivos para consumo:**

1. `output/Lotes_para_Turmas.csv` - Lotes com turmas atribuídas
2. `output/Mapeamento_Parametros.csv` - Dicionário para exibição de nomes
3. `output/Processos_Categorizados.xlsx` - Base completa de processos
4. `output/Ranking_Analistas.xlsx` - Métricas individuais
5. `output/Ranking_Turmas.xlsx` - Métricas agregadas
6. `output/dashboard_*.json` - Painéis estruturados em JSON

**Formato JSON:** Todos os dashboards são exportados em JSON estruturado, prontos para integração com APIs REST ou interfaces web modernas.

## Fluxo de Dados

```
Horas_parametros.xlsx (entrada)
         ↓
  [Ridge Regression] ← Modelo pré-treinado
         ↓
  Processos_com_HET.xlsx
         ↓
  [Identificação de Tipo] ← Mapeamento de parâmetros
         ↓
  [Categorização de Complexidade]
         ↓
  [Formação de Lotes]
         ↓
  [Distribuição entre Turmas]
         ↓
  Lotes_para_Turmas.csv (saída)
         ↓
  [Monitoramento em Execução]
         ↓
  Rankings e Dashboards (análise)
```

## Notas Técnicas

- **Modelo de Previsão**: Ridge Regression validado e em produção (R²=0.74)
- **Sistema de Organização**: Lógica determinística sem complexidade de ML desnecessária
- **Tipos de Documento**: Identificados diretamente dos parâmetros existentes (colunas 01.XX)
- **Distribuição**: Balanceada por tempo total, não por quantidade de processos
- **Monitoramento**: Sistema profissional focado em métricas objetivas e especialização

---

**Sistema:** CARF - Gestão Integrada de Processos  
**Versão:** 2.0  
**Última Atualização:** Outubro 2025
