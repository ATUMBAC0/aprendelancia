#!/bin/bash
# Script para servir la documentación MkDocs
# Uso: ./serve_docs.sh

echo " Iniciando servidor de documentación MkDocs..."
echo ""

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Entorno virtual activado"
fi

# Verificar que mkdocs esté instalado
if ! command -v mkdocs &> /dev/null; then
    echo " MkDocs no está instalado"
    echo "Instalando dependencias..."
    pip install -r docs/requirements.txt
fi

# Servir documentación
echo ""
echo " Documentación disponible en: http://127.0.0.1:8080"
echo "Presiona Ctrl+C para detener el servidor"
echo ""

mkdocs serve -a 127.0.0.1:8080
