# Sistema de Monitoramento e Análise de Performance - CARF

## Visão Geral

Sistema profissional de monitoramento e análise de performance para acompanhamento de analistas e gestores, utilizando comparação entre tempo real de análise e HET (Horas Estimadas de Trabalho) previsto pelo modelo de Machine Learning.

## Objetivos Estratégicos

### Perspectiva do Analista
- Monitoramento de tempo de análise em tempo real
- Comparação de performance individual com estimativas do modelo preditivo
- Acompanhamento longitudinal de produtividade
- Identificação de competências por tipo de processo
- Visualização de métricas de performance categorizadas

### Perspectiva do Gestor
- Monitoramento de performance agregada da turma
- Identificação de especialização por tipo de processo
- Alocação estratégica de processos baseada em competências demonstradas
- Análise de tendências e evolução da equipe
- Benchmarking entre turmas

## Metodologia de Classificação

### Sistema de Avaliação por Eficiência

A classificação é determinada pela relação entre tempo real de execução e HET previsto:

**Fórmula:** Eficiência = Tempo Real de Análise / HET Previsto

| Classificação | Faixa de Eficiência | Descrição | Interpretação |
|---------------|---------------------|-----------|---------------|
| **S** | < 0.70 | Excelente | Execução 30%+ mais rápida que o previsto |
| **A** | 0.70 - 0.85 | Ótimo | Execução 15-30% mais rápida que o previsto |
| **B** | 0.85 - 1.00 | Bom | Execução dentro do prazo estimado |
| **C** | 1.00 - 1.20 | Regular | Execução até 20% acima do estimado |
| **D** | > 1.20 | Requer atenção | Execução significativamente acima do estimado |

**Interpretação:**
- Eficiência < 1.0: Execução mais rápida que o previsto
- Eficiência = 1.0: Execução conforme previsto
- Eficiência > 1.0: Execução mais lenta que o previsto

### Análise de Especialização por Tipo de Processo

O sistema realiza análise granular de performance por categoria de processo, identificando áreas de maior competência:

**Exemplo de Análise de Especialização:**

```json
{
  "especialização_por_tipo": {
    "DCOMP": {
      "eficiencia_media": 0.68,
      "classificacao": "S",
      "volume_processado": 45,
      "tempo_medio_real": 8.5,
      "tempo_medio_previsto": 12.5
    },
    "AIOP": {
      "eficiencia_media": 0.82,
      "classificacao": "A",
      "volume_processado": 32,
      "tempo_medio_real": 14.2,
      "tempo_medio_previsto": 17.3
    },
    "PER": {
      "eficiencia_media": 1.15,
      "classificacao": "C",
      "volume_processado": 18,
      "tempo_medio_real": 22.1,
      "tempo_medio_previsto": 19.2
    }
  }
}
```

**Aplicações Estratégicas:**
- Alocação de processos baseada em especialização demonstrada (classificação S ou A)
- Identificação de necessidades de capacitação (classificação C ou D)
- Otimização de distribuição de carga entre turmas
- Planejamento de desenvolvimento profissional individualizado

## Sistema de Pontuação

### Metodologia de Cálculo

A pontuação é atribuída com base na eficiência demonstrada:

| Eficiência | Pontos Atribuídos | Critério |
|------------|-------------------|----------|
| < 0.80 | 150 | Execução significativamente acima da expectativa |
| 0.80 - 1.00 | 100 | Execução conforme ou acima da expectativa |
| 1.00 - 1.20 | 50 | Execução dentro da margem aceitável |
| > 1.20 | 10 | Execução abaixo da expectativa |

**Finalidade:** Quantificação objetiva de performance para fins de ranking e análise comparativa.

## Métricas e Indicadores

### Painel Individual do Analista

```json
{
  "identificacao": {
    "analista_id": "ANALISTA_005",
    "periodo_analise": "2025-Q4"
  },
  "metricas_volume": {
    "total_processos": 45,
    "processos_concluidos": 38,
    "processos_em_andamento": 7,
    "taxa_conclusao": 84.4
  },
  "metricas_eficiencia": {
    "eficiencia_media_geral": 0.82,
    "classificacao_geral": "A",
    "pontuacao_acumulada": 4200
  },
  "analise_especialização": {
    "DCOMP": {
      "eficiencia_media": 0.68,
      "classificacao": "S",
      "volume": 12
    },
    "AIOP": {
      "eficiencia_media": 0.85,
      "classificacao": "A",
      "volume": 18
    },
    "PER": {
      "eficiencia_media": 1.05,
      "classificacao": "C",
      "volume": 8
    }
  },
  "distribuicao_performance": {
    "acima_expectativa": 30,
    "conforme_expectativa": 8
  }
}
```

### Painel Gerencial da Turma

```json
{
  "identificacao": {
    "turma_id": 3,
    "periodo_analise": "2025-Q4"
  },
  "metricas_volume": {
    "total_processos": 234,
    "processos_concluidos": 189,
    "processos_em_andamento": 45,
    "taxa_conclusao": 80.77
  },
  "metricas_eficiencia": {
    "eficiencia_media": 0.88,
    "classificacao_geral": "B",
    "pontuacao_total": 18500
  },
  "composicao": {
    "numero_analistas": 8,
    "analistas_classificacao_a_ou_superior": 3,
    "analistas_requerem_atencao": 1
  },
  "especialização_turma": {
    "AIOP": {
      "eficiencia_media": 0.75,
      "classificacao": "A",
      "volume": 89
    },
    "DCOMP": {
      "eficiencia_media": 0.92,
      "classificacao": "B",
      "volume": 67
    }
  },
  "distribuicao_temporal": {
    "processos_no_prazo": 150,
    "processos_acima_prazo": 39
  }
}
```

## Utilização do Sistema

### Registro de Eventos de Análise

#### Início de Análise

```python
from src.api_monitoramento import APIMonitoramento

api = APIMonitoramento()

# Registrar início de análise
api.iniciar_analise(
    processo_id='PROC_12345',
    analista_id='ANALISTA_007',
    turma=3,
    het_previsto=15.5,
    tipo_documento='AIOP',
    complexidade='Médio'
)
```

#### Conclusão de Análise

```python
# Registrar conclusão
resultado = api.concluir_analise(
    processo_id='PROC_12345',
    observacoes='Processo concluído - sem intercorrências'
)

# Resultado:
# {
#   'het_previsto': 15.50,
#   'tempo_real': 13.20,
#   'eficiencia': 0.85,
#   'classificacao': 'A'
# }
```

### Consulta de Métricas

#### Métricas Individuais

```python
from src.gamificacao import MonitoramentoGamificacao

sistema = MonitoramentoGamificacao()

# Análise individual
metricas = sistema.calcular_metricas_analista('ANALISTA_007')

# Dashboard completo
dashboard = sistema.gerar_dashboard_analista('ANALISTA_007')
```

#### Métricas Gerenciais

```python
# Análise da turma
metricas_turma = sistema.calcular_metricas_gestor(turma_id=3)

# Dashboard gerencial
dashboard = sistema.gerar_dashboard_gestor(turma_id=3)
```

### Execução do Sistema Completo

```bash
# Pipeline completo (inclui módulo de monitoramento)
python executar_pipeline.py

# Módulo de monitoramento isolado
python src/gamificacao.py
```

## Arquivos de Saída

### Formatos de Exportação

**Excel/CSV (Análise e Reporting):**
- `output/Monitoramento_Processos.xlsx` - Registro histórico completo
- `output/Ranking_Analistas.xlsx` - Ranking individual por performance
- `output/Ranking_Turmas.xlsx` - Ranking de turmas

**JSON (Integração com Sistemas):**
- `output/dashboard_analista_[ID].json` - Painel individual
- `output/dashboard_gestor_turma_[ID].json` - Painel gerencial
- `output/monitoramento_api.json` - Dados consolidados para API

## Fluxo Operacional

```
1. Processo Atribuído → Analista
         ↓
2. Registro: Início de Análise
   - Timestamp de início
   - Associação analista + turma
   - Carregamento de HET previsto
         ↓
3. Execução da Análise
         ↓
4. Registro: Conclusão de Análise
   - Timestamp de conclusão
   - Cálculo de tempo real
   - Cálculo de eficiência
   - Atribuição de pontuação
   - Atualização de classificação
         ↓
5. Atualização de Rankings
   - Ranking individual
   - Ranking de turmas
         ↓
6. Disponibilização de Painéis
   - Dashboard do analista
   - Dashboard gerencial
```

## Painéis e Visualizações

### Dashboard Individual

**Componentes:**
- Gráfico de evolução de eficiência temporal
- Classificação atual (S/A/B/C/D)
- Mapa de especialização por tipo de processo
- Comparativo com média da turma
- Comparativo com média geral
- Posicionamento no ranking

### Dashboard Gerencial

**Componentes:**
- Indicadores agregados de performance
- Distribuição de analistas por classificação
- Matriz de especialização da turma
- Tendências temporais de eficiência
- Distribuição de processos por complexidade
- Análise de balanceamento de carga
- Comparativo inter-turmas

## Integração com Sistemas Externos

### Endpoints REST API (Proposta)

```
POST /api/v1/analise/iniciar
  Payload: { processo_id, analista_id, turma, het_previsto }
  
POST /api/v1/analise/concluir
  Payload: { processo_id, observacoes }
  
GET /api/v1/analista/{id}/metricas
  Response: { metricas_completas }
  
GET /api/v1/gestor/turma/{id}/metricas
  Response: { metricas_turma, lista_analistas }
  
GET /api/v1/rankings/analistas
  Response: [ { posicao, analista, classificacao, pontuacao } ]
  
GET /api/v1/rankings/turmas
  Response: [ { posicao, turma, classificacao, pontuacao } ]
```

### WebSocket (Atualização em Tempo Real)

```javascript
// Evento: Atualização de ranking
ws.on('ranking.updated', (data) => {
  atualizarInterfaceRanking(data);
});

// Evento: Mudança de classificação
ws.on('classificacao.alterada', (data) => {
  notificarMudancaClassificacao(data);
});

// Evento: Conclusão de processo
ws.on('processo.concluido', (data) => {
  atualizarMetricas(data);
});
```

## Aplicações Estratégicas

### Gestão de Recursos Humanos

**Alocação Inteligente:**
- Distribuir processos de acordo com especialização demonstrada
- Maximizar eficiência através de matching tipo-analista
- Reduzir tempo médio de processamento

**Desenvolvimento Profissional:**
- Identificar gaps de competência (classificações C/D)
- Planejar treinamentos específicos por tipo de processo
- Estabelecer mentoria entre analistas S/A e C/D

**Reconhecimento e Incentivos:**
- Base objetiva para avaliação de performance
- Critérios transparentes para reconhecimento
- Identificação de talentos de alta performance

### Gestão Operacional

**Otimização de Processos:**
- Análise de gargalos por tipo de processo
- Identificação de práticas bem-sucedidas
- Benchmark interno entre turmas

**Previsibilidade:**
- Estimativas mais precisas de conclusão de lotes
- Identificação antecipada de sobrecarga
- Planejamento de capacidade

**Qualidade:**
- Correlação entre eficiência e qualidade de análise
- Identificação de padrões de excelência
- Estabelecimento de melhores práticas

## Considerações de Privacidade e Conformidade

### Proteção de Dados

- Dados anonimizáveis para análises agregadas
- Controle de acesso baseado em função
- Auditoria completa de acessos
- Conformidade com LGPD

### Transparência

- Critérios de avaliação públicos e objetivos
- Acesso individual aos próprios dados
- Metodologia de cálculo documentada
- Processo de contestação de métricas

## Roadmap de Evolução

### Fase 1 (Atual)
- Sistema de classificação S/A/B/C/D
- Análise de especialização por tipo
- Rankings individuais e de turma
- Dashboards básicos

### Fase 2 (Próxima)
- Integração com banco de dados relacional
- API REST completa
- Dashboard web interativo
- Sistema de notificações

### Fase 3 (Futuro)
- Machine Learning para predição de performance
- Identificação automática de padrões
- Sistema de recomendação de alocação
- Analytics avançado

---

**Sistema:** CARF - Monitoramento e Análise de Performance  
**Versão:** 2.0  
**Data:** Outubro 2025  
**Classificação:** Documento Técnico Interno
