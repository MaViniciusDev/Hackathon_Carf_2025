import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import joblib
import warnings
warnings.filterwarnings('ignore')


class PrevisaoHET:
    """Sistema simplificado de previsão de HET"""
    
    def __init__(self):
        self.modelo = None
        self.scaler = None
        self.imputer = None
        
    def executar(self):
        """Executa pipeline completo de previsão"""
        print("=" * 80)
        print("🎯 SISTEMA DE PREVISÃO DE HET - CARF")
        print("=" * 80)
        
        # 1. Carregar dados
        print("\n📊 Etapa 1: Carregando dados...")
        df = pd.read_excel('data/Horas_parametros.xlsx')
        print(f"   ✅ {len(df):,} processos carregados")
        
        # 2. Converter HET e separar treino/previsão
        df['HET_numerico'] = pd.to_numeric(df['HET'], errors='coerce')
        df_treino = df[df['HET_numerico'].notna()].copy()
        df_prever = df[df['HET_numerico'].isna()].copy()
        
        print(f"\n📊 Distribuição dos dados:")
        print(f"   • Processos com HET (treino): {len(df_treino):,}")
        print(f"   • Processos sem HET (prever): {len(df_prever):,}")
        
        # 3. Preparar features
        print(f"\n⚙️ Etapa 2: Preparando features...")
        param_cols = [col for col in df.columns if col not in ['ID', 'HET', 'HET_numerico']]
        
        X_treino = df_treino[param_cols].values
        y_treino = df_treino['HET_numerico'].values
        X_prever = df_prever[param_cols].values
        
        # 4. Preprocessamento
        print(f"   • Imputando valores faltantes...")
        self.imputer = SimpleImputer(strategy='constant', fill_value=0)
        X_treino = self.imputer.fit_transform(X_treino)
        X_prever = self.imputer.transform(X_prever)
        
        print(f"   • Normalizando features...")
        self.scaler = StandardScaler()
        X_treino = self.scaler.fit_transform(X_treino)
        X_prever = self.scaler.transform(X_prever)
        
        # 5. Treinar modelo
        print(f"\n🤖 Etapa 3: Treinando Ridge Regression...")
        self.modelo = Ridge(alpha=1.0, random_state=42)
        self.modelo.fit(X_treino, y_treino)
        
        # Métricas no treino
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        y_pred_treino = self.modelo.predict(X_treino)
        mae = mean_absolute_error(y_treino, y_pred_treino)
        rmse = np.sqrt(mean_squared_error(y_treino, y_pred_treino))
        r2 = r2_score(y_treino, y_pred_treino)
        
        print(f"\n📊 Métricas do modelo:")
        print(f"   • MAE (Erro Médio): {mae:.2f}h")
        print(f"   • RMSE: {rmse:.2f}h")
        print(f"   • R² Score: {r2:.3f} ({r2*100:.1f}%)")
        
        # 6. Fazer previsões
        print(f"\n🔮 Etapa 4: Gerando previsões...")
        previsoes = self.modelo.predict(X_prever)
        df_prever['HET_PREVISTO'] = previsoes
        
        # 7. Criar resultado final
        df_resultado = df.copy()
        df_resultado['HET_FINAL'] = df_resultado['HET_numerico'].fillna(
            df_resultado['ID'].map(dict(zip(df_prever['ID'], df_prever['HET_PREVISTO'])))
        )
        
        print(f"   ✅ {len(previsoes):,} previsões geradas")
        
        # 8. Salvar resultados
        print(f"\n💾 Etapa 5: Salvando resultados...")
        
        # Salvar Excel completo
        df_resultado.to_excel('output/Processos_com_HET.xlsx', index=False)
        print(f"   ✅ output/Processos_com_HET.xlsx")
        
        # Salvar modelos
        joblib.dump(self.modelo, 'models/ridge_model.pkl')
        joblib.dump(self.scaler, 'models/scaler.pkl')
        joblib.dump(self.imputer, 'models/imputer.pkl')
        print(f"   ✅ models/ridge_model.pkl")
        print(f"   ✅ models/scaler.pkl")
        print(f"   ✅ models/imputer.pkl")
        
        # 9. Estatísticas finais
        print(f"\n📊 Estatísticas Finais:")
        print(f"   • HET médio (treino): {df_treino['HET_numerico'].mean():.2f}h")
        print(f"   • HET médio (previsto): {previsoes.mean():.2f}h")
        print(f"   • HET mínimo: {df_resultado['HET_FINAL'].min():.2f}h")
        print(f"   • HET máximo: {df_resultado['HET_FINAL'].max():.2f}h")
        
        print(f"\n✅ PIPELINE CONCLUÍDO COM SUCESSO!")
        print("=" * 80)
        
        return df_resultado


if __name__ == "__main__":
    previsao = PrevisaoHET()
    previsao.executar()
