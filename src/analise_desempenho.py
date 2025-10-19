""""""

Sistema de Análise de Desempenho - CARFSistema de Gamificação e Monitoramento - CARF

Analisa performance de analistas e turmas após conclusão de processosMonitora performance de analistas e gestores comparando tempo real vs HET previsto

Compara tempo real de execução vs HET previsto"""

"""

import pandas as pd

import pandas as pdimport numpy as np

import numpy as npfrom datetime import datetime, timedelta

from datetime import datetimefrom pathlib import Path

from pathlib import Pathimport json

import jsonimport warnings

import warningswarnings.filterwarnings('ignore')

warnings.filterwarnings('ignore')



class MonitoramentoGamificacao:

class AnaliseDesempenho:    """

    """    Sistema de gamificação para monitorar performance de analistas e gestores

    Sistema de análise de desempenho    Compara tempo real de análise vs HET previsto

    Analisa performance após conclusão dos processos    """

    """    

        def __init__(self):

    def __init__(self, arquivo_monitoramento='output/Monitoramento_Processos.xlsx'):        self.df_processos = None

        self.arquivo_monitoramento = arquivo_monitoramento        self.df_monitoramento = None

        self.df_monitoramento = None        self.metricas_analistas = {}

                self.metricas_gestores = {}

    def carregar_monitoramento(self):        self.rankings = {}

        """Carrega dados de processos concluídos"""        

        try:    def carregar_dados(self):

            if not Path(self.arquivo_monitoramento).exists():        """Carrega processos categorizados com HET"""

                print(f"⚠️  Arquivo de monitoramento não encontrado: {self.arquivo_monitoramento}")        try:

                print("    Execute primeiro o módulo de monitoramento para gerar dados")            self.df_processos = pd.read_excel('output/Processos_Categorizados.xlsx')

                return False            print(f"✅ {len(self.df_processos)} processos carregados")

                        return True

            self.df_monitoramento = pd.read_excel(self.arquivo_monitoramento)        except Exception as e:

            print(f"✓ {len(self.df_monitoramento)} registros carregados")            print(f"❌ Erro ao carregar dados: {e}")

                        return False

            # Filtrar apenas processos concluídos    

            concluidos = self.df_monitoramento[self.df_monitoramento['status'] == 'concluido']    def registrar_inicio_analise(self, processo_id, analista_id, data_inicio=None):

            print(f"✓ {len(concluidos)} processos concluídos para análise")        """Registra início da análise de um processo"""

                    if data_inicio is None:

            if len(concluidos) == 0:            data_inicio = datetime.now()

                print("⚠️  Nenhum processo concluído encontrado")        

                return False        registro = {

                        'processo_id': processo_id,

            return True            'analista_id': analista_id,

                        'data_inicio': data_inicio,

        except Exception as e:            'status': 'em_analise',

            print(f"❌ Erro ao carregar monitoramento: {e}")            'tempo_real': None,

            return False            'het_previsto': None,

                'eficiencia': None

    def _calcular_classificacao(self, eficiencia_media):        }

        """        

        Calcula classificação baseada na eficiência média        # Buscar HET previsto

        S = Excelente (< 0.70)        if self.df_processos is not None:

        A = Ótimo (0.70-0.85)            processo = self.df_processos[self.df_processos['ID'] == processo_id]

        B = Bom (0.85-1.00)            if not processo.empty:

        C = Regular (1.00-1.20)                registro['het_previsto'] = processo['HET_FINAL'].values[0]

        D = Requer atenção (> 1.20)                registro['tipo_documento'] = processo.get('tipo_documento', ['OUTROS']).values[0]

        """                registro['complexidade'] = processo.get('complexidade', ['Médio']).values[0]

        if eficiencia_media is None or pd.isna(eficiencia_media):        

            return 'N/A'        return registro

            

        if eficiencia_media < 0.70:    def registrar_conclusao_analise(self, processo_id, data_conclusao=None):

            return 'S'        """Registra conclusão da análise e calcula métricas"""

        elif eficiencia_media < 0.85:        if data_conclusao is None:

            return 'A'            data_conclusao = datetime.now()

        elif eficiencia_media <= 1.00:        

            return 'B'        # Aqui você carregaria do banco/arquivo o registro de início

        elif eficiencia_media <= 1.20:        # Por simplicidade, vamos criar um exemplo

            return 'C'        

        else:        return {

            return 'D'            'processo_id': processo_id,

                'data_conclusao': data_conclusao,

    def _calcular_especializacao_tipos(self, df_processos):            'status': 'concluido'

        """        }

        Calcula especialização por tipo de processo    

        Retorna classificação S/A/B/C/D para cada tipo processado    def calcular_metricas_analista(self, analista_id):

        """        """Calcula métricas de performance de um analista"""

        concluidos = df_processos[df_processos['status'] == 'concluido'].copy()        # Filtra processos do analista

                processos_analista = self.df_monitoramento[

        if concluidos.empty:            self.df_monitoramento['analista_id'] == analista_id

            return {}        ]

                

        especializacao = {}        if processos_analista.empty:

                    return None

        for tipo in concluidos['tipo_documento'].unique():        

            processos_tipo = concluidos[concluidos['tipo_documento'] == tipo]        # Calcular métricas

                    total_processos = len(processos_analista)

            if len(processos_tipo) == 0:        processos_concluidos = len(processos_analista[processos_analista['status'] == 'concluido'])

                continue        

                    # Eficiência média (tempo_real / het_previsto)

            eficiencia_tipo = processos_tipo['eficiencia'].mean()        # < 1.0 = mais rápido que previsto (bom)

                    # > 1.0 = mais lento que previsto (precisa melhorar)

            especializacao[tipo] = {        eficiencias = processos_analista['eficiencia'].dropna()

                'eficiencia_media': round(eficiencia_tipo, 3),        eficiencia_media = eficiencias.mean() if len(eficiencias) > 0 else None

                'classificacao': self._calcular_classificacao(eficiencia_tipo),        

                'volume': len(processos_tipo),        # Pontuação (quanto menor a eficiência, maior a pontuação)

                'tempo_medio_real': round(processos_tipo['tempo_real'].mean(), 2),        pontuacao = 0

                'tempo_medio_previsto': round(processos_tipo['het_previsto'].mean(), 2)        if eficiencia_media is not None:

            }            # Processos mais rápidos que previsto ganham mais pontos

                    for _, row in processos_analista.iterrows():

        # Ordenar por eficiência (melhores primeiro)                if pd.notna(row['eficiencia']):

        especializacao = dict(sorted(especializacao.items(), key=lambda x: x[1]['eficiencia_media']))                    if row['eficiencia'] < 0.8:  # 20% mais rápido

                                pontuacao += 150

        return especializacao                    elif row['eficiencia'] < 1.0:  # Dentro do prazo

                            pontuacao += 100

    def analisar_analista(self, analista_id):                    elif row['eficiencia'] < 1.2:  # Até 20% acima

        """Analisa desempenho de um analista"""                        pontuacao += 50

        processos = self.df_monitoramento[                    else:  # Muito acima do previsto

            self.df_monitoramento['analista_id'] == analista_id                        pontuacao += 10

        ]        

                # Análise de afinidade por tipo de processo

        if processos.empty:        afinidades = self._calcular_afinidade_tipos(processos_analista)

            return None        

                # Classificação geral (S, A, B, C, D)

        concluidos = processos[processos['status'] == 'concluido']        classificacao_geral = self._calcular_classificacao(eficiencia_media)

                

        if len(concluidos) == 0:        metricas = {

            return None            'analista_id': analista_id,

                    'total_processos': total_processos,

        eficiencia_media = concluidos['eficiencia'].mean()            'processos_concluidos': processos_concluidos,

        especializacao = self._calcular_especializacao_tipos(processos)            'processos_em_andamento': total_processos - processos_concluidos,

                    'eficiencia_media': round(eficiencia_media, 2) if eficiencia_media else None,

        analise = {            'pontuacao': pontuacao,

            'analista_id': analista_id,            'classificacao_geral': classificacao_geral,

            'volume_total': len(processos),            'afinidades_por_tipo': afinidades,

            'volume_concluido': len(concluidos),            'tempo_medio_real': processos_analista['tempo_real'].mean(),

            'volume_pendente': len(processos) - len(concluidos),            'tempo_medio_previsto': processos_analista['het_previsto'].mean(),

            'eficiencia_media': round(eficiencia_media, 3),            'processos_rapidos': len(processos_analista[processos_analista['eficiencia'] < 1.0]),

            'classificacao_geral': self._calcular_classificacao(eficiencia_media),            'processos_lentos': len(processos_analista[processos_analista['eficiencia'] >= 1.0])

            'especializacao_por_tipo': especializacao,        }

            'tempo_medio_real': round(concluidos['tempo_real'].mean(), 2),        

            'tempo_medio_previsto': round(concluidos['het_previsto'].mean(), 2),        return metricas

            'processos_rapidos': len(concluidos[concluidos['eficiencia'] < 1.0]),    

            'processos_lentos': len(concluidos[concluidos['eficiencia'] >= 1.0])    def calcular_metricas_gestor(self, turma_id):

        }        """Calcula métricas de performance de uma turma (gestor)"""

                processos_turma = self.df_monitoramento[

        return analise            self.df_monitoramento['turma'] == turma_id

            ]

    def analisar_turma(self, turma_id):        

        """Analisa desempenho de uma turma"""        if processos_turma.empty:

        processos = self.df_monitoramento[            return None

            self.df_monitoramento['turma'] == turma_id        

        ]        # Métricas da turma

                total_processos = len(processos_turma)

        if processos.empty:        processos_concluidos = len(processos_turma[processos_turma['status'] == 'concluido'])

            return None        taxa_conclusao = (processos_concluidos / total_processos) * 100

                

        concluidos = processos[processos['status'] == 'concluido']        # Eficiência média da turma

                eficiencia_media = processos_turma['eficiencia'].mean()

        if len(concluidos) == 0:        

            return None        # Analistas da turma

                analistas_unicos = processos_turma['analista_id'].nunique()

        eficiencia_media = concluidos['eficiencia'].mean()        

        especializacao = self._calcular_especializacao_tipos(processos)        # Distribuição por complexidade

                dist_complexidade = processos_turma['complexidade'].value_counts().to_dict()

        analise = {        

            'turma_id': turma_id,        # Pontuação da turma (soma das pontuações dos analistas)

            'volume_total': len(processos),        pontuacao_turma = 0

            'volume_concluido': len(concluidos),        for analista in processos_turma['analista_id'].unique():

            'taxa_conclusao': round((len(concluidos) / len(processos)) * 100, 2),            metricas_analista = self.calcular_metricas_analista(analista)

            'eficiencia_media': round(eficiencia_media, 3),            if metricas_analista:

            'classificacao_geral': self._calcular_classificacao(eficiencia_media),                pontuacao_turma += metricas_analista['pontuacao']

            'especializacao_por_tipo': especializacao,        

            'numero_analistas': processos['analista_id'].nunique(),        # Análise de afinidade por tipo de processo da turma

            'tempo_medio_real': round(concluidos['tempo_real'].mean(), 2),        afinidades_turma = self._calcular_afinidade_tipos(processos_turma)

            'tempo_medio_previsto': round(concluidos['het_previsto'].mean(), 2),        

            'processos_no_prazo': len(concluidos[concluidos['eficiencia'] <= 1.0]),        # Classificação geral da turma

            'processos_fora_prazo': len(concluidos[concluidos['eficiencia'] > 1.0])        classificacao_turma = self._calcular_classificacao(eficiencia_media)

        }        

                metricas = {

        return analise            'turma_id': turma_id,

                'total_processos': total_processos,

    def gerar_ranking_analistas(self):            'processos_concluidos': processos_concluidos,

        """Gera ranking de analistas por eficiência"""            'taxa_conclusao': round(taxa_conclusao, 2),

        analistas = self.df_monitoramento['analista_id'].unique()            'eficiencia_media': round(eficiencia_media, 2) if pd.notna(eficiencia_media) else None,

        ranking = []            'pontuacao': pontuacao_turma,

                    'classificacao_geral': classificacao_turma,

        for analista in analistas:            'afinidades_por_tipo': afinidades_turma,

            analise = self.analisar_analista(analista)            'numero_analistas': analistas_unicos,

            if analise and analise['volume_concluido'] > 0:            'distribuicao_complexidade': dist_complexidade,

                ranking.append(analise)            'tempo_medio_real': processos_turma['tempo_real'].mean(),

                    'tempo_medio_previsto': processos_turma['het_previsto'].mean(),

        # Ordenar por eficiência (menor = melhor)            'processos_no_prazo': len(processos_turma[processos_turma['eficiencia'] <= 1.0]),

        ranking = sorted(ranking, key=lambda x: x['eficiencia_media'])            'processos_atrasados': len(processos_turma[processos_turma['eficiencia'] > 1.0])

                }

        # Adicionar posição        

        for i, item in enumerate(ranking, 1):        return metricas

            item['posicao'] = i    

            def _calcular_classificacao(self, eficiencia_media):

        return ranking        """

            Calcula classificação baseada na eficiência média

    def gerar_ranking_turmas(self):        S = Excelente (< 0.70) - 30%+ mais rápido

        """Gera ranking de turmas por eficiência"""        A = Ótimo (0.70-0.85) - 15-30% mais rápido  

        turmas = self.df_monitoramento['turma'].unique()        B = Bom (0.85-1.00) - Dentro do prazo

        ranking = []        C = Regular (1.00-1.20) - Até 20% acima

                D = Necessita melhoria (> 1.20) - Muito acima

        for turma in turmas:        """

            analise = self.analisar_turma(turma)        if eficiencia_media is None:

            if analise and analise['volume_concluido'] > 0:            return 'N/A'

                ranking.append(analise)        

                if eficiencia_media < 0.70:

        # Ordenar por eficiência (menor = melhor)            return 'S'

        ranking = sorted(ranking, key=lambda x: x['eficiencia_media'])        elif eficiencia_media < 0.85:

                    return 'A'

        # Adicionar posição        elif eficiencia_media <= 1.00:

        for i, item in enumerate(ranking, 1):            return 'B'

            item['posicao'] = i        elif eficiencia_media <= 1.20:

                    return 'C'

        return ranking        else:

                return 'D'

    def gerar_dashboard_analista(self, analista_id, output_path=None):    

        """Gera dashboard completo para um analista"""    def _calcular_afinidade_tipos(self, df_processos):

        analise = self.analisar_analista(analista_id)        """

                Calcula afinidade (eficiência) por tipo de processo

        if not analise:        Retorna classificação S/A/B/C/D para cada tipo processado

            return None        """

                concluidos = df_processos[df_processos['status'] == 'concluido'].copy()

        ranking = self.gerar_ranking_analistas()        

        posicao = next((i['posicao'] for i in ranking if i['analista_id'] == analista_id), None)        if concluidos.empty:

                    return {}

        dashboard = {        

            'analista_id': analista_id,        # Agrupar por tipo de documento

            'data_geracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),        afinidades = {}

            'analise': analise,        

            'posicao_ranking': posicao,        for tipo in concluidos['tipo_documento'].unique():

            'total_analistas': len(ranking)            processos_tipo = concluidos[concluidos['tipo_documento'] == tipo]

        }            

                    if len(processos_tipo) == 0:

        if output_path:                continue

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)            

            with open(output_path, 'w', encoding='utf-8') as f:            eficiencia_tipo = processos_tipo['eficiencia'].mean()

                json.dump(dashboard, f, ensure_ascii=False, indent=2)            quantidade = len(processos_tipo)

                    

        return dashboard            afinidades[tipo] = {

                    'eficiencia_media': round(eficiencia_tipo, 2),

    def gerar_dashboard_turma(self, turma_id, output_path=None):                'classificacao': self._calcular_classificacao(eficiencia_tipo),

        """Gera dashboard completo para uma turma"""                'quantidade_processos': quantidade,

        analise = self.analisar_turma(turma_id)                'tempo_medio_real': round(processos_tipo['tempo_real'].mean(), 2),

                        'tempo_medio_previsto': round(processos_tipo['het_previsto'].mean(), 2)

        if not analise:            }

            return None        

                # Ordenar por eficiência (melhores primeiro)

        ranking = self.gerar_ranking_turmas()        afinidades = dict(sorted(afinidades.items(), key=lambda x: x[1]['eficiencia_media']))

        posicao = next((i['posicao'] for i in ranking if i['turma_id'] == turma_id), None)        

                return afinidades

        # Analistas da turma    

        processos_turma = self.df_monitoramento[self.df_monitoramento['turma'] == turma_id]    def gerar_ranking_analistas(self):

        analistas = processos_turma['analista_id'].unique()        """Gera ranking de analistas por pontuação"""

                analistas = self.df_monitoramento['analista_id'].unique()

        analistas_analise = []        ranking = []

        for analista in analistas:        

            analista_dados = self.analisar_analista(analista)        for analista in analistas:

            if analista_dados:            metricas = self.calcular_metricas_analista(analista)

                analistas_analise.append(analista_dados)            if metricas:

                        ranking.append(metricas)

        dashboard = {        

            'turma_id': turma_id,        # Ordenar por pontuação

            'data_geracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),        ranking = sorted(ranking, key=lambda x: x['pontuacao'], reverse=True)

            'analise_turma': analise,        

            'posicao_ranking': posicao,        # Adicionar posição

            'total_turmas': len(ranking),        for i, item in enumerate(ranking, 1):

            'analistas': analistas_analise            item['posicao'] = i

        }        

                return ranking

        if output_path:    

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)    def gerar_ranking_turmas(self):

            with open(output_path, 'w', encoding='utf-8') as f:        """Gera ranking de turmas por pontuação"""

                json.dump(dashboard, f, ensure_ascii=False, indent=2)        turmas = self.df_monitoramento['turma'].unique()

                ranking = []

        return dashboard        

            for turma in turmas:

    def executar(self):            metricas = self.calcular_metricas_gestor(turma)

        """Executa análise completa de desempenho"""            if metricas:

        print("\n" + "="*80)                ranking.append(metricas)

        print("ANÁLISE DE DESEMPENHO - CARF")        

        print("="*80)        # Ordenar por pontuação

                ranking = sorted(ranking, key=lambda x: x['pontuacao'], reverse=True)

        if not self.carregar_monitoramento():        

            return        # Adicionar posição

                for i, item in enumerate(ranking, 1):

        print("\nGerando análises...")            item['posicao'] = i

                

        # Gerar rankings        return ranking

        ranking_analistas = self.gerar_ranking_analistas()    

        ranking_turmas = self.gerar_ranking_turmas()    def gerar_dashboard_analista(self, analista_id, output_path='output/dashboard_analista.json'):

                """Gera dashboard completo para um analista"""

        if not ranking_analistas:        metricas = self.calcular_metricas_analista(analista_id)

            print("⚠️  Nenhum analista com processos concluídos")        ranking = self.gerar_ranking_analistas()

            return        

                # Encontrar posição do analista

        # Salvar rankings        posicao = next((i['posicao'] for i in ranking if i['analista_id'] == analista_id), None)

        Path('output').mkdir(exist_ok=True)        

        pd.DataFrame(ranking_analistas).to_excel('output/Ranking_Analistas.xlsx', index=False)        dashboard = {

        pd.DataFrame(ranking_turmas).to_excel('output/Ranking_Turmas.xlsx', index=False)            'analista_id': analista_id,

                    'data_geracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

        # Exibir resultados            'metricas': metricas,

        print(f"\n{'='*100}")            'posicao_ranking': posicao,

        print(f"RANKING DE ANALISTAS (por Eficiência)")            'total_analistas': len(ranking)

        print(f"{'='*100}")        }

        print(f"{'Pos':<5} {'Analista':<20} {'Class.':<8} {'Efic.':<8} {'Concl.':<8} {'Tempo Real':<12} {'Tempo Prev.':<12}")        

        print("-" * 100)        # Salvar JSON

                Path(output_path).parent.mkdir(exist_ok=True)

        for analista in ranking_analistas[:10]:  # Top 10        with open(output_path, 'w', encoding='utf-8') as f:

            print(f"{analista['posicao']:<5} "            json.dump(dashboard, f, ensure_ascii=False, indent=2)

                  f"{analista['analista_id']:<20} "        

                  f"{analista['classificacao_geral']:<8} "        return dashboard

                  f"{analista['eficiencia_media']:<8.3f} "    

                  f"{analista['volume_concluido']:<8} "    def gerar_dashboard_gestor(self, turma_id, output_path='output/dashboard_gestor.json'):

                  f"{analista['tempo_medio_real']:<12.2f} "        """Gera dashboard completo para um gestor (turma)"""

                  f"{analista['tempo_medio_previsto']:<12.2f}")        metricas = self.calcular_metricas_gestor(turma_id)

                    ranking = self.gerar_ranking_turmas()

            # Mostrar especialização        

            if analista['especializacao_por_tipo']:        # Encontrar posição da turma

                top_tipos = list(analista['especializacao_por_tipo'].items())[:3]        posicao = next((i['posicao'] for i in ranking if i['turma_id'] == turma_id), None)

                print(f"      Especialização: ", end="")        

                for tipo, dados in top_tipos:        # Detalhes dos analistas da turma

                    print(f"{tipo}({dados['classificacao']}, {dados['volume']}proc) ", end="")        analistas_turma = self.df_monitoramento[

                print()            self.df_monitoramento['turma'] == turma_id

                ]['analista_id'].unique()

        print(f"\n{'='*100}")        

        print(f"RANKING DE TURMAS (por Eficiência)")        analistas_metricas = []

        print(f"{'='*100}")        for analista in analistas_turma:

        print(f"{'Pos':<5} {'Turma':<10} {'Class.':<8} {'Efic.':<8} {'Concl.':<8} {'Taxa':<10} {'Analistas':<10}")            analista_metricas = self.calcular_metricas_analista(analista)

        print("-" * 100)            if analista_metricas:

                        analistas_metricas.append(analista_metricas)

        for turma in ranking_turmas:        

            print(f"{turma['posicao']:<5} "        dashboard = {

                  f"TURMA {turma['turma_id']:<4} "            'turma_id': turma_id,

                  f"{turma['classificacao_geral']:<8} "            'data_geracao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

                  f"{turma['eficiencia_media']:<8.3f} "            'metricas_turma': metricas,

                  f"{turma['volume_concluido']:<8} "            'posicao_ranking': posicao,

                  f"{turma['taxa_conclusao']:<9.1f}% "            'total_turmas': len(ranking),

                  f"{turma['numero_analistas']:<10}")            'analistas': analistas_metricas

                    }

            # Mostrar especialização        

            if turma['especializacao_por_tipo']:        # Salvar JSON

                top_tipos = list(turma['especializacao_por_tipo'].items())[:3]        Path(output_path).parent.mkdir(exist_ok=True)

                print(f"      Especialização: ", end="")        with open(output_path, 'w', encoding='utf-8') as f:

                for tipo, dados in top_tipos:            json.dump(dashboard, f, ensure_ascii=False, indent=2)

                    print(f"{tipo}({dados['classificacao']}, {dados['volume']}proc) ", end="")        

                print()        return dashboard

            

        print(f"\n{'='*100}")    def simular_dados_monitoramento(self):

        print("LEGENDA DE CLASSIFICAÇÃO")        """Simula dados de monitoramento para demonstração"""

        print(f"{'='*100}")        print("\n🎮 Simulando dados de monitoramento para demonstração...")

        print("S = Excelente        (eficiência < 0.70)  - 30%+ mais rápido que previsto")        

        print("A = Ótimo            (eficiência 0.70-0.85) - 15-30% mais rápido")        # Carregar processos categorizados

        print("B = Bom              (eficiência 0.85-1.00) - Dentro do prazo")        if not self.carregar_dados():

        print("C = Regular          (eficiência 1.00-1.20) - Até 20% acima")            return False

        print("D = Requer atenção   (eficiência > 1.20)  - Muito acima do previsto")        

        print()        # Criar dados simulados de monitoramento

        print("Eficiência = Tempo Real / HET Previsto")        np.random.seed(42)

                

        # Gerar dashboards exemplo        processos_sample = self.df_processos.sample(n=min(500, len(self.df_processos)))

        if ranking_analistas:        

            analista_top = ranking_analistas[0]['analista_id']        dados_monitoramento = []

            self.gerar_dashboard_analista(        

                analista_top,         for _, processo in processos_sample.iterrows():

                f'output/dashboard_analista_{analista_top}.json'            # Simular analista (1-20) e turma (1-8)

            )            analista_id = f"ANALISTA_{np.random.randint(1, 21):03d}"

                    turma = np.random.randint(1, 9)

        if ranking_turmas:            

            turma_top = ranking_turmas[0]['turma_id']            # Simular datas

            self.gerar_dashboard_turma(            dias_atras = np.random.randint(1, 90)

                turma_top,            data_inicio = datetime.now() - timedelta(days=dias_atras)

                f'output/dashboard_turma_{turma_top}.json'            

            )            # 80% dos processos estão concluídos

                    if np.random.random() < 0.8:

        print(f"\n{'='*80}")                dias_duracao = np.random.randint(1, dias_atras)

        print("ARQUIVOS GERADOS")                data_conclusao = data_inicio + timedelta(days=dias_duracao)

        print(f"{'='*80}")                status = 'concluido'

        print("✓ output/Ranking_Analistas.xlsx")                

        print("✓ output/Ranking_Turmas.xlsx")                # Tempo real (com variação em relação ao HET)

        print("✓ output/dashboard_analista_*.json")                het_previsto = processo['HET_FINAL']

        print("✓ output/dashboard_turma_*.json")                # 60% são mais rápidos, 40% mais lentos

        print()                if np.random.random() < 0.6:

                    tempo_real = het_previsto * np.random.uniform(0.6, 0.95)

                else:

if __name__ == '__main__':                    tempo_real = het_previsto * np.random.uniform(1.05, 1.5)

    sistema = AnaliseDesempenho()                

    sistema.executar()                eficiencia = tempo_real / het_previsto if het_previsto > 0 else None

            else:
                data_conclusao = None
                status = 'em_analise'
                tempo_real = None
                eficiencia = None
            
            dados_monitoramento.append({
                'processo_id': processo['ID'],
                'analista_id': analista_id,
                'turma': turma,
                'data_inicio': data_inicio,
                'data_conclusao': data_conclusao,
                'status': status,
                'het_previsto': processo['HET_FINAL'],
                'tempo_real': tempo_real,
                'eficiencia': eficiencia,
                'tipo_documento': processo.get('tipo_documento', 'OUTROS'),
                'complexidade': processo.get('complexidade', 'Médio')
            })
        
        self.df_monitoramento = pd.DataFrame(dados_monitoramento)
        print(f"   ✅ {len(self.df_monitoramento)} registros de monitoramento simulados")
        
        # Salvar dados de monitoramento
        self.df_monitoramento.to_excel('output/Monitoramento_Processos.xlsx', index=False)
        print(f"   💾 Salvo: output/Monitoramento_Processos.xlsx")
        
        return True
    
    def executar(self):
        """Executa o sistema completo de gamificação"""
        print("\n" + "="*80)
        print("🎮 SISTEMA DE GAMIFICAÇÃO E MONITORAMENTO - CARF")
        print("="*80)
        
        # Simular dados (em produção, isso viria de um banco de dados)
        if not self.simular_dados_monitoramento():
            print("❌ Erro ao simular dados")
            return
        
        print("\n📊 Gerando rankings e dashboards...")
        
        # Gerar rankings
        ranking_analistas = self.gerar_ranking_analistas()
        ranking_turmas = self.gerar_ranking_turmas()
        
        # Salvar rankings
        pd.DataFrame(ranking_analistas).to_excel('output/Ranking_Analistas.xlsx', index=False)
        pd.DataFrame(ranking_turmas).to_excel('output/Ranking_Turmas.xlsx', index=False)
        
        print(f"\n📊 TOP 5 ANALISTAS (por Pontuação):")
        print("-" * 100)
        print(f"{'Pos':<5} {'ID Analista':<20} {'Class.':<8} {'Efic.':<8} {'Proc.':<8} {'Pontos':<10}")
        print("-" * 100)
        for analista in ranking_analistas[:5]:
            print(f"{analista['posicao']:<5} {analista['analista_id']:<20} "
                  f"{analista['classificacao_geral']:<8} "
                  f"{analista['eficiencia_media']:<8.2f} "
                  f"{analista['processos_concluidos']:<8} "
                  f"{analista['pontuacao']:,}")
            
            # Mostrar top 3 afinidades
            if analista['afinidades_por_tipo']:
                afinidades_top = list(analista['afinidades_por_tipo'].items())[:3]
                print(f"      Maior Afinidade: ", end="")
                for tipo, dados in afinidades_top:
                    print(f"{tipo}({dados['classificacao']}) ", end="")
                print()
        
        print(f"\n📊 RANKING TURMAS (por Pontuação):")
        print("-" * 100)
        print(f"{'Pos':<5} {'Turma':<10} {'Class.':<8} {'Efic.':<8} {'Taxa Concl.':<12} {'Pontos':<10}")
        print("-" * 100)
        for turma in ranking_turmas:
            print(f"{turma['posicao']:<5} "
                  f"TURMA {turma['turma_id']:<4} "
                  f"{turma['classificacao_geral']:<8} "
                  f"{turma['eficiencia_media']:<8.2f} "
                  f"{turma['taxa_conclusao']:<11.1f}% "
                  f"{turma['pontuacao']:,}")
            
            # Mostrar top 3 afinidades
            if turma['afinidades_por_tipo']:
                afinidades_top = list(turma['afinidades_por_tipo'].items())[:3]
                print(f"      Tipos com melhor performance: ", end="")
                for tipo, dados in afinidades_top:
                    print(f"{tipo}({dados['classificacao']}, {dados['quantidade_processos']}proc) ", end="")
                print()
        
        print(f"\n📋 LEGENDA DE CLASSIFICAÇÃO:")
        print("   S = Excelente (< 0.70) - 30%+ mais rápido que previsto")
        print("   A = Ótimo (0.70-0.85) - 15-30% mais rápido")
        print("   B = Bom (0.85-1.00) - Dentro do prazo previsto")
        print("   C = Regular (1.00-1.20) - Até 20% acima do previsto")
        print("   D = Necessita melhoria (> 1.20) - Muito acima do previsto")
        
        # Gerar dashboards exemplo
        if len(ranking_analistas) > 0:
            analista_exemplo = ranking_analistas[0]['analista_id']
            self.gerar_dashboard_analista(analista_exemplo, f'output/dashboard_analista_{analista_exemplo}.json')
        
        if len(ranking_turmas) > 0:
            turma_exemplo = ranking_turmas[0]['turma_id']
            self.gerar_dashboard_gestor(turma_exemplo, f'output/dashboard_gestor_turma_{turma_exemplo}.json')
        
        print("\n✅ Arquivos gerados:")
        print("   📊 output/Monitoramento_Processos.xlsx")
        print("   🏆 output/Ranking_Analistas.xlsx")
        print("   🏆 output/Ranking_Turmas.xlsx")
        print("   📱 output/dashboard_analista_*.json")
        print("   📱 output/dashboard_gestor_turma_*.json")
        
        print("\n" + "="*80)
        print("🎉 Sistema de gamificação executado com sucesso!")
        print("="*80)


if __name__ == '__main__':
    sistema = MonitoramentoGamificacao()
    sistema.executar()
