"""
API de Monitoramento - CARF
Interface para registrar e consultar status de processos em tempo real
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
import json


class APIMonitoramento:
    """API para registrar eventos de análise de processos"""
    
    def __init__(self, arquivo_monitoramento='output/Monitoramento_Processos.xlsx'):
        self.arquivo = arquivo_monitoramento
        self.df = self._carregar_ou_criar()
    
    def _carregar_ou_criar(self):
        """Carrega arquivo existente ou cria novo"""
        if Path(self.arquivo).exists():
            return pd.read_excel(self.arquivo)
        else:
            return pd.DataFrame(columns=[
                'processo_id', 'analista_id', 'turma', 'data_inicio',
                'data_conclusao', 'status', 'het_previsto', 'tempo_real',
                'eficiencia', 'tipo_documento', 'complexidade', 'observacoes'
            ])
    
    def _salvar(self):
        """Salva dataframe no arquivo"""
        Path(self.arquivo).parent.mkdir(exist_ok=True)
        self.df.to_excel(self.arquivo, index=False)
    
    def iniciar_analise(self, processo_id, analista_id, turma, het_previsto, 
                       tipo_documento='OUTROS', complexidade='Médio'):
        """
        Registra início da análise de um processo
        
        Args:
            processo_id: ID do processo
            analista_id: ID do analista
            turma: Número da turma (1-8)
            het_previsto: HET previsto pelo modelo
            tipo_documento: Tipo de documento (AIOA, AIOP, etc.)
            complexidade: Simples, Médio ou Complexo
        
        Returns:
            dict com dados do registro criado
        """
        # Verificar se já existe
        if processo_id in self.df['processo_id'].values:
            print(f"⚠️  Processo {processo_id} já está em monitoramento")
            return None
        
        novo_registro = pd.DataFrame([{
            'processo_id': processo_id,
            'analista_id': analista_id,
            'turma': turma,
            'data_inicio': datetime.now(),
            'data_conclusao': None,
            'status': 'em_analise',
            'het_previsto': het_previsto,
            'tempo_real': None,
            'eficiencia': None,
            'tipo_documento': tipo_documento,
            'complexidade': complexidade,
            'observacoes': ''
        }])
        
        self.df = pd.concat([self.df, novo_registro], ignore_index=True)
        self._salvar()
        
        print(f"✅ Análise iniciada: Processo {processo_id} por {analista_id}")
        return novo_registro.to_dict('records')[0]
    
    def concluir_analise(self, processo_id, observacoes=''):
        """
        Registra conclusão da análise de um processo
        
        Args:
            processo_id: ID do processo
            observacoes: Observações opcionais
        
        Returns:
            dict com métricas calculadas
        """
        idx = self.df[self.df['processo_id'] == processo_id].index
        
        if len(idx) == 0:
            print(f"❌ Processo {processo_id} não encontrado")
            return None
        
        idx = idx[0]
        
        # Calcular tempo real
        data_inicio = pd.to_datetime(self.df.loc[idx, 'data_inicio'])
        data_conclusao = datetime.now()
        tempo_real = (data_conclusao - data_inicio).total_seconds() / 3600  # em horas
        
        het_previsto = self.df.loc[idx, 'het_previsto']
        eficiencia = tempo_real / het_previsto if het_previsto > 0 else None
        
        # Atualizar registro
        self.df.loc[idx, 'data_conclusao'] = data_conclusao
        self.df.loc[idx, 'status'] = 'concluido'
        self.df.loc[idx, 'tempo_real'] = tempo_real
        self.df.loc[idx, 'eficiencia'] = eficiencia
        self.df.loc[idx, 'observacoes'] = observacoes
        
        self._salvar()
        
        # Feedback
        if eficiencia < 0.8:
            feedback = "🌟 Excelente! 20% mais rápido que o previsto!"
        elif eficiencia < 1.0:
            feedback = "✅ Ótimo! Concluído dentro do prazo!"
        elif eficiencia < 1.2:
            feedback = "⚠️  Levemente acima do previsto"
        else:
            feedback = "⏰ Muito acima do tempo previsto"
        
        resultado = {
            'processo_id': processo_id,
            'het_previsto': het_previsto,
            'tempo_real': round(tempo_real, 2),
            'eficiencia': round(eficiencia, 2),
            'feedback': feedback
        }
        
        print(f"\n✅ Análise concluída: Processo {processo_id}")
        print(f"   HET Previsto: {het_previsto:.2f}h")
        print(f"   Tempo Real: {tempo_real:.2f}h")
        print(f"   Eficiência: {eficiencia:.2f}")
        print(f"   {feedback}\n")
        
        return resultado
    
    def pausar_analise(self, processo_id):
        """Marca processo como pausado"""
        idx = self.df[self.df['processo_id'] == processo_id].index
        if len(idx) > 0:
            self.df.loc[idx[0], 'status'] = 'pausado'
            self._salvar()
            print(f"⏸️  Processo {processo_id} pausado")
            return True
        return False
    
    def retomar_analise(self, processo_id):
        """Retoma análise pausada"""
        idx = self.df[self.df['processo_id'] == processo_id].index
        if len(idx) > 0:
            self.df.loc[idx[0], 'status'] = 'em_analise'
            self._salvar()
            print(f"▶️  Processo {processo_id} retomado")
            return True
        return False
    
    def consultar_processo(self, processo_id):
        """Consulta status de um processo"""
        processo = self.df[self.df['processo_id'] == processo_id]
        if processo.empty:
            return None
        return processo.to_dict('records')[0]
    
    def listar_processos_analista(self, analista_id, status=None):
        """Lista processos de um analista"""
        processos = self.df[self.df['analista_id'] == analista_id]
        
        if status:
            processos = processos[processos['status'] == status]
        
        return processos.to_dict('records')
    
    def listar_processos_turma(self, turma, status=None):
        """Lista processos de uma turma"""
        processos = self.df[self.df['turma'] == turma]
        
        if status:
            processos = processos[processos['status'] == status]
        
        return processos.to_dict('records')
    
    def estatisticas_analista(self, analista_id):
        """Retorna estatísticas de um analista"""
        processos = self.df[self.df['analista_id'] == analista_id]
        
        if processos.empty:
            return None
        
        concluidos = processos[processos['status'] == 'concluido']
        
        return {
            'analista_id': analista_id,
            'total_processos': len(processos),
            'concluidos': len(concluidos),
            'em_analise': len(processos[processos['status'] == 'em_analise']),
            'pausados': len(processos[processos['status'] == 'pausado']),
            'eficiencia_media': concluidos['eficiencia'].mean() if len(concluidos) > 0 else None,
            'tempo_medio': concluidos['tempo_real'].mean() if len(concluidos) > 0 else None
        }
    
    def exportar_json(self, output_path='output/monitoramento_api.json'):
        """Exporta dados para JSON"""
        dados = self.df.to_dict('records')
        
        # Converter timestamps para string
        for item in dados:
            if pd.notna(item.get('data_inicio')):
                item['data_inicio'] = str(item['data_inicio'])
            if pd.notna(item.get('data_conclusao')):
                item['data_conclusao'] = str(item['data_conclusao'])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Exportado: {output_path}")
        return dados


# Exemplo de uso
if __name__ == '__main__':
    api = APIMonitoramento()
    
    print("\n" + "="*60)
    print("📡 DEMONSTRAÇÃO - API DE MONITORAMENTO")
    print("="*60)
    
    # Exemplo: Iniciar análise
    print("\n1️⃣ Iniciando análise de processo...")
    api.iniciar_analise(
        processo_id='PROC_001',
        analista_id='ANALISTA_005',
        turma=3,
        het_previsto=12.5,
        tipo_documento='AIOP',
        complexidade='Médio'
    )
    
    # Exemplo: Consultar processo
    print("\n2️⃣ Consultando processo...")
    status = api.consultar_processo('PROC_001')
    print(f"   Status: {status['status']}")
    print(f"   Analista: {status['analista_id']}")
    print(f"   HET Previsto: {status['het_previsto']}h")
    
    # Exemplo: Concluir análise (simulado)
    # api.concluir_analise('PROC_001', observacoes='Processo simples, sem dificuldades')
    
    # Exemplo: Estatísticas
    print("\n3️⃣ Estatísticas do analista...")
    stats = api.estatisticas_analista('ANALISTA_005')
    if stats:
        print(f"   Total: {stats['total_processos']}")
        print(f"   Concluídos: {stats['concluidos']}")
        print(f"   Em análise: {stats['em_analise']}")
    
    print("\n" + "="*60)
