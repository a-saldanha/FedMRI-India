#!/bin/bash

echo "🏥 FedMRI India - Setup Script"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

echo ""
echo "Installing dependencies..."
uv pip install -q gradio plotly pandas numpy pillow

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Launching FedMRI India demo..."
echo "   The app will open in your browser automatically."
echo "   A shareable public link will also be generated."
echo ""

python3 fedmri_demo.py
