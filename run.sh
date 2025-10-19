#!/bin/bash

# 🎯 GUIA RÁPIDO - SISTEMA CARF
# Previsão de HET e Organização de Lotes

echo ""
echo "🚀 =============================================="
echo "   SISTEMA CARF - Previsão HET + Lotes"
echo "================================================"
echo ""

# Verificar se está no diretório correto
if [ ! -f "executar_pipeline.py" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto CARF"
    exit 1
fi

# Verificar se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "⚠️  Ambiente virtual não encontrado. Criando..."
    python3 -m venv .venv
    echo "✅ Ambiente virtual criado!"
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências se necessário
if ! python -c "import pandas" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    pip install -q -r docs/requirements.txt
    echo "✅ Dependências instaladas!"
fi

# Menu interativo
echo ""
echo "Escolha uma opção:"
echo ""
echo "1) 🎯 Executar PIPELINE COMPLETO (HET + Lotes)"
echo "2) 📊 Executar apenas PREVISÃO DE HET"
echo "3) 📦 Executar apenas ORGANIZAÇÃO DE LOTES"
echo "4) 📂 Ver estrutura do projeto"
echo "5) 📖 Ver README"
echo "6) 🚪 Sair"
echo ""
read -p "Opção: " opcao

case $opcao in
    1)
        echo ""
        echo "🚀 Executando pipeline completo..."
        python executar_pipeline.py
        ;;
    2)
        echo ""
        echo "📊 Executando previsão de HET..."
        python src/previsao_het.py
        ;;
    3)
        echo ""
        echo "📦 Executando organização de lotes..."
        python src/organizar_lotes.py
        ;;
    4)
        echo ""
        tree -L 2 -I '.venv|__pycache__|.git' --dirsfirst
        ;;
    5)
        echo ""
        cat README.md
        ;;
    6)
        echo ""
        echo "👋 Até logo!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac

echo ""
echo "✅ Concluído!"
echo ""
echo "📁 Arquivos gerados em: output/"
echo "   • Processos_com_HET.xlsx"
echo "   • Processos_Categorizados.xlsx"
echo "   • Lotes_para_Turmas.csv"
echo "   • Mapeamento_Parametros.csv"
echo ""
