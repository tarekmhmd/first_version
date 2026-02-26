# Notes for Cloning the Repository

This repository uses **Git LFS** for large files (DLLs, EXEs, trained data, etc.).  
To clone and get all files correctly, do the following:

```bash
git clone https://github.com/tarekmhmd/first_version.git
cd first_version
git lfs install    # if Git LFS is not installed
git lfs pull       # download large files


# 🏥 Medical AI Assistant

A comprehensive web-based medical assistant powered by artificial intelligence for health analysis and consultation.

## Features

- 🔬 **Skin Analysis**: AI-powered analysis of skin conditions using computer vision
- 🧪 **Lab Results Analysis**: Intelligent interpretation of laboratory test results
- 💬 **AI Chatbot**: Interactive medical consultation based on symptoms
- 🎤 **Sound Analysis**: Respiratory health assessment through audio analysis
- 📋 **Health Records**: Track and monitor your health history
- 👤 **User Profiles**: Personalized health tracking with profile completion

## Technology Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Responsive design with modern UI/UX principles

### Backend
- Python 3.11.4
- Flask (Web Framework)
- SQLite (Database)

### AI/ML
- TensorFlow / PyTorch (Deep Learning)
- OpenCV (Computer Vision)
- Librosa (Audio Processing)
- Pytesseract (OCR)

## Installation

### Prerequisites
- Python 3.11.4
- pip (Python package manager)

### Quick Start

1. **Clone or download the project**

2. **Run setup (First time only)**
   ```cmd
   setup.bat
   ```
   This will:
   - Create virtual environment
   - Install all dependencies
   - Download AI models
   - Initialize database

3. **Run the application**
   ```cmd
   run.bat
   ```

4. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Project Structure

```
medical-ai-assistant/
├── frontend/              # Frontend files
│   ├── index.html        # Login/Register page
│   ├── dashboard.html    # Main dashboard
│   ├── profile.html      # User profile
│   ├── skin-analysis.html
│   ├── lab-analysis.html
│   ├── chatbot.html
│   ├── sound-analysis.html
│   ├── health-records.html
│   ├── about.html
│   ├── contact.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
├── backend/              # Backend API
│   ├── app.py           # Main Flask application
│   ├── models/          # AI models
│   ├── database/        # Database management
│   └── utils/           # Helper functions
├── setup.bat            # Setup script
├── run.bat              # Run script
└── requirements.txt     # Python dependencies
```

## Usage

### First Time Setup
1. Run `setup.bat` to install everything
2. Wait for models to download
3. Run `run.bat` to start the server

### Daily Use
- Just run `run.bat` to start the application
- Access via browser at `http://localhost:5000`

## Docker Support

Build and run with Docker:

```bash
docker build -t medical-ai-assistant .
docker run -p 5000:5000 medical-ai-assistant
```

## Important Disclaimer

⚠️ **This application is for educational and informational purposes only.**

This application provides preliminary health information and should NOT be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## License

This project is for educational purposes.

## Support

For questions or issues, please contact: support@medicalai.com
