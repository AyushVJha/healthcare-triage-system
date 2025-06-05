# Healthcare Triage System 🏥

A lightweight, efficient healthcare triage system that helps medical professionals and patients assess symptoms and medical images quickly and accurately.

## Features

- **Symptom Analysis**: Quick assessment of patient symptoms with severity scoring
- **Image Analysis**: Basic analysis of medical images (skin conditions, wounds, general)
- **Patient Dashboard**: Track and monitor patient cases
- **System Analytics**: Monitor system performance and patient flow
- **Resource Allocation**: Smart allocation of medical resources based on priority

## System Requirements

- Python 3.8+
- 4GB RAM minimum
- Web browser for UI access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/healthcare-triage.git
cd healthcare-triage
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

1. Run the application:
```bash
streamlit run app.py
```

2. Access the web interface at `http://localhost:8501`

## Project Structure

```
healthcare-triage/
├── app.py                 # Main Streamlit application
├── models/
│   ├── symptom_analyzer.py    # Symptom analysis logic
│   └── image_analyzer.py      # Image analysis logic
├── utils/
│   └── triage_logic.py        # Triage and resource allocation
├── requirements.txt       # Python dependencies
└── deploy.sh             # Deployment script
```

## Key Components

### Symptom Analyzer
- Lightweight rule-based analysis
- Severity scoring
- Specialty recommendation
- Priority level determination

### Image Analyzer
- Basic computer vision analysis
- Color and texture analysis
- Shape detection
- Severity assessment

### Triage Logic
- Queue management
- Wait time estimation
- Resource allocation
- Priority-based routing

## Usage

1. **Symptom Analysis**
   - Enter patient information
   - Describe symptoms
   - Get immediate severity assessment
   - Receive specialty recommendations

2. **Image Analysis**
   - Upload medical images
   - Select image type
   - Get preliminary analysis
   - Receive recommendations

3. **Patient Dashboard**
   - Monitor patient cases
   - Track priority levels
   - View wait times
   - Access patient history

4. **System Analytics**
   - Monitor system performance
   - Track patient flow
   - Analyze resource utilization

## Performance Considerations

- Optimized for low-resource environments
- Minimal CPU/GPU usage
- Efficient memory management
- Fast response times

## Security

- No sensitive data storage
- Local processing only
- No external API calls
- Basic input validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

## Disclaimer

This system is for preliminary assessment only and should not replace professional medical advice. Always consult healthcare professionals for proper medical evaluation and treatment. 