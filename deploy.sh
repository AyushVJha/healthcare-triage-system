 #!/bin/bash

# Lightweight deployment script
echo "🚀 Deploying Healthcare Triage System..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install minimal requirements
pip install --no-cache-dir -r requirements.txt

# Run the application
echo "🏥 Starting Healthcare Triage System..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

echo "✅ Deployment complete! Access at http://localhost:8501"
