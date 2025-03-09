# Panduan Menjalankan Jupyter Notebook dan Streamlit Lokal

## 1. Membuat Virtual Environment

### Untuk Windows:
```bash
# Membuat virtual environment
python -m venv myenv

# Mengaktifkan virtual environment
myenv\Scripts\activate.bat
```

### Untuk MacOs/Linux:
```bash
# Membuat virtual environment
python3 -m venv myenv

# Mengaktifkan virtual environment
source myenv/bin/activate
```

## 2. Install Library yang perlukan

```bash
# Install library dasar
pip install jupyter notebook streamlit numpy pandas matplotlib seaborn

# Install dari requirements.txt
pip install -r requirements.txt
```

## 3. Menjalankan Jupyter Notebook
```bash
jupyter notebook
```

## 4. Menjalankan Aplikasi Streamlit
```bash
streamlit run dashboard.py
```
