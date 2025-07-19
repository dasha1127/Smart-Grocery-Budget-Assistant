# Smart Grocery & Budget Assistant - Setup Instructions

## Installation Steps

### 1. Environment Setup

First, ensure you have Python 3.7+ installed:
```bash
python --version
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv grocery_env

# Activate virtual environment
# On macOS/Linux:
source grocery_env/bin/activate
# On Windows:
grocery_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

### 5. Access the App
Open your web browser and navigate to:
```
http://localhost:8501
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

2. **Missing Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Permission Issues on macOS**
   ```bash
   chmod +x app.py
   ```

### System Requirements
- Python 3.7 or higher
- 2GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari, Edge)

## First Time Setup

1. Start the app
2. Navigate to "Add Grocery Item"
3. Add a few sample items
4. Go to "Budget Manager" and set monthly budgets
5. Explore the Dashboard and Analytics

Enjoy smart grocery management! 🛒
