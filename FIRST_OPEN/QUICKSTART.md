# Quick Setup Guide

## Get Started in 3 Steps

### 1. Install Python 3.13
# Run the installer and add Python to PATH during installation
python-3.13.0-amd64.exe


### 2. Install Dependencies
```bash
cd docs
pip install -r requirements.txt
```

### 3. Run a Dashboard
```bash
# Choose one:
python h1a/run_h1a.py    # Port 8050 - Global Work Mode Shift
python h1b/run_h1b.py    # Port 8051 - Flexibility by Org Size
python h2/run_h2.py      # Port 8052 - Flexibility Gap Evolution
python h3/run_h3.py      # Port 8053 - Flexibility Dividend
python h4/run_h4.py      # Port 8054 - Experience vs Compensation
python h5/run_h5.py      # Port 8055 - Language Evolution
python h6a/run_h6a.py    # Port 8056 - Framework Cohorts
python h6b/run_h6b.py    # Port 8057 - Framework Lifecycles
python run_all.py        # All Ports - Run Before Opening html File
```

That's it! Your browser will open automatically at http://127.0.0.1:PORT
