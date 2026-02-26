# Installation Guide - Medical AI Assistant

## System Requirements

- **Operating System**: Windows 10/11
- **Python Version**: 3.11.4 (Already installed on your system)
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space
- **Internet**: Required for initial setup

## Step-by-Step Installation

### Step 1: Verify Python Installation

Open Command Prompt and run:
```cmd
python --version
```

You should see: `Python 3.11.4`

### Step 2: Navigate to Project Directory

```cmd
cd path\to\medical-ai-assistant
```

### Step 3: Run Setup (First Time Only)

Double-click `setup.bat` or run in Command Prompt:
```cmd
setup.bat
```

This will:
1. Create a virtual environment
2. Install all required Python packages
3. Download AI models (if available)
4. Initialize the database
5. Create necessary folders

**Note**: This may take 5-15 minutes depending on your internet speed.

### Step 4: Start the Application

Double-click `run.bat` or run:
```cmd
run.bat
```

The application will start and automatically open in your browser at:
`http://localhost:5000`

## Troubleshooting

### Problem: "Python is not recognized"
**Solution**: Add Python to your system PATH or reinstall Python with "Add to PATH" option checked.

### Problem: "pip install failed"
**Solution**: 
1. Update pip: `python -m pip install --upgrade pip`
2. Run setup.bat again

### Problem: "Port 5000 already in use"
**Solution**: 
1. Close any application using port 5000
2. Or edit `backend/app.py` and change the port number

### Problem: "Module not found"
**Solution**: 
1. Activate virtual environment: `venv\Scripts\activate`
2. Install requirements: `pip install -r requirements.txt`

## First Time Usage

1. **Register an Account**
   - Open `http://localhost:5000`
   - Click "Register" tab
   - Fill in your details
   - Click "Register"

2. **Login**
   - Enter your email and password
   - Click "Login"

3. **Complete Your Profile**
   - Go to Profile page
   - Fill in all information
   - This helps the AI provide better assessments

4. **Start Using Features**
   - Try Skin Analysis
   - Upload Lab Reports
   - Chat with AI
   - Analyze Respiratory Sounds

## Updating the Application

To update to a new version:
1. Download the new version
2. Copy your `medical_assistant.db` file (to keep your data)
3. Run `setup.bat` again
4. Replace the database file

## Uninstallation

To remove the application:
1. Delete the project folder
2. (Optional) Remove Python if not needed for other projects

## Getting Help

If you encounter any issues:
1. Check the troubleshooting section above
2. Review error messages carefully
3. Contact support: support@medicalai.com

## Security Notes

- Change the SECRET_KEY in `.env` file for production use
- Never share your database file
- Keep your login credentials secure
- This application is for personal use only
