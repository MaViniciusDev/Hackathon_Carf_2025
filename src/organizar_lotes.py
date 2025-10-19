import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class OrganizadorLotes:
    """Sistema simplificado de organização de lotes"""
    
    def __init__(self):
        self.df = None
        self.mapeamento = {}
        
    def carregar_mapeamento(self):
        """Carrega mapeamento código → nome legível dos parâmetros"""
        try:
            df_desc = pd.read_excel('data/Descrição dos parâmetros.xlsx')
            mapa = dict(zip(
                df_desc['código quesito e parâmetro'].astype(str).str.strip(),
                df_desc['Parâmetro - Descrição'].astype(str).str.strip()
            ))
            self.mapeamento = mapa
            print(f"   ✅ {len(mapa)} mapeamentos carregados")
        except Exception as e:
            print(f"   ⚠️ Erro ao carregar mapeamento: {e}")
            self.mapeamento = {}
    
    def identificar_tipo_documento(self, row):
        """Identifica tipo de documento baseado nos parâmetros preenchidos"""
        # Códigos conhecidos de tipos de documento (coluna 01.XX)
        tipos_documento = {
            '01.01': 'AIOA',
            '01.02': 'AIOP', 
            '01.03': 'AIEOA',
            '01.04': 'AIEOP',
            '01.05': 'NEOP',
            '01.06': 'NEOA',
            '01.07.01': 'DCOMP',
            '01.07.02': 'DCOMP',
            '01.08.01': 'PER',
            '01.08.02': 'PER',
            '01.09': 'Benefícios Fiscais',
            '01.10': 'OUTROS'
        }
        
        # Verifica qual parâmetro 01.XX está preenchido
        for codigo, tipo in tipos_documento.items():
            col_nome = codigo.ljust(12)  # Padronizar nome da coluna
            # Tentar variações do nome da coluna
            for col in self.df.columns:
                if codigo in str(col).strip():
                    if pd.notna(row.get(col)) and row.get(col) != 0:
                        return tipo
        
        return 'OUTROS'
    
    def categorizar_complexidade(self, het):
        """Categoriza processo por complexidade (baseado em HET)"""
        if pd.isna(het):
            return 'Indefinido'
        elif het <= 5:
            return 'Simples'
        elif het <= 20:
            return 'Médio'
        else:
            return 'Complexo'
    
    def criar_lotes(self, tamanho_lote=50):
        """Cria lotes de processos similares"""
        print(f"\n📦 Criando lotes de {tamanho_lote} processos...")
        
        lotes = []
        
        # Agrupar por tipo de documento e complexidade
        grupos = self.df.groupby(['tipo_documento', 'complexidade'])
        
        for (tipo_doc, complexidade), grupo in grupos:
            # Ordenar por HET dentro do grupo
            grupo_ordenado = grupo.sort_values('HET_FINAL')
            
            # Dividir em lotes
            n_lotes = len(grupo_ordenado) // tamanho_lote + (1 if len(grupo_ordenado) % tamanho_lote > 0 else 0)
            
            for i in range(n_lotes):
                inicio = i * tamanho_lote
                fim = min((i + 1) * tamanho_lote, len(grupo_ordenado))
                lote_processos = grupo_ordenado.iloc[inicio:fim]
                
                lotes.append({
                    'lote_id': len(lotes) + 1,
                    'tipo_documento': tipo_doc,
                    'complexidade': complexidade,
                    'quantidade': len(lote_processos),
                    'het_medio': lote_processos['HET_FINAL'].mean(),
                    'het_total': lote_processos['HET_FINAL'].sum(),
                    'ids_processos': lote_processos['ID'].tolist()
                })
        
        df_lotes = pd.DataFrame(lotes)
        print(f"   ✅ {len(df_lotes)} lotes criados")
        
        return df_lotes
    
    def distribuir_turmas(self, df_lotes, n_turmas=8):
        """Distribui lotes para turmas de forma balanceada por tempo"""
        print(f"\n🎯 Distribuindo lotes para {n_turmas} turmas...")
        
        # Inicializar turmas com carga zero
        turmas = {i: {'lotes': [], 'tempo_total': 0} for i in range(1, n_turmas + 1)}
        
        # Ordenar lotes por tempo (maior primeiro) para melhor balanceamento
        lotes_ordenados = df_lotes.sort_values('het_total', ascending=False)
        
        # Distribuir lotes pela turma com menor carga
        for _, lote in lotes_ordenados.iterrows():
            # Encontrar turma com menor tempo acumulado
            turma_menor_carga = min(turmas.items(), key=lambda x: x[1]['tempo_total'])[0]
            
            # Adicionar lote à turma
            turmas[turma_menor_carga]['lotes'].append(lote['lote_id'])
            turmas[turma_menor_carga]['tempo_total'] += lote['het_total']
        
        # Adicionar coluna de turma aos lotes
        lote_para_turma = {}
        for turma_id, info in turmas.items():
            for lote_id in info['lotes']:
                lote_para_turma[lote_id] = turma_id
        
        df_lotes['turma'] = df_lotes['lote_id'].map(lote_para_turma)
        
        # Mostrar distribuição
        print(f"\n   📊 Distribuição por turma:")
        for turma_id, info in sorted(turmas.items()):
            n_lotes = len(info['lotes'])
            tempo = info['tempo_total']
            print(f"      Turma {turma_id}: {n_lotes:3d} lotes | {tempo:8.1f}h total")
        
        return df_lotes
    
    def executar(self):
        """Executa pipeline completo de organização"""
        print("=" * 80)
        print("📦 SISTEMA DE ORGANIZAÇÃO DE LOTES - CARF")
        print("=" * 80)
        
        # 1. Carregar dados com HET previsto
        print("\n📊 Etapa 1: Carregando dados...")
        self.df = pd.read_excel('output/Processos_com_HET.xlsx')
        print(f"   ✅ {len(self.df):,} processos carregados")
        
        # 2. Carregar mapeamento de parâmetros
        print("\n📖 Etapa 2: Carregando mapeamento de parâmetros...")
        self.carregar_mapeamento()
        
        # 3. Identificar tipo de documento
        print("\n🏷️ Etapa 3: Identificando tipos de documento...")
        self.df['tipo_documento'] = self.df.apply(self.identificar_tipo_documento, axis=1)
        
        distribuicao = self.df['tipo_documento'].value_counts()
        print(f"   📊 Tipos encontrados:")
        for tipo, count in distribuicao.items():
            pct = (count / len(self.df)) * 100
            print(f"      • {tipo:<20} {count:>6,} ({pct:>5.1f}%)")
        
        # 4. Categorizar por complexidade
        print("\n⚡ Etapa 4: Categorizando por complexidade...")
        self.df['complexidade'] = self.df['HET_FINAL'].apply(self.categorizar_complexidade)
        
        distribuicao_comp = self.df['complexidade'].value_counts()
        print(f"   📊 Complexidades:")
        for comp, count in distribuicao_comp.items():
            pct = (count / len(self.df)) * 100
            print(f"      • {comp:<20} {count:>6,} ({pct:>5.1f}%)")
        
        # 5. Criar lotes
        df_lotes = self.criar_lotes(tamanho_lote=50)
        
        # 6. Distribuir para turmas
        df_lotes = self.distribuir_turmas(df_lotes, n_turmas=8)
        
        # 7. Salvar resultados
        print("\n💾 Etapa 5: Salvando resultados...")
        
        # Salvar processos categorizados
        self.df.to_excel('output/Processos_Categorizados.xlsx', index=False)
        print(f"   ✅ output/Processos_Categorizados.xlsx")
        
        # Salvar lotes
        df_lotes.to_csv('output/Lotes_para_Turmas.csv', index=False)
        print(f"   ✅ output/Lotes_para_Turmas.csv")
        
        # Salvar mapeamento para front-end
        df_mapeamento = pd.DataFrame([
            {'codigo': k, 'descricao': v} 
            for k, v in self.mapeamento.items()
        ])
        df_mapeamento.to_csv('output/Mapeamento_Parametros.csv', index=False)
        print(f"   ✅ output/Mapeamento_Parametros.csv")
        
        # 8. Estatísticas finais
        print(f"\n📊 Resumo Final:")
        print(f"   • Total de processos: {len(self.df):,}")
        print(f"   • Total de lotes: {len(df_lotes)}")
        print(f"   • Processos por lote (média): {df_lotes['quantidade'].mean():.1f}")
        print(f"   • Tempo por lote (média): {df_lotes['het_total'].mean():.1f}h")
        print(f"   • Turmas: 8")
        
        print(f"\n✅ ORGANIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 80)
        
        return self.df, df_lotes


if __name__ == "__main__":
    organizador = OrganizadorLotes()
    organizador.executar()
