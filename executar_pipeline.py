"""
Script Master: Executa todo o pipeline do CARF
1. Previsão de HET (Ridge Regression)
2. Organização de Lotes (simples, sem ML complexo)
3. Distribuição para Turmas
4. Análise de Desempenho (opcional, apenas se houver dados de monitoramento)
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("\n" + "="*80)
print("PIPELINE COMPLETO - SISTEMA CARF")
print("="*80 + "\n")

# Importar e executar previsão de HET
print("\n" + "-" * 80)
print("FASE 1: PREVISÃO DE HET")
print("-" * 80)

from src.previsao_het import PrevisaoHET
previsao = PrevisaoHET()
previsao.executar()

# Importar e executar organização de lotes
print("\n" + "-" * 80)
print("FASE 2: ORGANIZAÇÃO DE LOTES")
print("-" * 80)

from src.organizar_lotes import OrganizadorLotes
organizador = OrganizadorLotes()
organizador.executar()

# Verificar se existe dados de monitoramento para análise de desempenho
arquivo_monitoramento = Path('output/Monitoramento_Processos.xlsx')
if arquivo_monitoramento.exists():
    print("\n" + "-" * 80)
    print("FASE 3: ANÁLISE DE DESEMPENHO")
    print("-" * 80)
    
    from src.analise_desempenho import AnaliseDesempenho
    analise = AnaliseDesempenho()
    analise.executar()
else:
    print("\n" + "-" * 80)
    print("FASE 3: ANÁLISE DE DESEMPENHO (AGUARDANDO DADOS)")
    print("-" * 80)
    print("⚠️  Nenhum dado de monitoramento encontrado")
    print("   Para gerar análise de desempenho:")
    print("   1. Use a API de monitoramento para registrar processos")
    print("   2. Execute novamente o pipeline após ter processos concluídos")

print("\n" + "="*80)
print("PIPELINE EXECUTADO COM SUCESSO!")
print("="*80)

print("\n📁 Arquivos gerados:")
print("   1. output/Processos_com_HET.xlsx - Processos com HET previsto")
print("   2. output/Processos_Categorizados.xlsx - Processos organizados")
print("   3. output/Lotes_para_Turmas.csv - Lotes distribuídos")
print("   4. output/Mapeamento_Parametros.csv - Códigos → Nomes")
print("   5. models/ridge_model.pkl - Modelo treinado")
if arquivo_monitoramento.exists():
    print("   6. output/Ranking_Analistas.xlsx - Ranking de analistas")
    print("   7. output/Ranking_Turmas.xlsx - Ranking de turmas")
    print("   8. output/dashboard_*.json - Dashboards individuais")
print()
