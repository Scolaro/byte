@echo off
echo Installing required libraries...
python -m pip install -r requirements.txt

echo Starting House Project Calculator...
python -m streamlit run app.py
pause
