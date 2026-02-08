#!/bin/bash
# Setup ambiente de desarrollo - Licitarte

echo "🔧 Configurando ambiente de desarrollo..."

# Web
echo "📦 Instalando dependencias web..."
cd web
python -m venv venv
source venv/bin/activate 2>/dev/null || venv\Scripts\activate
pip install -r requirements.txt

# Desktop
echo "📦 Instalando dependencias desktop..."
cd ../desktop
python -m venv venv
source venv/bin/activate 2>/dev/null || venv\Scripts\activate
pip install -r requirements.txt

echo "✅ Setup completado"
echo ""
echo "Para iniciar:"
echo "  Web:     cd web && python app.py"
echo "  Desktop: cd desktop && python main.py"
